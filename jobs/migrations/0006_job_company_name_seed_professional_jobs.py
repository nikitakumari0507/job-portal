from django.db import migrations, models


JOBS = [
    {
        "title": "Frontend Developer", "company_name": "Aurora Tech", "category": "Software Development",
        "job_type": "full_time", "location": "Bangalore", "experience": "0–2 years",
        "minimum_salary": 400000, "maximum_salary": 650000, "work_mode": "Hybrid",
        "education_level": "Bachelor's degree", "number_of_vacancies": 3,
        "skills": "HTML, CSS, JavaScript, React",
        "description": "Build responsive, accessible web experiences for modern digital products.",
        "requirements": "Strong frontend fundamentals, attention to detail, and familiarity with version control.",
        "benefits": "Flexible hours, learning budget, health insurance", "company_logo": "company_logos/aurora-careers.svg",
    },
    {
        "title": "Python Django Developer", "company_name": "CodeCraft Labs", "category": "Software Development",
        "job_type": "full_time", "location": "Kolkata", "experience": "Fresher–2 years",
        "minimum_salary": 450000, "maximum_salary": 750000, "work_mode": "Hybrid",
        "education_level": "BCA, B.Tech or equivalent", "number_of_vacancies": 2,
        "skills": "Python, Django, REST API, PostgreSQL",
        "description": "Develop secure Django applications and reliable backend services for growing products.",
        "requirements": "Good Python knowledge, database fundamentals, and an understanding of web APIs.",
        "benefits": "Mentorship, certification support, health insurance", "company_logo": "company_logos/codecraft.svg",
    },
    {
        "title": "Operations Assistant", "company_name": "HomeWise Services", "category": "Operations",
        "job_type": "part_time", "location": "Bangalore", "experience": "Fresher",
        "minimum_salary": 180000, "maximum_salary": 260000, "work_mode": "On-site",
        "education_level": "12th pass or graduate", "number_of_vacancies": 4,
        "skills": "Coordination, communication, time management",
        "description": "Support daily service operations, scheduling, documentation, and customer coordination.",
        "requirements": "Professional communication, reliability, and basic computer knowledge.",
        "benefits": "Flexible shifts, performance bonus", "company_logo": "company_logos/homewise.svg",
    },
    {
        "title": "Data Analyst", "company_name": "Quantix Analytics", "category": "Data & Analytics",
        "job_type": "full_time", "location": "Pune", "experience": "0–2 years",
        "minimum_salary": 500000, "maximum_salary": 850000, "work_mode": "Hybrid",
        "education_level": "Bachelor's degree", "number_of_vacancies": 3,
        "skills": "Excel, SQL, Python, Power BI",
        "description": "Transform business data into clear reports, dashboards, and actionable insights.",
        "requirements": "Analytical thinking, SQL fundamentals, and experience creating data visualizations.",
        "benefits": "Learning budget, hybrid work, health coverage", "company_logo": "company_logos/quantix.svg",
    },
    {
        "title": "UI/UX Designer", "company_name": "PixelWave Studio", "category": "Design",
        "job_type": "full_time", "location": "Hyderabad", "experience": "1–3 years",
        "minimum_salary": 420000, "maximum_salary": 700000, "work_mode": "Hybrid",
        "education_level": "Graduate or design certification", "number_of_vacancies": 2,
        "skills": "Figma, wireframing, prototyping, user research",
        "description": "Design intuitive user journeys and polished interfaces for web and mobile products.",
        "requirements": "A strong portfolio, visual design fundamentals, and collaborative working skills.",
        "benefits": "Creative workshops, flexible schedule, device allowance", "company_logo": "company_logos/pixelwave.svg",
    },
    {
        "title": "Backend Developer", "company_name": "Nexora Systems", "category": "Software Development",
        "job_type": "full_time", "location": "Noida", "experience": "1–3 years",
        "minimum_salary": 600000, "maximum_salary": 950000, "work_mode": "Remote",
        "education_level": "Bachelor's degree", "number_of_vacancies": 2,
        "skills": "Python, APIs, PostgreSQL, Docker",
        "description": "Create scalable backend services, integrations, and data-driven application features.",
        "requirements": "Experience with server-side development, relational databases, and clean code practices.",
        "benefits": "Remote work, internet allowance, annual bonus", "company_logo": "company_logos/nexora.svg",
    },
    {
        "title": "Digital Marketing Executive", "company_name": "BrightReach Media", "category": "Marketing",
        "job_type": "full_time", "location": "Mumbai", "experience": "Fresher–2 years",
        "minimum_salary": 300000, "maximum_salary": 520000, "work_mode": "Hybrid",
        "education_level": "Graduate", "number_of_vacancies": 3,
        "skills": "SEO, social media, content, analytics",
        "description": "Plan and optimize digital campaigns across search, social media, and content channels.",
        "requirements": "Strong communication, creative thinking, and familiarity with digital marketing metrics.",
        "benefits": "Campaign incentives, training, flexible hours", "company_logo": "company_logos/brightreach.svg",
    },
    {
        "title": "HR Recruiter", "company_name": "PeopleFirst HR", "category": "Human Resources",
        "job_type": "full_time", "location": "Ranchi", "experience": "Fresher–2 years",
        "minimum_salary": 280000, "maximum_salary": 480000, "work_mode": "On-site",
        "education_level": "Graduate", "number_of_vacancies": 2,
        "skills": "Recruitment, communication, screening, MS Office",
        "description": "Coordinate sourcing, candidate screening, interviews, and recruitment documentation.",
        "requirements": "Clear communication, organizational ability, and a professional approach to candidates.",
        "benefits": "Performance incentives, structured training", "company_logo": "company_logos/peoplefirst.svg",
    },
    {
        "title": "Cloud Support Associate", "company_name": "SkyGrid Cloud", "category": "IT Support",
        "job_type": "full_time", "location": "Chennai", "experience": "0–2 years",
        "minimum_salary": 420000, "maximum_salary": 680000, "work_mode": "Remote",
        "education_level": "BCA, B.Sc IT or equivalent", "number_of_vacancies": 4,
        "skills": "Linux, networking, cloud fundamentals, troubleshooting",
        "description": "Help customers resolve cloud platform, access, networking, and deployment issues.",
        "requirements": "Technical troubleshooting skills and willingness to work in rotational support shifts.",
        "benefits": "Remote work, cloud certifications, shift allowance", "company_logo": "company_logos/skygrid.svg",
    },
    {
        "title": "Customer Success Executive", "company_name": "CareBridge Solutions", "category": "Customer Success",
        "job_type": "full_time", "location": "Gurugram", "experience": "Fresher–2 years",
        "minimum_salary": 320000, "maximum_salary": 550000, "work_mode": "Hybrid",
        "education_level": "Graduate", "number_of_vacancies": 5,
        "skills": "Communication, CRM, problem solving, customer service",
        "description": "Guide customers through onboarding, product adoption, support, and account success.",
        "requirements": "Empathy, professional communication, and the ability to manage customer relationships.",
        "benefits": "Incentives, transport support, wellness program", "company_logo": "company_logos/carebridge.svg",
    },
]


def seed_jobs(apps, schema_editor):
    Job = apps.get_model("jobs", "Job")
    User = apps.get_model("accounts", "User")
    employer = User.objects.filter(user_type="employer").first()
    if not employer:
        return

    existing = list(Job.objects.filter(is_active=True).order_by("id")[:3])
    for index, data in enumerate(JOBS):
        values = {**data, "employer": employer, "is_active": True}
        if index < len(existing):
            job = existing[index]
            for field, value in values.items():
                setattr(job, field, value)
            job.save()
        else:
            Job.objects.update_or_create(
                title=data["title"], company_name=data["company_name"],
                defaults=values,
            )


def unseed_jobs(apps, schema_editor):
    Job = apps.get_model("jobs", "Job")
    Job.objects.filter(company_name__in=[item["company_name"] for item in JOBS[3:]]).delete()


class Migration(migrations.Migration):
    dependencies = [("jobs", "0005_notification_candidate_and_more")]
    operations = [
        migrations.AddField(
            model_name="job",
            name="company_name",
            field=models.CharField(blank=True, max_length=180),
        ),
        migrations.RunPython(seed_jobs, unseed_jobs),
    ]
