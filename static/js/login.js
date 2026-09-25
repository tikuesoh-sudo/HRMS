document.addEventListener("DOMContentLoaded", function () {

    const loginForm = document.getElementById("loginForm");
    const passwordInput = document.getElementById("password");
    const togglePassword = document.getElementById("togglePassword");

    const loginButton = document.getElementById("loginButton");
    const loginText = document.getElementById("loginText");
    const loginSpinner = document.getElementById("loginSpinner");

    const forgotPassword =
        document.getElementById("forgotPassword");


    /* =====================================
       SHOW / HIDE PASSWORD
    ===================================== */

    if (togglePassword && passwordInput) {

        togglePassword.addEventListener("click", function () {

            if (passwordInput.type === "password") {

                passwordInput.type = "text";

                togglePassword.innerHTML =
                    '<i class="bi bi-eye-slash"></i>';

            } else {

                passwordInput.type = "password";

                togglePassword.innerHTML =
                    '<i class="bi bi-eye"></i>';
            }

        });
    }


    /* =====================================
       LOGIN FORM
    ===================================== */

    if (loginForm) {

        loginForm.addEventListener("submit", function () {

            /*
             * DO NOT USE:
             *
             * event.preventDefault();
             *
             * Flask must receive this POST request.
             */

            if (loginButton) {
                loginButton.disabled = true;
            }

            if (loginText) {
                loginText.textContent = "Signing In...";
            }

            if (loginSpinner) {
                loginSpinner.classList.remove("d-none");
            }

        });
    }


    /* =====================================
       FORGOT PASSWORD
    ===================================== */

    if (forgotPassword) {

        forgotPassword.addEventListener(
            "click",
            function (event) {

                event.preventDefault();

                alert(
                    "Password recovery will be implemented later."
                );

            }
        );
    }

});