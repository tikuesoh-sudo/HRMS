from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import json
import os


app = Flask(__name__)
app.secret_key = "hrms-secret-key"


# ============================================================
# SAMPLE DATA
# ============================================================

employees = [
    {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@hrms.com",
        "phone": "+237 690 123 456",
        "department": "Human Resources",
        "position": "HR Manager",
        "salary": 450000,
        "status": "Active",
        "join_date": "2024-01-15"
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "email": "jane.smith@hrms.com",
        "phone": "+237 691 234 567",
        "department": "Finance",
        "position": "Accountant",
        "salary": 380000,
        "status": "Active",
        "join_date": "2024-03-10"
    },
    {
        "id": 3,
        "name": "Michael Johnson",
        "email": "michael.johnson@hrms.com",
        "phone": "+237 692 345 678",
        "department": "IT",
        "position": "Software Developer",
        "salary": 500000,
        "status": "Active",
        "join_date": "2024-02-20"
    },
    {
        "id": 4,
        "name": "Sarah Williams",
        "email": "sarah.williams@hrms.com",
        "phone": "+237 693 456 789",
        "department": "Marketing",
        "position": "Marketing Officer",
        "salary": 350000,
        "status": "Probation",
        "join_date": "2025-01-05"
    }
]


departments = [
    {
        "id": 1,
        "name": "Human Resources",
        "manager": "John Doe",
        "employees": 1
    },
    {
        "id": 2,
        "name": "Finance",
        "manager": "Jane Smith",
        "employees": 1
    },
    {
        "id": 3,
        "name": "IT",
        "manager": "Michael Johnson",
        "employees": 1
    },
    {
        "id": 4,
        "name": "Marketing",
        "manager": "Sarah Williams",
        "employees": 1
    }
]


leave_requests = [
    {
        "id": 1,
        "employee": "John Doe",
        "leave_type": "Annual Leave",
        "start_date": "2025-03-10",
        "end_date": "2025-03-14",
        "days": 5,
        "reason": "Family vacation",
        "status": "Approved"
    },
    {
        "id": 2,
        "employee": "Jane Smith",
        "leave_type": "Sick Leave",
        "start_date": "2025-03-20",
        "end_date": "2025-03-21",
        "days": 2,
        "reason": "Medical appointment",
        "status": "Pending"
    }
]


payroll_records = []


# ============================================================
# NOTIFICATIONS
# ============================================================

notification_records = [
    {
        "id": 1,
        "title": "Pending Leave Request",
        "message": "Jane Smith has a pending Sick Leave request.",
        "type": "Leave",
        "read": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
]


def add_notification(title, message, notification_type="General"):
    """Create a new notification."""

    new_id = (
        max(notification["id"] for notification in notification_records) + 1
        if notification_records
        else 1
    )

    notification_records.insert(
        0,
        {
            "id": new_id,
            "title": title,
            "message": message,
            "type": notification_type,
            "read": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    )

    return new_id


def get_unread_notification_count():
    """Return the number of unread notifications."""

    return sum(
        1
        for notification in notification_records
        if not notification["read"]
    )


@app.context_processor
def inject_notification_data():
    """Make unread notification count available to all templates."""

    return {
        "unread_notifications": get_unread_notification_count()
    }


# ============================================================
# SETTINGS
# ============================================================

settings_data = {
    "company_name": "HRMS Company",
    "timezone": "Africa/Douala",
    "currency": "FCFA",
    "date_format": "YYYY-MM-DD",
    "email_notifications": True,
    "leave_notifications": True,
    "payroll_notifications": True,
    "two_factor": False,
    "dark_mode": False,
    "compact_sidebar": False
}


# ============================================================
# ADMIN ACCOUNT
# ============================================================

CREDENTIALS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "admin_credentials.json"
)


DEFAULT_ADMIN_CREDENTIALS = {
    "email": "admin@hrms.com",
    "password": "admin123"
}


admin_credentials = DEFAULT_ADMIN_CREDENTIALS.copy()


def save_admin_credentials(credentials):
    """Save admin credentials to a JSON file."""

    with open(CREDENTIALS_FILE, "w", encoding="utf-8") as file:
        json.dump(credentials, file, indent=4)


def load_admin_credentials():
    """Load admin credentials from the JSON file."""

    if not os.path.exists(CREDENTIALS_FILE):
        save_admin_credentials(DEFAULT_ADMIN_CREDENTIALS)
        return DEFAULT_ADMIN_CREDENTIALS.copy()

    try:
        with open(CREDENTIALS_FILE, "r", encoding="utf-8") as file:
            credentials = json.load(file)

        if (
            isinstance(credentials, dict)
            and "email" in credentials
            and "password" in credentials
        ):
            return credentials

    except (json.JSONDecodeError, OSError):
        pass

    save_admin_credentials(DEFAULT_ADMIN_CREDENTIALS)
    return DEFAULT_ADMIN_CREDENTIALS.copy()


admin_credentials = load_admin_credentials()


# ============================================================
# LOGIN
# ============================================================

@app.route("/", methods=["GET", "POST"])
def login():

    global admin_credentials

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        admin_credentials = load_admin_credentials()

        stored_email = admin_credentials.get(
            "email", ""
        ).strip().lower()

        stored_password = admin_credentials.get(
            "password", ""
        )

        if email == stored_email and password == stored_password:
            return redirect(url_for("dashboard"))

        flash(
            "Invalid email address or password.",
            "danger"
        )

    return render_template("authentication/login.html")


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    flash(
        "You have been logged out successfully.",
        "success"
    )

    return redirect(url_for("login"))


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():

    total_employees = len(employees)

    active_employees = sum(
        1
        for employee in employees
        if employee["status"] == "Active"
    )

    probation_employees = sum(
        1
        for employee in employees
        if employee["status"] == "Probation"
    )

    inactive_employees = sum(
        1
        for employee in employees
        if employee["status"] == "Inactive"
    )

    pending_leave = sum(
        1
        for leave in leave_requests
        if leave["status"] == "Pending"
    )

    approved_leave = sum(
        1
        for leave in leave_requests
        if leave["status"] == "Approved"
    )

    monthly_payroll = sum(
        employee["salary"]
        for employee in employees
    )

    return render_template(
        "dashboard/dashboard.html",
        employees=employees,
        leave_requests=leave_requests,
        total_employees=total_employees,
        active_employees=active_employees,
        probation_employees=probation_employees,
        inactive_employees=inactive_employees,
        pending_leave=pending_leave,
        approved_leave=approved_leave,
        monthly_payroll=monthly_payroll
    )


# ============================================================
# NOTIFICATIONS
# ============================================================

@app.route("/notifications")
def notifications():

    return render_template(
        "notifications/notifications.html",
        notifications=notification_records
    )


@app.route("/notifications/create", methods=["GET", "POST"])
def create_notification():

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        message = request.form.get("message", "").strip()
        notification_type = request.form.get(
            "type",
            "General"
        ).strip()

        if not title or not message:
            flash(
                "Title and message are required.",
                "danger"
            )

            return redirect(
                url_for("create_notification")
            )

        add_notification(
            title,
            message,
            notification_type
        )

        flash(
            "Notification created successfully.",
            "success"
        )

        return redirect(
            url_for("notifications")
        )

    return render_template(
        "notifications/create_notification.html"
    )


@app.route(
    "/notifications/<int:notification_id>/read",
    methods=["POST"]
)
def mark_notification_read(notification_id):

    for notification in notification_records:

        if notification["id"] == notification_id:
            notification["read"] = True
            break

    return redirect(
        url_for("notifications")
    )


@app.route(
    "/notifications/<int:notification_id>/delete",
    methods=["POST"]
)
def delete_notification(notification_id):

    global notification_records

    notification_records = [
        notification
        for notification in notification_records
        if notification["id"] != notification_id
    ]

    flash(
        "Notification deleted successfully.",
        "success"
    )

    return redirect(
        url_for("notifications")
    )


@app.route(
    "/notifications/read-all",
    methods=["POST"]
)
def mark_all_notifications_read():

    for notification in notification_records:
        notification["read"] = True

    flash(
        "All notifications marked as read.",
        "success"
    )

    return redirect(
        url_for("notifications")
    )


@app.route(
    "/notifications/delete-all",
    methods=["POST"]
)
def delete_all_notifications():

    notification_records.clear()

    flash(
        "All notifications deleted.",
        "success"
    )

    return redirect(
        url_for("notifications")
    )


# ============================================================
# EMPLOYEES
# ============================================================

@app.route("/employees")
def employee_list():

    search = request.args.get(
        "search",
        ""
    ).strip().lower()

    filtered_employees = employees

    if search:

        filtered_employees = [
            employee
            for employee in employees
            if (
                search in employee["name"].lower()
                or search in employee["email"].lower()
                or search in employee["department"].lower()
                or search in employee["position"].lower()
            )
        ]

    return render_template(
        "employees/employees.html",
        employees=filtered_employees,
        search=search
    )


@app.route("/employees/add", methods=["GET", "POST"])
def add_employee():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        department = request.form.get(
            "department",
            ""
        ).strip()

        position = request.form.get(
            "position",
            ""
        ).strip()

        status = request.form.get(
            "status",
            "Active"
        ).strip()

        join_date = request.form.get(
            "join_date",
            ""
        ).strip()

        try:
            salary = float(
                request.form.get(
                    "salary",
                    0
                )
            )
        except ValueError:
            flash(
                "Salary must be a valid number.",
                "danger"
            )

            return redirect(
                url_for("add_employee")
            )

        if not name or not email:
            flash(
                "Name and email are required.",
                "danger"
            )

            return redirect(
                url_for("add_employee")
            )

        new_id = (
            max(employee["id"] for employee in employees) + 1
            if employees
            else 1
        )

        new_employee = {
            "id": new_id,
            "name": name,
            "email": email,
            "phone": phone,
            "department": department,
            "position": position,
            "salary": salary,
            "status": status,
            "join_date": join_date
        }

        employees.append(new_employee)

        add_notification(
            "New Employee Added",
            f"{name} has been added to the employee list.",
            "Employee"
        )

        flash(
            "Employee added successfully.",
            "success"
        )

        return redirect(
            url_for("employee_list")
        )

    return render_template(
        "employees/add_employee.html",
        departments=departments
    )


@app.route("/employees/<int:employee_id>")
def employee_detail(employee_id):

    employee = next(
        (
            employee
            for employee in employees
            if employee["id"] == employee_id
        ),
        None
    )

    if employee is None:
        flash(
            "Employee not found.",
            "danger"
        )

        return redirect(
            url_for("employee_list")
        )

    return render_template(
        "employees/employee_detail.html",
        employee=employee
    )


@app.route(
    "/employees/<int:employee_id>/edit",
    methods=["GET", "POST"]
)
def edit_employee(employee_id):

    employee = next(
        (
            employee
            for employee in employees
            if employee["id"] == employee_id
        ),
        None
    )

    if employee is None:
        flash(
            "Employee not found.",
            "danger"
        )

        return redirect(
            url_for("employee_list")
        )

    if request.method == "POST":

        employee["name"] = request.form.get(
            "name",
            ""
        ).strip()

        employee["email"] = request.form.get(
            "email",
            ""
        ).strip()

        employee["phone"] = request.form.get(
            "phone",
            ""
        ).strip()

        employee["department"] = request.form.get(
            "department",
            ""
        ).strip()

        employee["position"] = request.form.get(
            "position",
            ""
        ).strip()

        employee["status"] = request.form.get(
            "status",
            "Active"
        ).strip()

        employee["join_date"] = request.form.get(
            "join_date",
            ""
        ).strip()

        try:
            employee["salary"] = float(
                request.form.get(
                    "salary",
                    0
                )
            )
        except ValueError:
            flash(
                "Salary must be a valid number.",
                "danger"
            )

            return redirect(
                url_for(
                    "edit_employee",
                    employee_id=employee_id
                )
            )

        flash(
            "Employee updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "employee_detail",
                employee_id=employee_id
            )
        )

    return render_template(
        "employees/edit_employee.html",
        employee=employee,
        departments=departments
    )


@app.route(
    "/employees/<int:employee_id>/delete",
    methods=["POST"]
)
def delete_employee(employee_id):

    global employees

    employee = next(
        (
            employee
            for employee in employees
            if employee["id"] == employee_id
        ),
        None
    )

    if employee is None:
        flash(
            "Employee not found.",
            "danger"
        )

        return redirect(
            url_for("employee_list")
        )

    employee_name = employee["name"]

    employees = [
        employee
        for employee in employees
        if employee["id"] != employee_id
    ]

    add_notification(
        "Employee Deleted",
        f"{employee_name} has been removed from the employee list.",
        "Employee"
    )

    flash(
        "Employee deleted successfully.",
        "success"
    )

    return redirect(
        url_for("employee_list")
    )


# ============================================================
# LEAVE
# ============================================================

@app.route("/leave")
def leave_list():
    total_leave_requests = len(leave_requests)

    pending_leave_requests = sum(
        1 for leave in leave_requests
        if leave.get("status") == "Pending"
    )

    approved_leave_requests = sum(
        1 for leave in leave_requests
        if leave.get("status") == "Approved"
    )

    rejected_leave_requests = sum(
        1 for leave in leave_requests
        if leave.get("status") == "Rejected"
    )

    return render_template(
        "leave/leave_list.html",
        leave_requests=leave_requests,
        total_leave_requests=total_leave_requests,
        pending_leave_requests=pending_leave_requests,
        approved_leave_requests=approved_leave_requests,
        rejected_leave_requests=rejected_leave_requests
    )


@app.route("/leave/apply", methods=["GET", "POST"])
def apply_leave():

    if request.method == "POST":

        employee_name = request.form.get(
            "employee",
            ""
        ).strip()

        leave_type = request.form.get(
            "leave_type",
            ""
        ).strip()

        start_date = request.form.get(
            "start_date",
            ""
        ).strip()

        end_date = request.form.get(
            "end_date",
            ""
        ).strip()

        reason = request.form.get(
            "reason",
            ""
        ).strip()

        try:
            days = int(
                request.form.get(
                    "days",
                    0
                )
            )
        except ValueError:
            days = 0

        if not employee_name or not leave_type:
            flash(
                "Employee and leave type are required.",
                "danger"
            )

            return redirect(
                url_for("apply_leave")
            )

        if days <= 0:
            flash(
                "Leave days must be greater than zero.",
                "danger"
            )

            return redirect(
                url_for("apply_leave")
            )

        new_id = (
            max(leave["id"] for leave in leave_requests) + 1
            if leave_requests
            else 1
        )

        new_leave = {
            "id": new_id,
            "employee": employee_name,
            "leave_type": leave_type,
            "start_date": start_date,
            "end_date": end_date,
            "days": days,
            "reason": reason,
            "status": "Pending"
        }

        leave_requests.append(new_leave)

        if settings_data["leave_notifications"]:

            add_notification(
                "New Leave Request",
                f"{employee_name} submitted a {leave_type} request.",
                "Leave"
            )

        flash(
            "Leave request submitted successfully.",
            "success"
        )

        return redirect(
            url_for("leave_list")
        )

    return render_template(
        "leave/apply_leave.html",
        employees=employees
    )


@app.route("/leave/<int:leave_id>")
def leave_detail(leave_id):

    leave = next(
        (
            leave
            for leave in leave_requests
            if leave["id"] == leave_id
        ),
        None
    )

    if leave is None:
        flash(
            "Leave request not found.",
            "danger"
        )

        return redirect(
            url_for("leave_list")
        )

    return render_template(
        "leave/leave_detail.html",
        leave=leave
    )


@app.route(
    "/leave/<int:leave_id>/approve",
    methods=["POST"]
)
def approve_leave(leave_id):

    leave = next(
        (
            leave
            for leave in leave_requests
            if leave["id"] == leave_id
        ),
        None
    )

    if leave is None:
        flash(
            "Leave request not found.",
            "danger"
        )

        return redirect(
            url_for("leave_list")
        )

    leave["status"] = "Approved"

    if settings_data["leave_notifications"]:

        add_notification(
            "Leave Approved",
            f"{leave['employee']}'s {leave['leave_type']} request was approved.",
            "Leave"
        )

    flash(
        "Leave request approved.",
        "success"
    )

    return redirect(
        url_for("leave_list")
    )


@app.route(
    "/leave/<int:leave_id>/reject",
    methods=["POST"]
)
def reject_leave(leave_id):

    leave = next(
        (
            leave
            for leave in leave_requests
            if leave["id"] == leave_id
        ),
        None
    )

    if leave is None:
        flash(
            "Leave request not found.",
            "danger"
        )

        return redirect(
            url_for("leave_list")
        )

    leave["status"] = "Rejected"

    if settings_data["leave_notifications"]:

        add_notification(
            "Leave Rejected",
            f"{leave['employee']}'s {leave['leave_type']} request was rejected.",
            "Leave"
        )

    flash(
        "Leave request rejected.",
        "warning"
    )

    return redirect(
        url_for("leave_list")
    )


# ============================================================
# PAYROLL
# ============================================================

@app.route("/payroll")
def payroll():

    total_payroll = sum(
        record["net_salary"]
        for record in payroll_records
    )

    paid_payroll = sum(
        record["net_salary"]
        for record in payroll_records
        if record["status"] == "Paid"
    )

    pending_payroll = sum(
        record["net_salary"]
        for record in payroll_records
        if record["status"] == "Pending"
    )

    return render_template(
        "payroll/payroll.html",
        payroll_records=payroll_records,
        total_payroll=total_payroll,
        paid_payroll=paid_payroll,
        pending_payroll=pending_payroll
    )


@app.route("/payroll/add", methods=["GET", "POST"])
def add_payroll():

    if request.method == "POST":

        employee_name = request.form.get(
            "employee",
            ""
        ).strip()

        pay_period = request.form.get(
            "pay_period",
            ""
        ).strip()

        try:
            allowances = float(
                request.form.get(
                    "allowances",
                    0
                )
            )
        except ValueError:
            allowances = 0

        try:
            deductions = float(
                request.form.get(
                    "deductions",
                    0
                )
            )
        except ValueError:
            deductions = 0

        employee = next(
            (
                employee
                for employee in employees
                if employee["name"] == employee_name
            ),
            None
        )

        if employee is None:
            flash(
                "Employee not found.",
                "danger"
            )

            return redirect(
                url_for("add_payroll")
            )

        basic_salary = employee["salary"]

        gross_salary = (
            basic_salary + allowances
        )

        net_salary = (
            gross_salary - deductions
        )

        new_id = (
            max(record["id"] for record in payroll_records) + 1
            if payroll_records
            else 1
        )

        new_record = {
            "id": new_id,
            "employee": employee_name,
            "pay_period": pay_period,
            "basic_salary": basic_salary,
            "allowances": allowances,
            "deductions": deductions,
            "gross_salary": gross_salary,
            "net_salary": net_salary,
            "status": "Pending"
        }

        payroll_records.append(new_record)

        if settings_data["payroll_notifications"]:

            add_notification(
                "Payroll Generated",
                f"Payroll for {employee_name} has been generated.",
                "Payroll"
            )

        flash(
            "Payroll record created successfully.",
            "success"
        )

        return redirect(
            url_for("payroll")
        )

    return render_template(
        "payroll/add_payroll.html",
        employees=employees
    )


@app.route("/payroll/<int:payroll_id>")
def payroll_detail(payroll_id):

    record = next(
        (
            record
            for record in payroll_records
            if record["id"] == payroll_id
        ),
        None
    )

    if record is None:
        flash(
            "Payroll record not found.",
            "danger"
        )

        return redirect(
            url_for("payroll")
        )

    return render_template(
        "payroll/payroll_detail.html",
        payroll=record
    )


@app.route(
    "/payroll/<int:payroll_id>/pay",
    methods=["POST"]
)
def mark_payroll_paid(payroll_id):

    record = next(
        (
            record
            for record in payroll_records
            if record["id"] == payroll_id
        ),
        None
    )

    if record is None:
        flash(
            "Payroll record not found.",
            "danger"
        )

        return redirect(
            url_for("payroll")
        )

    record["status"] = "Paid"

    if settings_data["payroll_notifications"]:

        add_notification(
            "Payroll Paid",
            f"Payroll for {record['employee']} has been marked as paid.",
            "Payroll"
        )

    flash(
        "Payroll marked as paid.",
        "success"
    )

    return redirect(
        url_for("payroll")
    )


@app.route(
    "/payroll/<int:payroll_id>/delete",
    methods=["POST"]
)
def delete_payroll(payroll_id):

    global payroll_records

    payroll_records = [
        record
        for record in payroll_records
        if record["id"] != payroll_id
    ]

    flash(
        "Payroll record deleted successfully.",
        "success"
    )

    return redirect(
        url_for("payroll")
    )


# ============================================================
# REPORTS
# ============================================================

@app.route("/reports")
def reports():

    total_employees = len(employees)

    active_employees = sum(1 for employee in employees if employee.get("status") == "Active")
    probation_employees = sum(1 for employee in employees if employee.get("status") == "Probation")
    inactive_employees = sum(1 for employee in employees if employee.get("status") == "Inactive")

    total_salary = sum(employee.get("salary", 0) for employee in employees)
    average_salary = total_salary / total_employees if total_employees else 0

    department_reports = []
    for department in departments:
        department_name = department.get("name", "")
        department_employees = [employee for employee in employees if employee.get("department") == department_name]
        department_active = sum(1 for employee in department_employees if employee.get("status") == "Active")
        department_payroll = sum(employee.get("salary", 0) for employee in department_employees)
        department_reports.append({
            "department": department_name,
            "name": department_name,
            "manager": department.get("manager", ""),
            "employees": len(department_employees),
            "active": department_active,
            "payroll": department_payroll
        })

    total_leave_requests = len(leave_requests)
    pending_leave_requests = sum(1 for leave in leave_requests if leave.get("status") == "Pending")
    approved_leave_requests = sum(1 for leave in leave_requests if leave.get("status") == "Approved")
    rejected_leave_requests = sum(1 for leave in leave_requests if leave.get("status") == "Rejected")
    total_leave_days = sum(leave.get("days", 0) for leave in leave_requests)

    leave_type_reports = {}
    for leave in leave_requests:
        leave_type = leave.get("leave_type", leave.get("type", "Other"))
        if leave_type not in leave_type_reports:
            leave_type_reports[leave_type] = {"requests": 0, "days": 0}
        leave_type_reports[leave_type]["requests"] += 1
        leave_type_reports[leave_type]["days"] += leave.get("days", 0)

    total_payroll_records = len(payroll_records)
    paid_payroll_records = sum(1 for record in payroll_records if record.get("status") == "Paid")
    pending_payroll_records = sum(1 for record in payroll_records if record.get("status") == "Pending")
    payroll_total = sum(record.get("net_salary", 0) for record in payroll_records)
    payroll_paid = sum(record.get("net_salary", 0) for record in payroll_records if record.get("status") == "Paid")
    payroll_pending = sum(record.get("net_salary", 0) for record in payroll_records if record.get("status") == "Pending")

    recent_payroll = payroll_records[-5:][::-1]
    recent_leave = []
    for leave in leave_requests[-5:][::-1]:
        leave_copy = dict(leave)
        leave_copy["type"] = leave_copy.get("type", leave_copy.get("leave_type", "Leave"))
        recent_leave.append(leave_copy)

    return render_template(
        "reports/reports.html",
        total_employees=total_employees,
        active_employees=active_employees,
        probation_employees=probation_employees,
        inactive_employees=inactive_employees,
        total_salary=total_salary,
        average_salary=average_salary,
        department_reports=department_reports,
        total_leave_requests=total_leave_requests,
        pending_leave_requests=pending_leave_requests,
        approved_leave_requests=approved_leave_requests,
        rejected_leave_requests=rejected_leave_requests,
        total_leave_days=total_leave_days,
        total_leave=total_leave_requests,
        pending_leave=pending_leave_requests,
        approved_leave=approved_leave_requests,
        rejected_leave=rejected_leave_requests,
        leave_type_reports=leave_type_reports,
        payroll_total=payroll_total,
        payroll_paid=payroll_paid,
        payroll_pending=payroll_pending,
        total_payroll=payroll_total,
        paid_payroll=payroll_paid,
        pending_payroll=payroll_pending,
        total_payroll_records=total_payroll_records,
        paid_payroll_records=paid_payroll_records,
        pending_payroll_records=pending_payroll_records,
        recent_payroll=recent_payroll,
        recent_leave=recent_leave,
        settings=settings_data
    )


# ============================================================
# PROFILE
# ============================================================

@app.route("/profile", methods=["GET", "POST"])
def profile():

    if request.method == "POST":

        flash(
            "Profile updated successfully!",
            "success"
        )

        return redirect(
            url_for("profile")
        )

    return render_template(
        "profile/profile.html"
    )


# ============================================================
# SETTINGS
# ============================================================

@app.route("/settings", methods=["GET", "POST"])
def settings():

    if request.method == "POST":

        settings_data["company_name"] = request.form.get(
            "company_name",
            settings_data["company_name"]
        ).strip()

        settings_data["timezone"] = request.form.get(
            "timezone",
            settings_data["timezone"]
        ).strip()

        settings_data["currency"] = request.form.get(
            "currency",
            settings_data["currency"]
        ).strip()

        settings_data["date_format"] = request.form.get(
            "date_format",
            settings_data["date_format"]
        ).strip()

        settings_data["email_notifications"] = (
            request.form.get("email_notifications") == "on"
        )

        settings_data["leave_notifications"] = (
            request.form.get("leave_notifications") == "on"
        )

        settings_data["payroll_notifications"] = (
            request.form.get("payroll_notifications") == "on"
        )

        settings_data["two_factor"] = (
            request.form.get("two_factor") == "on"
        )

        settings_data["dark_mode"] = (
            request.form.get("dark_mode") == "on"
        )

        settings_data["compact_sidebar"] = (
            request.form.get("compact_sidebar") == "on"
        )

        flash(
            "Settings saved successfully.",
            "success"
        )

        return redirect(
            url_for("settings")
        )

    return render_template(
        "settings/settings.html",
        settings=settings_data
    )


@app.route(
    "/settings/reset",
    methods=["POST"]
)
def reset_settings():

    default_settings = {
        "company_name": "HRMS Company",
        "timezone": "Africa/Douala",
        "currency": "FCFA",
        "date_format": "YYYY-MM-DD",
        "email_notifications": True,
        "leave_notifications": True,
        "payroll_notifications": True,
        "two_factor": False,
        "dark_mode": False,
        "compact_sidebar": False
    }

    settings_data.clear()
    settings_data.update(default_settings)

    flash(
        "Settings have been reset to default.",
        "success"
    )

    return redirect(
        url_for("settings")
    )


@app.route(
    "/settings/change-password",
    methods=["POST"]
)
def change_password():

    global admin_credentials

    current_password = request.form.get(
        "current_password",
        ""
    )

    new_password = request.form.get(
        "new_password",
        ""
    )

    confirm_password = request.form.get(
        "confirm_password",
        ""
    )

    admin_credentials = load_admin_credentials()

    if current_password != admin_credentials["password"]:

        flash(
            "Current password is incorrect.",
            "danger"
        )

        return redirect(
            url_for("settings")
        )

    if len(new_password) < 6:

        flash(
            "New password must be at least 6 characters.",
            "danger"
        )

        return redirect(
            url_for("settings")
        )

    if new_password != confirm_password:

        flash(
            "New passwords do not match.",
            "danger"
        )

        return redirect(
            url_for("settings")
        )

    if new_password == current_password:

        flash(
            "New password must be different from the current password.",
            "danger"
        )

        return redirect(
            url_for("settings")
        )

    admin_credentials["password"] = new_password

    save_admin_credentials(admin_credentials)

    flash(
        "Password changed successfully.",
        "success"
    )

    return redirect(
        url_for("settings")
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)