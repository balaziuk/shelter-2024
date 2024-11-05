from django.shortcuts import render, redirect, get_object_or_404
from .models import Animal, VolunteeringActivity
from .forms import AnimalForm, AdoptionForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import logout
from django.utils import timezone
from django.contrib import messages


def homepage(request):
    return render(request, 'shelter/homepage.html')

def animal_list(request):
    animals = Animal.objects.all()   
    return render(request, 'shelter/animal_list.html', {'animals': animals})

def animal_list_dogs(request):
    animals = Animal.objects.filter(species='dog', adopted=False)
    return render(request, 'shelter/animal_list.html', {'animals': animals})

def animal_list_cats(request):
    animals = Animal.objects.filter(species='cat', adopted=False)
    return render(request, 'shelter/animal_list.html', {'animals': animals})

def animal_list_other(request):
    animals = Animal.objects.filter(species='other', adopted=False)
    return render(request, 'shelter/animal_list.html', {'animals': animals})

def profile(request):
    if not request.user.is_authenticated:
        return redirect('account_login')

    adopted_animals = Animal.objects.filter(adopted_by=request.user)
    volunteering_activities = VolunteeringActivity.objects.filter(volunteer=request.user) if request.user.volunteer else None

    roles = []
    if request.user.is_staff_member:
        roles.append('staff')
    if request.user.is_volunteer:
        roles.append('volunteer')
    if request.user.is_adopter:
        roles.append('adopter')

    if request.method == "POST" and "activity_type" in request.POST:
        # Створення волонтерської діяльності
        animal_id = request.POST.get("animal_id")
        activity_type = request.POST.get("activity_type")
        animal = Animal.objects.get(id=animal_id)
        VolunteeringActivity.objects.create(
            volunteer=request.user,
            animal=animal,
            activity_type=activity_type,
            timestamp=timezone.now()
        )
        return redirect("profile")

    animals = Animal.objects.all()

    return render(request, 'shelter/profile.html', {
        'adopted_animals': adopted_animals,
        'volunteering_activities': volunteering_activities,
        'roles': roles,
        'animals': animals
    })


def logout_view(request):
    logout(request)
    return redirect('homepage')

def add_animal(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  
            return redirect('animal_list')  
    else:
        form = AnimalForm() 

    return render(request, 'shelter/add_animal.html', {'form': form})

@login_required
def adopt_animal(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)

    if animal.adopted:
        messages.error(request, "Ця тварина вже усиновлена.")
        return redirect('animal_list')

    if request.method == "POST":
        form = AdoptionForm(request.POST)
        if form.is_valid() and form.cleaned_data.get("agree_to_adopt"):
            animal.adopt(request.user) 
            messages.success(request, "Дякуємо за усиновлення! Ви стали опікуном тварини.")
            return redirect('profile')
    else:
        form = AdoptionForm()

    return render(request, 'shelter/adopt_animal.html', {'animal': animal, 'form': form})