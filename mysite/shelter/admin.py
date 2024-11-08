from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Animal, Shelter, VolunteeringActivity, AdoptionRequest

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('staff_member', 'volunteer', 'adopter')}),  # додавання кастомних полів для користувача
    )

# Реєстрація моделі AdoptionRequest
@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'animal', 'user', 'birth_date', 'address', 'phone_number', 'email', 'agree_to_adopt')
    search_fields = ('first_name', 'last_name', 'animal__name', 'user__username')  # Додавання полів для пошуку
    list_filter = ('agree_to_adopt',)  # Додавання фільтру за полем 'agree_to_adopt'

# Реєстрація інших моделей
admin.site.register(User, CustomUserAdmin)
admin.site.register(Animal)
admin.site.register(Shelter)
admin.site.register(VolunteeringActivity)
