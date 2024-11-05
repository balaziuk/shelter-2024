from django.urls import path
from .views import animal_list_dogs, animal_list_cats, animal_list_other, animal_list, profile, add_animal
from allauth.account.views import LoginView, SignupView
from .views import logout_view
from . import views


urlpatterns = [
    path('animals/', animal_list, name='animal_list'),
    path('animals/dogs/', animal_list_dogs, name='animal_list_dogs'),
    path('animals/cats/', animal_list_cats, name='animal_list_cats'),
    path('animals/other/', animal_list_other, name='animal_list_other'),
    path('profile/', profile, name='profile'),
    path('login/', LoginView.as_view(), name='account_login'),  
    path('logout/', logout_view, name='logout'),
    path('signup/', SignupView.as_view(), name='account_signup'),  
    path('adopt_animal/<int:animal_id>/', views.adopt_animal, name='adopt_animal'),
    path('add-animal/', add_animal, name='add_animal'),
]