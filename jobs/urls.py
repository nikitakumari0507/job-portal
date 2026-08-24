from django.urls import path
from . import views

urlpatterns = [
    path('post-job/', views.post_job, name='post_job'),

    path(
        "employer/my-jobs/",
        views.my_jobs,
        name='my_jobs'
    ),
    path('browse/', views.browse_jobs, name='browse_jobs'),
    
    path(
    'apply/<int:job_id>/',
    views.apply_job,
    name='apply_job'
),
    path(
    "employer-applications/",
    views.employer_applications,
    name="employer_applications"
),
    path(
    "application/<int:application_id>/shortlist/",
    views.shortlist_application,
    name="shortlist_application"
),

path(
    "application/<int:application_id>/reject/",
    views.reject_application,
    name="reject_application"
),
path(
    "candidate-applications/",
    views.candidate_applications,
    name="candidate_applications"
),
path(
    "save-job/<int:job_id>/",
    views.toggle_saved_job,
    name="toggle_saved_job"
),
path(
    "saved-jobs/",
    views.saved_jobs,
    name="saved_jobs"
),
path(
    "delete/<int:job_id>/",
    views.delete_job,
    name="delete_job"
),
path(
    "edit/<int:job_id>/",
    views.edit_job,
    name="edit_job"
),

path(
    "toggle-status/<int:job_id>/",
    views.toggle_job_status,
    name="toggle_job_status"
),
path(
    "search-candidates/",
    views.search_candidates,
    name="search_candidates",
),
path(
    "job/<int:job_id>/",
    views.job_detail,
    name="job_detail",
),

path(
    "notifications/read/<int:id>/",
    views.mark_notification_read,
    name="mark_notification_read"
),
path(
    "employer/notifications/",
    views.employer_notifications,
    name="employer_notifications",
),
path(
    "employer/notifications/read-all/",
    views.mark_all_notifications_read,
    name="mark_all_notifications_read",
),

path(
    "notifications/delete/<int:id>/",
    views.delete_notification,
    name="delete_notification"
),
]
