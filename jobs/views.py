from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from accounts.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from pathlib import Path
from django.db.models import Q


from .models import Application, Job, SavedJob, Notification


# =========================================================
# EMPLOYER — POST A NEW JOB
# =========================================================

@login_required
def post_job(request):

    if request.user.user_type != "employer":
        messages.error(
            request,
            "Only employers can post jobs."
        )
        return redirect("home")

    if request.method == "POST":

        title = request.POST.get("title", "").strip()
        location = request.POST.get("location", "").strip()
        description = request.POST.get("description", "").strip()
        requirements = request.POST.get("requirements", "").strip()

        if not title or not location or not description or not requirements:

            messages.error(
                request,
                "Please fill all required fields."
            )

            return render(
                request,
                "employer/post_job.html"
            )
            

        Job.objects.create(
            employer=request.user,
            title=title,
            company_name=request.POST.get("company_name", "").strip(),
            category=request.POST.get("category", "").strip(),
            job_type=request.POST.get("job_type", "").strip(),
            location=location,
            experience=request.POST.get("experience", "").strip(),
            minimum_salary=(
                request.POST.get("minimum_salary") or None
            ),
            maximum_salary=(
                request.POST.get("maximum_salary") or None
            ),
            description=description,
            requirements=requirements,
            skills=request.POST.get("skills", "").strip(),
            application_deadline=(
                request.POST.get("application_deadline") or None
            ),
            number_of_vacancies=(
                request.POST.get("vacancies") or 1
            ),
            work_mode=request.POST.get("work_mode", "").strip(),
            education_level=request.POST.get("education", "").strip(),
            benefits=request.POST.get("benefits", "").strip(),
            company_logo=request.FILES.get("company_logo"),
        )

        messages.success(
            request,
            "Job posted successfully."
        )

        return redirect("employer_dashboard")

    return render(
        request,
      "employer/post_job.html"
    )


# =========================================================
# EMPLOYER — MY JOBS
# =========================================================

@login_required
def my_jobs(request):

    if request.user.user_type != "employer":
        messages.error(
            request,
            "Only employers can access this page."
        )
        return redirect("home")

    jobs = Job.objects.filter(
        employer=request.user
    ).order_by("-created_at")

    return render(
        request,
        "employer/my-jobs.html",
        {
            "jobs": jobs
        }
    )


# =========================================================
# CANDIDATE — BROWSE JOBS
# =========================================================

def browse_jobs(request):

    jobs = Job.objects.filter(
        is_active=True
    )

    search_query = request.GET.get(
        "search",
        ""
    ).strip()

    location = request.GET.get(
        "location",
        ""
    ).strip()

    job_type = request.GET.get(
        "job_type",
        ""
    ).strip()

    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query)
            | Q(company_name__icontains=search_query)
            | Q(category__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(employer__first_name__icontains=search_query)
            | Q(employer__username__icontains=search_query)
        )

    if location:
        jobs = jobs.filter(
            location__icontains=location
        )

    if job_type:
        jobs = jobs.filter(
            job_type=job_type
        )

    jobs = jobs.order_by("-created_at")

    paginator = Paginator(
        jobs,
        10
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(
        page_number
    )

    saved_job_ids = []

    if request.user.is_authenticated and request.user.user_type == "candidate":

        saved_job_ids = SavedJob.objects.filter(
            candidate=request.user
        ).values_list(
            "job_id",
            flat=True
        )

    return render(
        request,
        "jobs.html",
        {
            "jobs": page_obj,
            "page_obj": page_obj,
            "saved_job_ids": saved_job_ids,
            "search_query": search_query,
            "selected_location": location,
            "selected_job_type": job_type,
            "jobs_count": paginator.count,
        }
    )


# =========================================================
# JOB DETAIL
# =========================================================

def job_detail(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id,
        is_active=True
    )

    already_applied = False
    is_saved = False

    if request.user.is_authenticated and request.user.user_type == "candidate":

        already_applied = Application.objects.filter(
            job=job,
            candidate=request.user
        ).exists()

        is_saved = SavedJob.objects.filter(
            job=job,
            candidate=request.user
        ).exists()

    similar_jobs = list(
        Job.objects.filter(is_active=True, category=job.category)
        .exclude(id=job.id)
        .select_related("employer")
        .order_by("-created_at")[:3]
    )
    if len(similar_jobs) < 3:
        excluded_ids = [job.id, *[item.id for item in similar_jobs]]
        similar_jobs.extend(
            Job.objects.filter(is_active=True)
            .exclude(id__in=excluded_ids)
            .select_related("employer")
            .order_by("-created_at")[: 3 - len(similar_jobs)]
        )

    return render(
    request,
    "candidate/job-detail.html",
    {
        "job": job,
        "already_applied": already_applied,
        "is_saved": is_saved,
        "similar_jobs": similar_jobs,
    }
)


# =========================================================
# CANDIDATE — APPLY FOR JOB
# =========================================================


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True)

    if request.user.user_type != "candidate":
        messages.error(request, "Only candidates can apply for jobs.")
        return redirect("job_detail", job_id=job.id)

    already_applied = Application.objects.filter(
        job=job,
        candidate=request.user
    ).exists()

    if already_applied:
        messages.error(request, "You have already applied for this job.")
        return redirect("job_detail", job_id=job.id)

    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        resume = request.FILES.get("resume")

        if not full_name or not email or not phone:
            messages.error(request, "Please fill all required fields.")
            return render(request, "apply-job.html", {"job": job, "form_data": request.POST})

        if not resume:
            messages.error(request, "Please upload your resume.")
            return render(request, "apply-job.html", {"job": job, "form_data": request.POST})

        allowed_extensions = {".pdf", ".doc", ".docx"}
        if Path(resume.name).suffix.lower() not in allowed_extensions:
            messages.error(request, "Please upload a PDF, DOC, or DOCX resume.")
            return render(request, "apply-job.html", {"job": job, "form_data": request.POST})

        if resume.size > 5 * 1024 * 1024:
            messages.error(request, "Resume file must be smaller than 5 MB.")
            return render(request, "apply-job.html", {"job": job, "form_data": request.POST})

        application = Application.objects.create(
            job=job,
            candidate=request.user,
            full_name=full_name,
            email=email,
            phone=phone,
            resume=resume
        )

        Notification.objects.create(
            employer=job.employer,
            application=application,
            title="New Job Application",
            message=f"{request.user.get_full_name() or request.user.username} applied for '{job.title}'."
        )

        messages.success(request, "Application submitted successfully.")
        return redirect("job_detail", job_id=job.id)

    # GET request - Apply form show hoga
    return render(request, "apply-job.html", {"job": job})
# =========================================================
# EMPLOYER — VIEW APPLICATIONS
# =========================================================

@login_required
def employer_applications(request):

    if request.user.user_type != "employer":
        messages.error(
            request,
            "Only employers can access this page."
        )
        return redirect("home")

    applications = Application.objects.filter(
        job__employer=request.user
    ).select_related(
        "job",
        "candidate"
    ).order_by("-applied_at")

    return render(
        request,
        "employer/employer-applications.html",
        {
            "applications": applications
        }
    )


# =========================================================
# EMPLOYER — SHORTLIST APPLICATION
# =========================================================

@login_required
@require_POST
def shortlist_application(request, application_id):

    if request.user.user_type != "employer":
        messages.error(
            request,
            "Only employers can perform this action."
        )
        return redirect("home")

    application = get_object_or_404(
        Application,
        id=application_id,
        job__employer=request.user
    )

    application.status = "shortlisted"
    application.save()
    Notification.objects.create(
    candidate=application.candidate,
    application=application,
    title="Application Shortlisted",
    message=f"Congratulations! Your application for '{application.job.title}' has been shortlisted."
)

    messages.success(
        request,
        f"{application.full_name} has been shortlisted."
    )

    return redirect("employer_applications")


# =========================================================
# EMPLOYER — REJECT APPLICATION
# =========================================================

@login_required
@require_POST
def reject_application(request, application_id):

    if request.user.user_type != "employer":
        messages.error(
            request,
            "Only employers can perform this action."
        )
        return redirect("home")

    application = get_object_or_404(
        Application,
        id=application_id,
        job__employer=request.user
    )

    application.status = "rejected"
    application.save()
    Notification.objects.create(
    candidate=application.candidate,
    application=application,
    title="Application Rejected",
    message=f"Your application for '{application.job.title}' has been rejected."
)

    messages.success(
        request,
        f"{application.full_name}'s application has been rejected."
    )

    return redirect("employer_applications")


# =========================================================
# CANDIDATE — MY APPLICATIONS
# =========================================================

@login_required
def candidate_applications(request):

    if request.user.user_type != "candidate":
        messages.error(
            request,
            "Only candidates can access this page."
        )
        return redirect("home")

    applications = Application.objects.filter(
        candidate=request.user
    ).select_related(
        "job",
        "job__employer"
    ).order_by("-applied_at")

    return render(
        request,
        "candidate-applications.html",
        {
            "applications": applications
        }
    )


# =========================================================
# CANDIDATE — SAVE OR UNSAVE JOB
# =========================================================

@login_required
def toggle_saved_job(request, job_id):

    if request.user.user_type != "candidate":
        messages.error(
            request,
            "Only candidates can save jobs."
        )
        return redirect("home")

    job = get_object_or_404(
        Job,
        id=job_id,
        is_active=True
    )

    saved_job = SavedJob.objects.filter(
        candidate=request.user,
        job=job
    ).first()

    if saved_job:

        saved_job.delete()

        messages.success(
            request,
            "Job removed from saved jobs."
        )

    else:

        SavedJob.objects.create(
            candidate=request.user,
            job=job
        )

        messages.success(
            request,
            "Job saved successfully."
        )

    next_url = request.POST.get(
        "next"
    ) or request.GET.get(
        "next"
    )

    if next_url:
        return redirect(next_url)

    return redirect("browse_jobs")


# =========================================================
# CANDIDATE — SAVED JOBS
# =========================================================

@login_required
def saved_jobs(request):

    if request.user.user_type != "candidate":
        messages.error(
            request,
            "Only candidates can access saved jobs."
        )
        return redirect("home")

    candidate_saved_jobs = SavedJob.objects.filter(
        candidate=request.user
    ).select_related(
        "job",
        "job__employer"
    ).order_by("-saved_at")

    return render(
        request,
        "saved-jobs.html",
        {
            "saved_jobs": candidate_saved_jobs
        }
    )


# =========================================================
# EMPLOYER — DELETE JOB
# =========================================================

@login_required
def delete_job(request, job_id):

    if request.user.user_type != "employer":
        messages.error(
            request,
            "Only employers can access this page."
        )
        return redirect("home")

    job = get_object_or_404(
        Job,
        id=job_id,
        employer=request.user
    )

    if request.method == "POST":

        job_title = job.title
        job.delete()

        messages.success(
            request,
            f"{job_title} has been deleted successfully."
        )

    else:

        messages.error(
            request,
            "Invalid request."
        )

    return redirect("my_jobs")


# =========================================================
# EMPLOYER — EDIT JOB
# =========================================================

@login_required
def edit_job(request, job_id):

    if request.user.user_type != "employer":
        messages.error(
            request,
            "Only employers can access this page."
        )
        return redirect("home")

    job = get_object_or_404(
        Job,
        id=job_id,
        employer=request.user
    )

    if request.method == "POST":

        title = request.POST.get(
            "title",
            ""
        ).strip()

        location = request.POST.get(
            "location",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        requirements = request.POST.get(
            "requirements",
            ""
        ).strip()

        if not title or not location or not description or not requirements:

            messages.error(
                request,
                "Please fill all required fields."
            )

            return render(
                request,
                "edit-job.html",
                {
                    "job": job
                }
            )

        job.title = title
        job.company_name = request.POST.get("company_name", job.company_name).strip()
        job.category = request.POST.get(
            "category",
            ""
        ).strip()

        job.job_type = request.POST.get(
            "job_type",
            ""
        ).strip()

        job.location = location

        job.experience = request.POST.get(
            "experience",
            ""
        ).strip()

        job.minimum_salary = (
            request.POST.get("minimum_salary") or None
        )

        job.maximum_salary = (
            request.POST.get("maximum_salary") or None
        )

        job.description = description
        job.requirements = requirements

        job.skills = request.POST.get(
            "skills",
            ""
        ).strip()

        job.application_deadline = (
            request.POST.get("application_deadline") or None
        )

        job.number_of_vacancies = (
            request.POST.get("vacancies") or 1
        )

        job.work_mode = request.POST.get(
            "work_mode",
            ""
        ).strip()

        job.education_level = request.POST.get(
            "education",
            ""
        ).strip()

        job.benefits = request.POST.get(
            "benefits",
            ""
        ).strip()

        company_logo = request.FILES.get(
            "company_logo"
        )

        if company_logo:
            job.company_logo = company_logo

        job.save()

        messages.success(
            request,
            "Job updated successfully."
        )

        return redirect("my_jobs")

    return render(
        request,
                "edit-job.html",
        {
            "job": job
        }
    )


# =========================================================
# EMPLOYER — OPEN OR CLOSE JOB
# =========================================================

@login_required
def toggle_job_status(request, job_id):

    if request.user.user_type != "employer":
        messages.error(
            request,
            "Only employers can access this page."
        )
        return redirect("home")

    job = get_object_or_404(
        Job,
        id=job_id,
        employer=request.user
    )

    if request.method == "POST":

        job.is_active = not job.is_active
        job.save()

        if job.is_active:

            messages.success(
                request,
                "Job opened successfully."
            )

        else:

            messages.success(
                request,
                "Job closed successfully."
            )

    else:

        messages.error(
            request,
            "Invalid request."
        )

    return redirect("my_jobs")



@login_required
def search_candidates(request):

    if request.user.user_type != "employer":
        messages.error(request, "Only employers can browse candidates.")
        return redirect("home")

    candidates = User.objects.filter(user_type="candidate")

    return render(
        request,
        "employer/search_candidates.html",
        {
            "candidates": candidates
        }
    )

@login_required
def employer_notifications(request):

    if request.user.user_type != "employer":
        messages.error(request, "Only employers can access notifications.")
        return redirect("home")

    notifications = Notification.objects.filter(
    employer=request.user
).select_related(
    "application",
    "application__candidate",
    "application__job"
).order_by("-created_at")

    return render(
        request,
        "employer/notifications.html",
        {
            "notifications": notifications
        }
    )
@login_required
def mark_notification_read(request, id):

    notification = get_object_or_404(
        Notification,
        id=id,
        employer=request.user
    )

    notification.is_read = True
    notification.save()

    return redirect("employer_notifications")


@login_required
@require_POST
def mark_all_notifications_read(request):

    if request.user.user_type != "employer":
        messages.error(request, "Only employers can update notifications.")
        return redirect("home")

    Notification.objects.filter(
        employer=request.user,
        is_read=False
    ).update(is_read=True)

    return redirect("employer_notifications")


@login_required
def delete_notification(request, id):

    notification = get_object_or_404(
        Notification,
        id=id,
        employer=request.user
    )

    if request.method == "POST":

        notification.delete()

    return redirect(
        "employer_notifications"
    )


@login_required
def notification_count(request):

    count = Notification.objects.filter(
        employer=request.user,
        is_read=False
    ).count()

    return JsonResponse(
        {
            "count": count
        }
    )
    
