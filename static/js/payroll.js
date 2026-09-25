document.addEventListener("DOMContentLoaded", function () {

    const sidebar = document.getElementById("sidebar");
    const sidebarToggle = document.getElementById("sidebarToggle");
    const payrollSearch = document.getElementById("payrollSearch");
    const payrollTableBody = document.getElementById("payrollTableBody");

    // ============================================================
    // SIDEBAR TOGGLE
    // ============================================================

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener("click", function () {
            sidebar.classList.toggle("show");
        });
    }


    // ============================================================
    // PAYROLL SEARCH
    // ============================================================

    if (payrollSearch && payrollTableBody) {

        payrollSearch.addEventListener("input", function () {

            const searchTerm = this.value
                .toLowerCase()
                .trim();

            const rows = payrollTableBody.querySelectorAll(
                "tr:not(#emptyPayrollRow)"
            );

            rows.forEach(function (row) {

                const rowText = row.textContent
                    .toLowerCase();

                if (rowText.includes(searchTerm)) {
                    row.style.display = "";
                } else {
                    row.style.display = "none";
                }

            });

        });

    }


    // ============================================================
    // CLOSE SIDEBAR ON MOBILE
    // ============================================================

    document.addEventListener("click", function (event) {

        if (!sidebar || !sidebarToggle) {
            return;
        }

        const isMobile = window.innerWidth <= 992;

        if (!isMobile) {
            return;
        }

        if (
            sidebar.classList.contains("show") &&
            !sidebar.contains(event.target) &&
            !sidebarToggle.contains(event.target)
        ) {
            sidebar.classList.remove("show");
        }

    });


    // ============================================================
    // PAYROLL BUTTON LOADING STATE
    // ============================================================

    const payForms = document.querySelectorAll(
        'form[action*="/pay"]'
    );

    payForms.forEach(function (form) {

        form.addEventListener("submit", function () {

            const button = form.querySelector(
                "button[type='submit']"
            );

            if (!button) {
                return;
            }

            button.disabled = true;

            button.innerHTML =
                '<span class="spinner-border spinner-border-sm" ' +
                'aria-hidden="true"></span>';

        });

    });


    // ============================================================
    // DELETE CONFIRMATION
    // ============================================================

    const deleteForms = document.querySelectorAll(
        ".delete-form"
    );

    deleteForms.forEach(function (form) {

        form.addEventListener("submit", function (event) {

            const confirmed = confirm(
                "Are you sure you want to delete this payroll record?"
            );

            if (!confirmed) {
                event.preventDefault();
            }

        });

    });


    // ============================================================
    // SIMPLE PAGE ANIMATION
    // ============================================================

    const animatedItems = document.querySelectorAll(
        ".stat-card, .payroll-directory"
    );

    animatedItems.forEach(function (item, index) {

        item.style.opacity = "0";
        item.style.transform = "translateY(10px)";

        setTimeout(function () {

            item.style.transition =
                "opacity 0.35s ease, transform 0.35s ease";

            item.style.opacity = "1";
            item.style.transform = "translateY(0)";

        }, index * 80);

    });

});