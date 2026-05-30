from django.contrib import admin

from .models import CarpoolGroup, Child, ParentProfile, School

admin.site.register(School)
admin.site.register(ParentProfile)
admin.site.register(Child)
admin.site.register(CarpoolGroup)
