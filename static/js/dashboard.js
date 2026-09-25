/* =========================================
   HRMS DASHBOARD JAVASCRIPT
========================================= */

document.addEventListener("DOMContentLoaded", function () {

    /* =====================================
       SIDEBAR TOGGLE
    ===================================== */

    const sidebar = document.querySelector(".sidebar");
    const toggleButton = document.querySelector(".sidebar-toggle");

    if (toggleButton && sidebar) {
        toggleButton.addEventListener("click", function () {
            sidebar.classList.toggle("show");
        });
    }


    /* =====================================
       CLOSE SIDEBAR WHEN CLICKING OUTSIDE
    ===================================== */

    document.addEventListener("click", function (event) {

        if (!sidebar || !toggleButton) return;

        const clickedOutside =
            !sidebar.contains(event.target) &&
            !toggleButton.contains(event.target);

        if (
            clickedOutside &&
            window.innerWidth <= 992 &&
            sidebar.classList.contains("show")
        ) {
            sidebar.classList.remove("show");
        }
    });


    /* =====================================
       CURRENT DATE
    ===================================== */

    const dateElement = document.getElementById("currentDate");

    if (dateElement) {

        const today = new Date();

        const options = {
            weekday: "long",
            day: "numeric",
            month: "long",
            year: "numeric"
        };

        dateElement.textContent =
            today.toLocaleDateString("en-GB", options);
    }


    /* =====================================
       PAYROLL CHART
    ===================================== */

    const chartCanvas =
        document.getElementById("payrollChart");

    if (chartCanvas && typeof Chart !== "undefined") {

        const ctx = chartCanvas.getContext("2d");

        new Chart(ctx, {

            type: "line",

            data: {

                labels: [
                    "Jan",
                    "Feb",
                    "Mar",
                    "Apr",
                    "May",
                    "Jun",
                    "Jul",
                    "Aug",
                    "Sep",
                    "Oct",
                    "Nov",
                    "Dec"
                ],

                datasets: [
                    {
                        label: "Payroll (XAF)",

                        data: [
                            7.5,
                            9.2,
                            10.8,
                            12.4,
                            14.1,
                            15.2,
                            16.8,
                            17.4,
                            18.6,
                            19.5,
                            20.7,
                            22.1
                        ],

                        borderWidth: 3,

                        tension: 0.4,

                        fill: true,

                        backgroundColor:
                            "rgba(37, 99, 235, 0.08)",

                        borderColor:
                            "#2563eb",

                        pointBackgroundColor:
                            "#2563eb",

                        pointBorderColor:
                            "#ffffff",

                        pointBorderWidth: 2,

                        pointRadius: 4,

                        pointHoverRadius: 6
                    }
                ]
            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                interaction: {
                    intersect: false,
                    mode: "index"
                },

                plugins: {

                    legend: {
                        display: false
                    },

                    tooltip: {
                        backgroundColor: "#0f172a",

                        titleColor: "#ffffff",

                        bodyColor: "#ffffff",

                        padding: 12,

                        cornerRadius: 8,

                        displayColors: false,

                        callbacks: {

                            label: function (context) {

                                return " Payroll: XAF"
                                    + context.parsed.y
                                    + "M";
                            }
                        }
                    }
                },

                scales: {

                    y: {

                        beginAtZero: true,

                        grid: {
                            color: "#eef2f7"
                        },

                        ticks: {

                            color: "#64748b",

                            font: {
                                size: 10
                            },

                            callback: function (value) {

                                return "XAF"
                                    + value
                                    + "M";
                            }
                        }
                    },

                    x: {

                        grid: {
                            display: false
                        },

                        ticks: {

                            color: "#64748b",

                            font: {
                                size: 10
                            }
                        }
                    }
                }
            }
        });
    }


    /* =====================================
       QUICK ACTION BUTTONS
    ===================================== */

    const quickActions =
        document.querySelectorAll(".quick-action");

    quickActions.forEach(function (button) {

        button.addEventListener("click", function () {

            const action =
                button.dataset.action;

            if (action) {

                console.log(
                    "Selected action:",
                    action
                );
            }
        });
    });


    /* =====================================
       NOTIFICATION BUTTON
    ===================================== */

    const notificationButton =
        document.querySelector(".notification-button");

    if (notificationButton) {

        notificationButton.addEventListener(
            "click",
            function () {

                alert(
                    "You have 3 new notifications."
                );

            }
        );
    }


    /* =====================================
       STAT CARD ANIMATION
    ===================================== */

    const statCards =
        document.querySelectorAll(".stat-card");

    statCards.forEach(function (card, index) {

        card.style.animationDelay =
            `${index * 0.1}s`;
    });


    /* =====================================
       SEARCH
    ===================================== */

    const searchInput =
        document.querySelector(
            ".dashboard-search"
        );

    if (searchInput) {

        searchInput.addEventListener(
            "input",
            function () {

                const searchValue =
                    searchInput.value
                        .toLowerCase()
                        .trim();

                console.log(
                    "Searching for:",
                    searchValue
                );

                /*
                 * Database search will be
                 * connected later.
                 */
            }
        );
    }


    /* =====================================
       LOGOUT CONFIRMATION
    ===================================== */

    const logoutButton =
        document.querySelector(
            ".logout"
        );

    if (logoutButton) {

        logoutButton.addEventListener(
            "click",
            function (event) {

                const confirmLogout =
                    confirm(
                        "Are you sure you want to logout?"
                    );

                if (!confirmLogout) {
                    event.preventDefault();
                }
            }
        );
    }

});