from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Animal, Shelter, VolunteeringActivity

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('staff_member', 'volunteer', 'adopter')}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Animal)
admin.site.register(Shelter)
admin.site.register(VolunteeringActivity)
