from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme

from jobs.models import Job, Application, SavedJob
from .models import User
from pathlib import Path

def register_view(request):

    if request.method == "POST":

        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        phone = request.POST.get("phone", "").strip()
        user_type = request.POST.get("user_type", "").strip()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        profile_image = request.FILES.get("profile_image")

        # Check required fields
        if not full_name or not email or not password or not confirm_password:
            messages.error(
                request,
                "Please fill all required fields."
            )
            return render(request, "register.html")

        # Check user type
        if user_type not in ["candidate", "employer"]:
            messages.error(
                request,
                "Please select Candidate or Employer."
            )
            return render(request, "register.html")

        # Check password
        if password != confirm_password:
            messages.error(
                request,
                "Passwords do not match."
            )
            return render(request, "register.html")

        if len(password) < 8:
            messages.error(request, "Password must contain at least 8 characters.")
            return render(request, "register.html")

        if profile_image:
            if Path(profile_image.name).suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
                messages.error(request, "Profile photo must be a JPG, PNG, or WEBP image.")
                return render(request, "register.html")
            if profile_image.size > 3 * 1024 * 1024:
                messages.error(request, "Profile photo must be smaller than 3 MB.")
                return render(request, "register.html")

        # Check existing email
        if User.objects.filter(email=email).exists():
            messages.error(
                request,
                "An account with this email already exists."
            )
            return render(request, "register.html")

        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=full_name,
            phone=phone,
            user_type=user_type,
            password=password,
        )

        # Save profile image
        if profile_image:
            user.profile_image = profile_image
            user.save()

        messages.success(
            request,
            "Account created successfully. Please login."
        )

        return redirect("login")

    return render(
        request,
        "register.html"
    ) 

def login_view(request):

    next_url = request.POST.get("next") or request.GET.get("next")

    if request.method == "POST":

        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password")

        if not email or not password:
            messages.error(
                request,
                "Please enter your email and password."
            )
            return render(request, "login.html", {"next": next_url})

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:

            login(request, user)

            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)

            # Candidate
            if user.user_type == "candidate":
                return redirect("candidate_dashboard")

            # Employer
            elif user.user_type == "employer":
                return redirect("employer_dashboard")

            # Invalid user type
            else:
                logout(request)

                messages.error(
                    request,
                    "Invalid account type."
                )

                return render(request, "login.html", {"next": next_url})

        # Wrong email/password
        messages.error(
            request,
            "Invalid email or password."
        )

        return render(request, "login.html", {"next": next_url})

    return render(request, "login.html", {"next": next_url})
@login_required
def candidate_dashboard(request):

    if request.user.user_type != "candidate":
        messages.error(request, "Only candidates can access this page.")
        return redirect("employer_dashboard")

    applications = Application.objects.filter(
        candidate=request.user
    ).select_related(
        "job",
        "job__employer"
    ).order_by(
        "-applied_at"
    )

    saved_jobs = SavedJob.objects.filter(
        candidate=request.user
    ).select_related(
        "job",
        "job__employer"
    ).order_by(
        "-saved_at"
    )

    applied_job_ids = applications.values_list(
        "job_id",
        flat=True
    )

    recommended_jobs = Job.objects.filter(
        is_active=True
    ).exclude(
        id__in=applied_job_ids
    ).select_related(
        "employer"
    ).order_by(
        "-created_at"
    )[:3]

    profile_points = 0

    if request.user.first_name:
        profile_points += 20

    if request.user.email:
        profile_points += 20

    if request.user.phone:
        profile_points += 20

    if request.user.profile_image:
        profile_points += 20

    if request.user.resume:
        profile_points += 20

    context = {
        "applications_count": applications.count(),
        "saved_jobs_count": saved_jobs.count(),
        "recent_applications": applications[:3],
        "recent_saved_jobs": saved_jobs[:2],
        "recommended_jobs": recommended_jobs,
        "profile_completion": profile_points,
        "context_interviews": 0,
"profile_views": 0,
    }

    return render(
        request,
        "candidate-dashboard.html",
        context
    )


@login_required
def employer_dashboard(request):

    if request.user.user_type != "employer":
        messages.error(
            request,
            "Only employers can access this page."
        )
        return redirect("home")

    employer_jobs = Job.objects.filter(
        employer=request.user
    )

    recent_jobs = employer_jobs.order_by(
        "-created_at"
    )[:4]

    total_jobs = employer_jobs.count()

    active_jobs = employer_jobs.filter(
        is_active=True
    ).count()

    closed_jobs = employer_jobs.filter(
        is_active=False
    ).count()

    total_applications = Application.objects.filter(
        job__employer=request.user
    ).count()

    recent_applications = Application.objects.filter(
        job__employer=request.user
    ).select_related(
        "job",
        "candidate"
    ).order_by(
        "-applied_at"
    )[:5]

    context = {
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "closed_jobs": closed_jobs,
        "total_applications": total_applications,
        "recent_jobs": recent_jobs,
        "recent_applications": recent_applications,
    }

    return render(
        request,
        "employer-dashboard.html",
        context
    )

@login_required
def edit_profile(request):

    user = request.user

    if request.method == "POST":

        user.first_name = request.POST.get(
            "full_name"
        )

        user.phone = request.POST.get(
            "phone"
        )

        if request.FILES.get("profile_image"):
            user.profile_image = request.FILES.get(
                "profile_image"
            )

        if request.FILES.get("resume"):
            user.resume = request.FILES.get(
                "resume"
            )

        user.save()

        messages.success(
            request,
            "Profile updated successfully."
        )

        dashboard = "employer_dashboard" if user.user_type == "employer" else "candidate_dashboard"
        return redirect(dashboard)

    return render(
        request,
        "edit-profile.html",
        {
            "user": user
        }
    )


def logout_view(request):

    logout(request)

    return redirect(
        "login"
    )
def about(request):
    return render(
        request,
        "about.html"
    )


def companies(request):
    return render(
        request,
        "companies.html"
    )


def contact(request):
    return render(
        request,
        "contact.html"
    )
def login_choice(request):
    return render(request, "login_choice.html")


def register_choice(request):
    return render(request, "register_choice.html")
