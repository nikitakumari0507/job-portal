const searchInput = document.getElementById("jobSearch");
const locationFilter = document.getElementById("locationFilter");
const typeFilter = document.getElementById("typeFilter");

const jobCards = document.querySelectorAll(".job-card");
const noJobs = document.getElementById("noJobsMessage");

function filterJobs(){

let visible = 0;

jobCards.forEach(card=>{

const title = card.dataset.title.toLowerCase();
const location = card.dataset.location;
const type = card.dataset.type;

const searchValue = searchInput.value.toLowerCase();
const locationValue = locationFilter.value;
const typeValue = typeFilter.value;

const matchSearch = title.includes(searchValue);
const matchLocation = locationValue==="" || location===locationValue;
const matchType = typeValue==="" || type===typeValue;

if(matchSearch && matchLocation && matchType){

card.style.display="flex";
visible++;

}
else{

card.style.display="none";

}

});

if(visible===0){

noJobs.style.display="block";

}
else{

noJobs.style.display="none";

}

}

if(searchInput && locationFilter && typeFilter){

    searchInput.addEventListener("keyup",filterJobs);

    locationFilter.addEventListener("change",filterJobs);

    typeFilter.addEventListener("change",filterJobs);

}
const applyModal = document.getElementById("applyModal");
const selectedJobTitle = document.getElementById("selectedJobTitle");
const applyForm = document.getElementById("applyForm");
const applicationMessage = document.getElementById("applicationMessage");

function openApplyModal(jobTitle) {
    selectedJobTitle.textContent = jobTitle;
    applicationMessage.textContent = "";
    applyModal.classList.add("active");
}

function closeApplyModal() {
    applyModal.classList.remove("active");
    applyForm.reset();
    applicationMessage.textContent = "";
}

if(applyForm && applyModal){

    applyForm.addEventListener("submit", function(event) {

        event.preventDefault();

        applicationMessage.textContent =
        "Application submitted successfully!";

        setTimeout(function(){

            closeApplyModal();

        },1800);

    });

    applyModal.addEventListener("click", function(event){

        if(event.target===applyModal){

            closeApplyModal();

        }

    });

}
function toggleSaveJob(button) {
    const icon = button.querySelector("i");

    button.classList.toggle("saved");

    if (button.classList.contains("saved")) {
        icon.classList.remove("bi-heart");
        icon.classList.add("bi-heart-fill");
    } else {
        icon.classList.remove("bi-heart-fill");
        icon.classList.add("bi-heart");
    }
}
const toggleRegisterPassword = document.getElementById("toggleRegisterPassword");
const registerPassword = document.getElementById("registerPassword");
const confirmPassword = document.getElementById("confirmPassword");

if (toggleRegisterPassword && registerPassword) {
    toggleRegisterPassword.addEventListener("click", function () {

        const isPassword =
            registerPassword.type === "password";

        registerPassword.type =
            isPassword ? "text" : "password";

        this.classList.toggle("bi-eye-fill");
        this.classList.toggle("bi-eye-slash-fill");
    });
}


/* ===========================
   LOGIN PAGE
=========================== */

document.addEventListener("DOMContentLoaded", function () {

    const passwordInput = document.getElementById("password");
    const eyeIcon = document.getElementById("togglePassword");

    if (passwordInput && eyeIcon) {

        eyeIcon.addEventListener("click", function () {

            if (passwordInput.type === "password") {
                passwordInput.type = "text";
                eyeIcon.classList.remove("bi-eye-fill");
                eyeIcon.classList.add("bi-eye-slash-fill");
            } else {
                passwordInput.type = "password";
                eyeIcon.classList.remove("bi-eye-slash-fill");
                eyeIcon.classList.add("bi-eye-fill");
            }

        });

    }

});
/* =================================
   PREMIUM FRONTEND FEATURES
================================= */

document.addEventListener("DOMContentLoaded", function () {

   

   
    /* SCROLL TO TOP */

    const scrollTopBtn = document.getElementById("scrollTopBtn");

    if (scrollTopBtn) {

        window.addEventListener("scroll", function () {

            if (window.scrollY > 350) {
                scrollTopBtn.classList.add("show");
            } else {
                scrollTopBtn.classList.remove("show");
            }
        });

        scrollTopBtn.addEventListener("click", function () {

            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        });
    }
    /* =================================
   EMPLOYER ANALYTICS CHART
================================= */

const analyticsCanvas =
    document.getElementById("hiringAnalyticsChart");

const analyticsPeriod =
    document.getElementById("analyticsPeriod");

let hiringChart = null;

const analyticsData = {

    6:{

        labels:[
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul"
        ],

        applications:[
            140,
            185,
            220,
            260,
            295,
            326
        ],

        jobs:[
            8,
            11,
            13,
            16,
            20,
            24
        ]

    },

    12:{

        labels:[
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul"
        ],

        applications:[
            72,
            88,
            102,
            120,
            135,
            128,
            140,
            185,
            220,
            260,
            295,
            326
        ],

        jobs:[
            3,
            4,
            5,
            6,
            7,
            7,
            8,
            11,
            13,
            16,
            20,
            24
        ]

    }

};

function createHiringChart(period){

    if(!analyticsCanvas || typeof Chart==="undefined"){
        return;
    }

    if(hiringChart){
        hiringChart.destroy();
    }

    const chartData = analyticsData[period];

    hiringChart = new Chart(
        analyticsCanvas,
        {

            type:"line",

            data:{

                labels:chartData.labels,

                datasets:[

                    {

                        label:"Applications",

                        data:chartData.applications,

                        borderColor:"#2563EB",

                        backgroundColor:"rgba(37,99,235,.12)",

                        fill:true,

                        tension:.4,

                        borderWidth:3,

                        pointRadius:4,

                        pointBackgroundColor:"#ffffff",

                        pointBorderColor:"#2563EB",

                        pointBorderWidth:2,

                        yAxisID:"y"

                    },

                    {

                        label:"Jobs Posted",

                        data:chartData.jobs,

                        borderColor:"#38BDF8",

                        backgroundColor:"transparent",

                        fill:false,

                        tension:.4,

                        borderWidth:3,

                        pointRadius:4,

                        pointBackgroundColor:"#ffffff",

                        pointBorderColor:"#38BDF8",

                        pointBorderWidth:2,

                        yAxisID:"y1"

                    }

                ]

            },

            options:{
                                responsive:true,

                maintainAspectRatio:false,

                interaction:{
                    mode:"index",
                    intersect:false
                },

                plugins:{

                    legend:{

                        position:"top",

                        labels:{

                            usePointStyle:true,

                            color:"#64748B",

                            font:{
                                family:"Poppins",
                                size:12
                            }

                        }

                    },

                    tooltip:{

                        backgroundColor:"#0B1F4D",

                        titleColor:"#ffffff",

                        bodyColor:"#ffffff",

                        padding:12,

                        cornerRadius:10

                    }

                },

                scales:{

                    x:{

                        grid:{
                            display:false
                        },

                        ticks:{
                            color:"#64748B"
                        }

                    },

                    y:{

                        beginAtZero:true,

                        position:"left",

                        ticks:{
                            color:"#64748B"
                        },

                        grid:{
                            color:"rgba(148,163,184,.20)"
                        }

                    },

                    y1:{

                        beginAtZero:true,

                        position:"right",

                        grid:{
                            drawOnChartArea:false
                        },

                        ticks:{
                            color:"#64748B"
                        }

                    }

                }

            }

        }

    );

}

if (analyticsCanvas) {
    createHiringChart("6");
}

if (analyticsPeriod) {

    analyticsPeriod.addEventListener(
        "change",
        function () {

            createHiringChart(this.value);

        }
    );


}
        /* =================================
       HIRING CALENDAR
    ================================= */

    const calendarDays =
        document.getElementById("calendarDays");

    const calendarMonthTitle =
        document.getElementById("calendarMonthTitle");

    const calendarPrevBtn =
        document.getElementById("calendarPrevBtn");

    const calendarNextBtn =
        document.getElementById("calendarNextBtn");

    const calendarTodayBtn =
        document.getElementById("calendarTodayBtn");

    const today = new Date();

    let calendarDate =
        new Date(
            today.getFullYear(),
            today.getMonth(),
            1
        );

    const interviewDates = [8, 14, 21, 26];
    const deadlineDates = [11, 18, 29];

    function renderHiringCalendar() {

        if (!calendarDays || !calendarMonthTitle) {
            return;
        }

        calendarDays.innerHTML = "";

        const year =
            calendarDate.getFullYear();

        const month =
            calendarDate.getMonth();

        const firstDay =
            new Date(year, month, 1).getDay();

        const daysInMonth =
            new Date(year, month + 1, 0).getDate();

        const daysInPreviousMonth =
            new Date(year, month, 0).getDate();

        calendarMonthTitle.textContent =
            calendarDate.toLocaleDateString(
                "en-US",
                {
                    month:"long",
                    year:"numeric"
                }
            );

        for (let i = firstDay - 1; i >= 0; i--) {

            const dayButton =
                document.createElement("button");

            dayButton.type = "button";

            dayButton.className =
                "calendar-day other-month";

            dayButton.textContent =
                daysInPreviousMonth - i;

            calendarDays.appendChild(dayButton);

        }

        for (let day = 1; day <= daysInMonth; day++) {

            const dayButton =
                document.createElement("button");

            dayButton.type = "button";
            dayButton.className = "calendar-day";
            dayButton.textContent = day;

            const isToday =
                day === today.getDate()
                && month === today.getMonth()
                && year === today.getFullYear();

            if (isToday) {
                dayButton.classList.add("today");
            }

            if (interviewDates.includes(day)) {
                dayButton.classList.add("has-interview");
                dayButton.title = "Interview scheduled";
            }

            if (deadlineDates.includes(day)) {
                dayButton.classList.add("has-deadline");
                dayButton.title = "Hiring deadline";
            }

            calendarDays.appendChild(dayButton);

        }

        const totalCells =
            firstDay + daysInMonth;

        const remainingCells =
            totalCells % 7 === 0
                ? 0
                : 7 - (totalCells % 7);

        for (
            let day = 1;
            day <= remainingCells;
            day++
        ) {

            const dayButton =
                document.createElement("button");

            dayButton.type = "button";

            dayButton.className =
                "calendar-day other-month";

            dayButton.textContent = day;

            calendarDays.appendChild(dayButton);

        }

    }

    if (calendarPrevBtn) {

        calendarPrevBtn.addEventListener(
            "click",
            function () {

                calendarDate.setMonth(
                    calendarDate.getMonth() - 1
                );

                renderHiringCalendar();

            }
        );

    }

    if (calendarNextBtn) {

        calendarNextBtn.addEventListener(
            "click",
            function () {

                calendarDate.setMonth(
                    calendarDate.getMonth() + 1
                );

                renderHiringCalendar();

            }
        );

    }

    if (calendarTodayBtn) {

        calendarTodayBtn.addEventListener(
            "click",
            function () {

                calendarDate =
                    new Date(
                        today.getFullYear(),
                        today.getMonth(),
                        1
                    );

                renderHiringCalendar();

            }
        );

    }

    renderHiringCalendar();
    /* RESUME UPLOAD FIX */

const resumeUpdateBtn =
    document.getElementById("resumeUpdateBtn");

const resumeFileInput =
    document.getElementById("resumeFileInput");

const resumeCard =
    document.querySelector(".resume-card");

if (
    resumeUpdateBtn &&
    resumeFileInput &&
    resumeCard
) {

    resumeUpdateBtn.addEventListener(
        "click",
        function () {

            resumeFileInput.click();

        }
    );

    resumeFileInput.addEventListener(
        "change",
        function () {

            if (!this.files || !this.files.length) {
                return;
            }

            const selectedFile = this.files[0];

            const allowedExtensions =
                ["pdf", "doc", "docx"];

            const extension =
                selectedFile.name
                    .split(".")
                    .pop()
                    .toLowerCase();

            if (!allowedExtensions.includes(extension)) {

                alert(
                    "Please select a PDF, DOC or DOCX file."
                );

                this.value = "";

                return;
            }

            const resumeTitle =
                resumeCard.querySelector("h3");

            const resumeStatus =
                resumeCard.querySelector("span");

            if (resumeTitle) {

                resumeTitle.textContent =
                    selectedFile.name;

            }

            if (resumeStatus) {

                resumeStatus.textContent =
                    "Resume updated successfully";

            }

        }
    );

}

/* DOMContentLoaded CLOSE */
/* CANDIDATE JOB BUTTON TOAST */

function showCandidateToast(message) {

    let toast =
        document.querySelector(".candidate-toast");

    if (!toast) {

        toast = document.createElement("div");
        toast.className = "candidate-toast";

        toast.innerHTML = `
            <i class="bi bi-check-circle-fill"></i>
            <p></p>
        `;

        document.body.appendChild(toast);

    }

    const toastText = toast.querySelector("p");

    if (toastText) {
        toastText.textContent = message;
    }

    toast.classList.add("show");

    clearTimeout(window.candidateToastTimer);

    window.candidateToastTimer =
        setTimeout(function () {

            toast.classList.remove("show");

        }, 2200);
}

const candidateJobButtons =
    document.querySelectorAll(
        ".candidate-apply-btn"
    );

candidateJobButtons.forEach(function (button) {

    button.addEventListener(
        "click",
        function () {

            showCandidateToast(
                "Opening job details..."
            );

        }
    );

});
/* =================================
   MOBILE SIDEBAR CLOSE
================================= */

const candidateSidebar =
    document.getElementById("candidateSidebar");

const candidateMenuButton =
    document.getElementById("candidateMenuBtn");

document.addEventListener("click", function (event) {

    if (
        window.innerWidth > 991 ||
        !candidateSidebar
    ) {
        return;
    }

    if (
        candidateSidebar.classList.contains("sidebar-open") &&
        !candidateSidebar.contains(event.target) &&
        candidateMenuButton &&
        !candidateMenuButton.contains(event.target)
    ) {

        candidateSidebar.classList.remove("sidebar-open");

    }
/* COMPANY LOGO UPLOAD */

const companyLogoUploadBtn =
    document.getElementById("companyLogoUploadBtn");

const companyLogoInput =
    document.getElementById("companyLogoInput");

const companyLogoPreview =
    document.getElementById("companyLogoPreview");

const livePreviewLogo =
    document.querySelector(".post-job-preview-logo");

if (
    companyLogoUploadBtn &&
    companyLogoInput
) {

    companyLogoUploadBtn.addEventListener(
        "click",
        function () {

            companyLogoInput.click();

        }
    );

    companyLogoInput.addEventListener(
        "change",
        function () {

            if (!this.files || !this.files.length) {
                return;
            }

            const file = this.files[0];

            const allowedTypes = [
                "image/png",
                "image/jpeg"
            ];

            if (!allowedTypes.includes(file.type)) {

                showPostJobToast(
                    "Please select a PNG or JPG image.",
                    "error"
                );

                this.value = "";

                return;
            }

            if (file.size > 2 * 1024 * 1024) {

                showPostJobToast(
                    "Logo size must be less than 2 MB.",
                    "error"
                );

                this.value = "";

                return;
            }

            const imageURL =
                URL.createObjectURL(file);

            if (companyLogoPreview) {

                companyLogoPreview.innerHTML = `
                    <img
                        src="${imageURL}"
                        alt="Company Logo"
                    >
                `;

            }

            if (livePreviewLogo) {

                livePreviewLogo.innerHTML = `
                    <img
                        src="${imageURL}"
                        alt="Company Logo"
                    >
                `;

            }

            showPostJobToast(
                "Company logo updated."
            );

        }
    );

}
});

});
/* PROFILE PHOTO UPLOAD */

document.addEventListener("DOMContentLoaded", function () {

    const profileInput =
        document.getElementById("profile_image");

    const profileUploadText =
        document.getElementById("profile-upload-text");

    if (!profileInput || !profileUploadText) {
        return;
    }

    profileInput.addEventListener("change", function () {

        if (this.files && this.files.length > 0) {

            profileUploadText.textContent =
                this.files[0].name;

        } else {

            profileUploadText.textContent =
                "Choose Profile Photo";

        }

    });

});
document.addEventListener("DOMContentLoaded", function () {

    const profileInput =
        document.getElementById("profile_image");

    const profileUploadText =
        document.getElementById("profile-upload-text");

    const profileUploadStatus =
        document.getElementById("profile-upload-status");

    if (
        !profileInput ||
        !profileUploadText ||
        !profileUploadStatus
    ) {
        return;
    }

    profileInput.addEventListener("change", function () {

        if (this.files && this.files.length > 0) {

            const selectedFile = this.files[0];

            profileUploadText.textContent =
                selectedFile.name;

            profileUploadStatus.textContent =
                "✓ Profile photo selected";

            profileUploadStatus.classList.add("show");

        } else {

            profileUploadText.textContent =
                "Choose Profile Photo";

            profileUploadStatus.textContent = "";

            profileUploadStatus.classList.remove("show");

        }

    });

});