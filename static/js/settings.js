// static/js/settings.js

(function () {

    "use strict";


    /* =====================================================
       SETTINGS STORAGE
    ===================================================== */

    const STORAGE_KEY = "hrms_settings";


    const defaultSettings = {

        dark_mode: false,

        compact_sidebar: false,

        email_notifications: true,

        leave_notifications: true,

        payroll_notifications: true,

        two_factor: false

    };


    function getStoredSettings() {

        try {

            const stored =
                localStorage.getItem(STORAGE_KEY);

            if (!stored) {
                return { ...defaultSettings };
            }

            return {
                ...defaultSettings,
                ...JSON.parse(stored)
            };

        } catch (error) {

            return { ...defaultSettings };

        }

    }


    function saveSettings(settings) {

        localStorage.setItem(
            STORAGE_KEY,
            JSON.stringify(settings)
        );

    }


    let settings = getStoredSettings();


    /* =====================================================
       DARK MODE
    ===================================================== */

    function applyDarkMode(enabled) {

        document.documentElement.setAttribute(
            "data-theme",
            enabled ? "dark" : "light"
        );

        document.body.classList.toggle(
            "dark-mode",
            enabled
        );

    }


    /* =====================================================
       COMPACT SIDEBAR
    ===================================================== */

    function applyCompactSidebar(enabled) {

        document.body.classList.toggle(
            "compact-sidebar",
            enabled
        );

        const sidebar =
            document.getElementById("sidebar");

        if (sidebar) {

            sidebar.classList.toggle(
                "compact",
                enabled
            );

        }

    }


    /* =====================================================
       APPLY SETTINGS ON PAGE LOAD
    ===================================================== */

    applyDarkMode(settings.dark_mode);

    applyCompactSidebar(
        settings.compact_sidebar
    );


    /* =====================================================
       SETTINGS PAGE CONTROLS
    ===================================================== */

    const darkMode =
        document.getElementById("dark_mode");

    const compactSidebar =
        document.getElementById(
            "compact_sidebar"
        );

    const emailNotifications =
        document.getElementById(
            "email_notifications"
        );

    const leaveNotifications =
        document.getElementById(
            "leave_notifications"
        );

    const payrollNotifications =
        document.getElementById(
            "payroll_notifications"
        );

    const twoFactor =
        document.getElementById("two_factor");


    if (darkMode) {

        darkMode.checked =
            settings.dark_mode;

        darkMode.addEventListener(
            "change",
            function () {

                settings.dark_mode =
                    darkMode.checked;

                saveSettings(settings);

                applyDarkMode(
                    settings.dark_mode
                );

            }
        );

    }


    if (compactSidebar) {

        compactSidebar.checked =
            settings.compact_sidebar;

        compactSidebar.addEventListener(
            "change",
            function () {

                settings.compact_sidebar =
                    compactSidebar.checked;

                saveSettings(settings);

                applyCompactSidebar(
                    settings.compact_sidebar
                );

            }
        );

    }


    if (emailNotifications) {

        emailNotifications.checked =
            settings.email_notifications;

        emailNotifications.addEventListener(
            "change",
            function () {

                settings.email_notifications =
                    emailNotifications.checked;

                saveSettings(settings);

            }
        );

    }


    if (leaveNotifications) {

        leaveNotifications.checked =
            settings.leave_notifications;

        leaveNotifications.addEventListener(
            "change",
            function () {

                settings.leave_notifications =
                    leaveNotifications.checked;

                saveSettings(settings);

            }
        );

    }


    if (payrollNotifications) {

        payrollNotifications.checked =
            settings.payroll_notifications;

        payrollNotifications.addEventListener(
            "change",
            function () {

                settings.payroll_notifications =
                    payrollNotifications.checked;

                saveSettings(settings);

            }
        );

    }


    if (twoFactor) {

        twoFactor.checked =
            settings.two_factor;

        twoFactor.addEventListener(
            "change",
            function () {

                settings.two_factor =
                    twoFactor.checked;

                saveSettings(settings);

            }
        );

    }


    /* =====================================================
       SIDEBAR TOGGLE
    ===================================================== */

    const sidebarToggle =
        document.getElementById(
            "sidebarToggle"
        );

    const sidebar =
        document.getElementById("sidebar");


    if (
        sidebarToggle &&
        sidebar
    ) {

        sidebarToggle.addEventListener(
            "click",
            function () {

                sidebar.classList.toggle(
                    "collapsed"
                );

            }
        );

    }


    /* =====================================================
       CHANGE PASSWORD MODAL
    ===================================================== */

    const changePasswordBtn =
        document.getElementById(
            "changePasswordBtn"
        );

    const passwordModal =
        document.getElementById(
            "passwordModal"
        );

    const passwordForm =
        document.getElementById(
            "passwordForm"
        );

    const closePasswordModal =
        document.getElementById(
            "closePasswordModal"
        );

    const cancelPasswordBtn =
        document.getElementById(
            "cancelPasswordBtn"
        );


    function openPasswordModal() {

        if (!passwordModal) {
            return;
        }

        passwordModal.classList.add(
            "show"
        );

        document.body.classList.add(
            "modal-open"
        );

    }


    function closePasswordModalFunction() {

        if (!passwordModal) {
            return;
        }

        passwordModal.classList.remove(
            "show"
        );

        document.body.classList.remove(
            "modal-open"
        );

        if (passwordForm) {
            passwordForm.reset();
        }

    }


    if (changePasswordBtn) {

        changePasswordBtn.addEventListener(
            "click",
            openPasswordModal
        );

    }


    if (closePasswordModal) {

        closePasswordModal.addEventListener(
            "click",
            closePasswordModalFunction
        );

    }


    if (cancelPasswordBtn) {

        cancelPasswordBtn.addEventListener(
            "click",
            closePasswordModalFunction
        );

    }


    if (passwordModal) {

        passwordModal.addEventListener(
            "click",
            function (event) {

                if (
                    event.target ===
                    passwordModal
                ) {

                    closePasswordModalFunction();

                }

            }
        );

    }


    /* =====================================================
       PASSWORD VALIDATION
    ===================================================== */

    if (passwordForm) {

        passwordForm.addEventListener(
            "submit",
            function (event) {

                const newPassword =
                    document.getElementById(
                        "new_password"
                    );

                const confirmPassword =
                    document.getElementById(
                        "confirm_password"
                    );

                if (
                    newPassword &&
                    confirmPassword &&
                    newPassword.value !==
                    confirmPassword.value
                ) {

                    event.preventDefault();

                    alert(
                        "The new passwords do not match."
                    );

                    return;

                }


                if (
                    newPassword &&
                    newPassword.value.length < 6
                ) {

                    event.preventDefault();

                    alert(
                        "Password must contain at least 6 characters."
                    );

                }

            }
        );

    }


    /* =====================================================
       RESET SETTINGS
    ===================================================== */

    const settingsForm =
        document.getElementById(
            "settingsForm"
        );

    const resetSettingsBtn =
        document.getElementById(
            "resetSettingsBtn"
        );


    if (resetSettingsBtn) {

        resetSettingsBtn.addEventListener(
            "click",
            function () {

                const confirmed =
                    confirm(
                        "Reset all preferences to their default values?"
                    );

                if (!confirmed) {
                    return;
                }

                settings =
                    { ...defaultSettings };

                saveSettings(settings);

                applyDarkMode(false);

                applyCompactSidebar(false);

                if (darkMode) {
                    darkMode.checked = false;
                }

                if (compactSidebar) {
                    compactSidebar.checked = false;
                }

                if (emailNotifications) {
                    emailNotifications.checked = true;
                }

                if (leaveNotifications) {
                    leaveNotifications.checked = true;
                }

                if (payrollNotifications) {
                    payrollNotifications.checked = true;
                }

                if (twoFactor) {
                    twoFactor.checked = false;
                }

            }
        );

    }


    /* =====================================================
       SAVE SETTINGS
    ===================================================== */

    if (settingsForm) {

        settingsForm.addEventListener(
            "submit",
            function () {

                settings.dark_mode =
                    darkMode
                        ? darkMode.checked
                        : false;

                settings.compact_sidebar =
                    compactSidebar
                        ? compactSidebar.checked
                        : false;

                settings.email_notifications =
                    emailNotifications
                        ? emailNotifications.checked
                        : true;

                settings.leave_notifications =
                    leaveNotifications
                        ? leaveNotifications.checked
                        : true;

                settings.payroll_notifications =
                    payrollNotifications
                        ? payrollNotifications.checked
                        : true;

                settings.two_factor =
                    twoFactor
                        ? twoFactor.checked
                        : false;

                saveSettings(settings);

            }
        );

    }


    /* =====================================================
       GLOBAL SETTINGS ACCESS
    ===================================================== */

    window.HRMSSettings = {

        get: function () {
            return getStoredSettings();
        },

        save: function (newSettings) {

            settings = {
                ...settings,
                ...newSettings
            };

            saveSettings(settings);

            applyDarkMode(
                settings.dark_mode
            );

            applyCompactSidebar(
                settings.compact_sidebar
            );

        },

        apply: function () {

            settings =
                getStoredSettings();

            applyDarkMode(
                settings.dark_mode
            );

            applyCompactSidebar(
                settings.compact_sidebar
            );

        }

    };

})();