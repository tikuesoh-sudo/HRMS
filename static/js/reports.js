// static/js/reports.js

document.addEventListener("DOMContentLoaded", function () {

    const sidebar = document.getElementById("sidebar");
    const sidebarToggle = document.getElementById("sidebarToggle");

    /* =========================
       SIDEBAR
    ========================= */

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener("click", function () {
            sidebar.classList.toggle("show");
        });
    }

    document.addEventListener("click", function (event) {
        if (!sidebar || !sidebarToggle) {
            return;
        }

        if (
            window.innerWidth <= 992 &&
            sidebar.classList.contains("show") &&
            !sidebar.contains(event.target) &&
            !sidebarToggle.contains(event.target)
        ) {
            sidebar.classList.remove("show");
        }
    });


    /* =========================
       STAT CARD ANIMATION
    ========================= */

    const statCards = document.querySelectorAll(".stat-card");

    statCards.forEach(function (card, index) {
        card.style.opacity = "0";
        card.style.transform = "translateY(15px)";

        setTimeout(function () {
            card.style.transition = "opacity 0.4s ease, transform 0.4s ease";
            card.style.opacity = "1";
            card.style.transform = "translateY(0)";
        }, index * 80);
    });


    /* =========================
       REPORT CARD ANIMATION
    ========================= */

    const reportCards = document.querySelectorAll(".report-card");

    reportCards.forEach(function (card, index) {
        card.style.opacity = "0";
        card.style.transform = "translateY(12px)";

        setTimeout(function () {
            card.style.transition = "opacity 0.4s ease, transform 0.4s ease";
            card.style.opacity = "1";
            card.style.transform = "translateY(0)";
        }, 250 + (index * 70));
    });


    /* =========================
       PROGRESS BAR ANIMATION
    ========================= */

    const progressBars = document.querySelectorAll(
        ".progress-bar, .rate-fill"
    );

    progressBars.forEach(function (bar) {
        const targetWidth = bar.style.width;

        bar.style.width = "0%";

        setTimeout(function () {
            bar.style.transition = "width 0.8s ease";
            bar.style.width = targetWidth;
        }, 500);
    });


    /* =========================
       PRINT REPORT
    ========================= */

    const printButton = document.querySelector(".report-print-btn");

    if (printButton) {
        printButton.addEventListener("click", function () {
            window.print();
        });
    }

});