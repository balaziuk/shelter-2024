from django.db import models
from django.contrib.auth.models import AbstractUser


class Animal(models.Model):

    SPECIES_CHOICES = [
        ('dog', 'Собака'),     
        ('cat', 'Кіт'),
        ('other', 'Інше'),
    ]
    GENDER_CHOICES = [
        ('male', 'Хлопчик'),  
        ('female', 'Дівчинка'),  
    ]
    name = models.CharField(max_length=100)  
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES) 
    species = models.CharField(max_length=10, choices=SPECIES_CHOICES, default='other')  
    breed = models.CharField(max_length=100, blank=True, null=True)  
    age = models.IntegerField()  
    health_status = models.CharField(max_length=255) 
    adopted = models.BooleanField(default=False) 
    adopted_by = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL, related_name='adopted_pets')
    shelter = models.ForeignKey('Shelter', on_delete=models.CASCADE, related_name='pets')
    photo = models.ImageField(upload_to='animal_photos/', null=True, blank=True)  
    
    def adopt(self, user):
        self.adopted = True
        self.adopted_by = user
        self.save()

    def __str__(self):
        return self.name
    
class User(AbstractUser):
    staff_member = models.BooleanField(default=False)  # Персонал
    volunteer = models.BooleanField(default=False)  # Волонтер
    adopter = models.BooleanField(default=False)  # Усиновлювач

    def __str__(self):
        return self.username
    
    def change_role(self, role):
        if self.staff_member and role == 'staff':
            return False
        elif role == 'volunteer':
            self.volunteer = True
        elif role == 'adopter':
            self.adopter = True
        self.save()
        return True
    
    @property
    def is_staff_member(self):
        return self.staff_member

    @property
    def is_volunteer(self):
        return self.volunteer

    @property
    def is_adopter(self):
        return self.adopter

class Shelter(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class VolunteeringActivity(models.Model):
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE)  
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)  
    activity_type = models.CharField(max_length=100)  
    timestamp = models.DateTimeField(auto_now_add=True)  


class AdoptionRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    agree_to_adopt = models.BooleanField()

    def __str__(self):
        return f"Заява на усиновлення тварини {self.animal.name} від {self.first_name} {self.last_name}"