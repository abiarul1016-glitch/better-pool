from django import forms
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from carpool.models import CarpoolGroup, Child, ParentProfile, School


class ParentSignupForm(UserCreationForm):
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
    requested_neighbourhood = request.GET.get("neighbourhood", "")

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
