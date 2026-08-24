from django.db import models
from django.conf import settings



class Job(models.Model):

    JOB_TYPES = (
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
        ("internship", "Internship"),
        ("contract", "Contract"),
        ("remote", "Remote"),
    )

    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posted_jobs"
    )
    

    title = models.CharField(max_length=200)

    company_name = models.CharField(
        max_length=180,
        blank=True
    )

    category = models.CharField(
        max_length=100,
        blank=True
    )

    job_type = models.CharField(
        max_length=20,
        choices=JOB_TYPES
    )

    location = models.CharField(max_length=150)

    experience = models.CharField(
        max_length=100,
        blank=True
    )

    minimum_salary = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    maximum_salary = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    description = models.TextField()

    requirements = models.TextField()

    skills = models.CharField(
        max_length=500,
        blank=True
    )

    application_deadline = models.DateField(
        blank=True,
        null=True
    )

    number_of_vacancies = models.PositiveIntegerField(
        default=1
    )

    work_mode = models.CharField(
        max_length=50,
        blank=True
    )

    education_level = models.CharField(
        max_length=100,
        blank=True
    )

    benefits = models.CharField(
        max_length=500,
        blank=True
    )

    company_logo = models.ImageField(
        upload_to="company_logos/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    
class Application(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applications"
    )

    candidate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_applications"
    )

    full_name = models.CharField(max_length=150)

    email = models.EmailField()

    phone = models.CharField(max_length=20)

    resume = models.FileField(
        upload_to="resumes/"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            "job",
            "candidate"
        )

    def __str__(self):
        return f"{self.full_name} - {self.job.title}"


class SavedJob(models.Model):

    candidate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="saved_jobs"
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="saved_by_candidates"
    )

    saved_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = (
            "candidate",
            "job"
        )

    def __str__(self):
        return f"{self.candidate.username} - {self.job.title}"


class Notification(models.Model):

    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=True,
        blank=True
    )

    candidate = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="candidate_notifications",
        null=True,
        blank=True
    )

    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    title = models.CharField(max_length=200)

    message = models.TextField()

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
