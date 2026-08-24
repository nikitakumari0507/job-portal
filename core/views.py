from django.shortcuts import render
from django.contrib.auth import get_user_model
from jobs.models import Job


def home(request):
    featured_jobs = Job.objects.filter(is_active=True).select_related("employer").order_by("id")[:3]
    User = get_user_model()
    return render(request, "index.html", {
        "featured_jobs": featured_jobs,
        "active_jobs_count": Job.objects.filter(is_active=True).count(),
        "employers_count": User.objects.filter(user_type="employer").count(),
        "candidates_count": User.objects.filter(user_type="candidate").count(),
    })

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
