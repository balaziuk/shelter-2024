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

# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Animal, AdoptionRequest
from .forms import AdoptionForm
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from django.contrib import messages
@login_required
def adopt_animal(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id)

    if animal.adopted:
        messages.error(request, "Ця тварина вже усиновлена.")
        return redirect('animal_list')

    if request.method == "POST":
        form = AdoptionForm(request.POST)
        if form.is_valid():
            # Створюємо запис у базі для заявки
            adoption_request = form.save(commit=False)
            adoption_request.user = request.user  # Призначаємо користувача
            adoption_request.animal = animal  # Призначаємо тварину
            adoption_request.save()

            # Змінюємо статус тварини на усиновлену
            animal.adopt(adoption_request.user)  # Викликаємо метод adopt

            messages.success(request, f"Ви успішно подали заявку на усиновлення тварини {animal.name}.")
            
            # Після успішної подачі форми перенаправляємо на сторінку завантаження PDF
            return redirect('download_pdf', animal_id=animal.id)

    else:
        form = AdoptionForm()

    return render(request, 'shelter/adopt_animal.html', {'animal': animal, 'form': form})


from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse
from .models import AdoptionRequest
from django.shortcuts import get_object_or_404

def generate_adoption_pdf(request, animal_id):
    # Get the relevant adoption request from the database
    adoption_request = get_object_or_404(AdoptionRequest, animal__id=animal_id, user=request.user)

    # Create PDF
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    # Use standard Helvetica font
    pdf.setFont("Helvetica", 12)  # Use standard Helvetica font

    # Add text to the PDF
    pdf.drawString(100, 800, f"Adoption Request for Animal {adoption_request.animal.name}")
    pdf.drawString(100, 780, f"First Name: {adoption_request.first_name}")
    pdf.drawString(100, 760, f"Last Name: {adoption_request.last_name}")
    pdf.drawString(100, 740, f"Date of Birth: {adoption_request.birth_date}")
    pdf.drawString(100, 720, f"Address: {adoption_request.address}")
    pdf.drawString(100, 700, f"Phone Number: {adoption_request.phone_number}")
    pdf.drawString(100, 680, f"Email: {adoption_request.email}")
    pdf.drawString(100, 660, f"Animal: {adoption_request.animal.name}")
    pdf.drawString(100, 640, f"Agree to Adopt: {adoption_request.agree_to_adopt}")

    pdf.showPage()
    pdf.save()

    # Return the PDF response
    buffer.seek(0)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="adoption_request_{adoption_request.animal.id}.pdf"'
    response.write(buffer.read())
    return response
