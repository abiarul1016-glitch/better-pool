from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from carpool.models import CarpoolGroup, Child, ParentProfile, School


class ParentSignupForm(UserCreationForm):
    """
    Custom form, combining both Django User elements, and custom Parent Details
    """

    phone_number = forms.CharField(max_length=20)
    home_address = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
    city = forms.CharField(max_length=100)
    neighborhood = forms.CharField(max_length=100)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email")

    def save(self, commit=True):
        user = super().save(commit=commit)

        # Create and link the ParentProfile automatically
        ParentProfile.objects.create(
            user=user,
            phone_number=self.cleaned_data["phone_number"],
            home_address=self.cleaned_data["home_address"],
            city=self.cleaned_data["city"],
            neighborhood=self.cleaned_data["neighborhood"],
        )
        return user


# Create your views here.
def index(request):
    return render(request, "carpool/index.html")


def search(request):
    requested_neighbourhood: str = request.GET.get("neighbourhood", "")

    if requested_neighbourhood:
        carpool_groups = CarpoolGroup.objects.filter(
            driver__neighborhood=requested_neighbourhood
        )
    else:
        carpool_groups = []

    return render(
        request,
        "carpool/results.html",
        {
            "carpool_groups": carpool_groups,
        },
    )


def signup(request):
    if request.method == "POST":
        form = ParentSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("carpool:index")
    else:
        form = ParentSignupForm()

    return render(request, "carpool/signup.html", {"form": form})


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "carpool/login.html", {"form": form})


@login_required
def profile_view(request):
    try:
        profile = request.user.parent_profile
    except ParentProfile.DoesNotExist:
        # If they haven't finished setting up their profile data yet
        return redirect("carpool:profile_setup")

    # Prefetch related data for clean template iteration
    children = profile.children.all()
    driving_groups = profile.driving_groups.all()
    joined_carpools = profile.joined_carpools.all()

    context = {
        "profile": profile,
        "children": children,
        "driving_groups": driving_groups,
        "joined_carpools": joined_carpools,
    }
    return render(request, "carpool/profile.html", context)


def group_details(request, group_id):

    group = get_object_or_404(CarpoolGroup, pk=group_id)

    if request.method == "POST":
        # Ensure the user is logged in before they can join
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to join a carpool group.")
            return redirect("login")

        try:
            # Fetch the logged-in parent's profile
            parent_profile = request.user.parent_profile
        except ParentProfile.DoesNotExist:
            messages.error(
                request, "You must complete your Parent Profile before joining groups."
            )
            return redirect(
                "carpool:profile_setup"
            )  # Adjust to your profile setup view name

        # Check if the parent already the driver?
        if group.driver == parent_profile:
            messages.warning(request, "You are the driver of this group!")
            return redirect("carpool:group_detail", group_id=group.id)

        # Check if the parent already a passenger?
        if parent_profile in group.passengers.all():
            messages.info(request, "You have already joined this carpool group.")
            return redirect("carpool:group_detail", group_id=group.id)

        # Check if the carpool already full?
        if group.passengers.count() >= group.max_capacity:
            messages.error(request, "Sorry, this carpool group is already full!")
            return redirect("carpool:group_detail", group_id=group.id)

        # Add the parent to the ManyToMany relationship if they pass the checks
        group.passengers.add(parent_profile)
        messages.success(
            request, f"Successfully joined {group.name}! The driver has been notified."
        )
        return redirect("carpool:group_detail", group_id=group.id)

    # 3. Handle the standard page viewing (GET)
    # Check if the current user is already a member of this carpool to toggle buttons in HTML
    is_member = False
    if request.user.is_authenticated:
        try:
            is_member = request.user.parent_profile in group.passengers.all()
        except ParentProfile.DoesNotExist:
            pass

    return render(
        request,
        "carpool/group.html",
        {
            "group": group,
            "is_member": is_member,
        },
    )
