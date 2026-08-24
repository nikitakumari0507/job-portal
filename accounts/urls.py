from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
     path('login/', views.login_view, name='login'),
     path('logout/', views.logout_view, name='logout'),
      path(
        'candidate-dashboard/',
        views.candidate_dashboard,
        name='candidate_dashboard'
    ),
      path(
    'employer-dashboard/',
    views.employer_dashboard,
    name='employer_dashboard'
),
path(
    "edit-profile/",
    views.edit_profile,
    name="edit_profile"
),
path(
    "about/",
    views.about,
    name="about"
),

path(
    "companies/",
    views.companies,
    name="companies"
),

path(
    "contact/",
    views.contact,
    name="contact"
),

path(
    "login-choice/",
    views.login_choice,
    name="login_choice",
),

path(
    "register-choice/",
    views.register_choice,
    name="register_choice",
),
]