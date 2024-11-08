from django import forms
from .models import User, Animal, AdoptionRequest
from allauth.account.forms import SignupForm


class CustomSignupForm(SignupForm):
    staff_member = forms.BooleanField(required=False)
    volunteer = forms.BooleanField(required=False)
    adopter = forms.BooleanField(required=False)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.staff_member = self.cleaned_data['staff_member']
        user.volunteer = self.cleaned_data['volunteer']
        user.adopter = self.cleaned_data['adopter']
        user.save()
        return user


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = [
            'name',
            'gender',
            'species',
            'breed',
            'age',
            'health_status',
            'adopted',
            'adopted_by',
            'shelter',
            'photo',
        ]
        widgets = {
            'photo': forms.ClearableFileInput(attrs={'multiple': False}),
        }

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 0:
            raise forms.ValidationError("Вік не може бути від'ємним!")
        return age


class UserRoleChangeForm(forms.Form):
    role = forms.ChoiceField(choices=[('volunteer', 'Волонтер'), ('adopter', 'Усиновлювач')], label="Додати роль")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_role(self):
        role = self.cleaned_data.get('role')
        if self.user.is_staff_member:
            return role
        elif role == 'staff':
            raise forms.ValidationError("Не можна призначити роль персоналу.")
        return role

    def save(self):
        role = self.cleaned_data.get('role')
        if role == 'volunteer':
            self.user.volunteer = True
        elif role == 'adopter':
            self.user.adopter = True
        self.user.save()

class AdoptionForm(forms.ModelForm):
    first_name = forms.CharField(label="Ім'я", max_length=50)
    last_name = forms.CharField(label="Прізвище", max_length=50)
    birth_date = forms.DateField(label="Дата народження", widget=forms.SelectDateWidget(years=range(1900, 2025)))
    address = forms.CharField(label="Адреса проживання", widget=forms.Textarea)
    phone_number = forms.CharField(max_length=15, required=True, label="Номер телефону")
    email = forms.EmailField(required=True, label="Електронна адреса")
    agree_to_adopt = forms.BooleanField(label="Погоджуюся на усиновлення", required=True)

    class Meta:
        model = AdoptionRequest  # Тепер форма зв'язана з моделлю AdoptionRequest
        fields = ['first_name', 'last_name', 'birth_date', 'address', 'phone_number', 'email', 'agree_to_adopt']