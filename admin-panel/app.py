from flask import Flask, render_template, redirect, url_for, session, request
from functools import wraps
import os

from mailserver import (
    get_users,
    get_quota,
    add_user,
    set_quota,
    delete_user,
    update_password,
    restrict_send,
    allow_send,
    restrict_receive,
    allow_receive,
    get_server_status
)


app = Flask(__name__)


app.secret_key = os.environ.get(
    "ADMIN_SECRET_KEY",
    "change-this-secret-key"
)


ADMIN_USERNAME = os.environ.get(
    "ADMIN_USERNAME",
    "admin"
)


ADMIN_PASSWORD = os.environ.get(
    "ADMIN_PASSWORD",
    "admin123"
)


# =========================================================
# Authentication
# =========================================================

def login_required(view):

    @wraps(view)
    def wrapped_view(*args, **kwargs):

        if "admin_logged_in" not in session:

            return redirect(
                url_for("login")
            )

        return view(*args, **kwargs)

    return wrapped_view


# =========================================================
# Home
# =========================================================

@app.route("/")
def index():

    if "admin_logged_in" in session:

        return redirect(
            url_for("dashboard")
        )

    return redirect(
        url_for("login")
    )


# =========================================================
# Login
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    error = None

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        if (
            username == ADMIN_USERNAME
            and password == ADMIN_PASSWORD
        ):

            session["admin_logged_in"] = True

            session["admin_username"] = username

            return redirect(
                url_for("dashboard")
            )

        error = (
            "نام کاربری یا رمز عبور اشتباه است."
        )

    return render_template(
        "login.html",
        error=error
    )


# =========================================================
# Logout
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# =========================================================
# Dashboard
# =========================================================

@app.route("/dashboard")
@login_required
def dashboard():

    error = None
    server = {}

    try:

        server = get_server_status()

    except Exception as e:

        error = str(e)

    return render_template(
        "dashboard.html",
        admin_username=session.get(
            "admin_username"
        ),
        server=server,
        error=error
    )


# =========================================================
# Users
# =========================================================

@app.route("/users")
@login_required
def users():

    users_list = []

    error = None

    try:

        users_list = get_users()

        users_data = []

        for email in users_list:

            try:

                quota = get_quota(
                    email
                )

            except Exception:

                quota = {
                    "used_kb": 0,
                    "limit_kb": 0,
                    "used_mb": 0,
                    "limit_mb": None,
                    "percentage": 0
                }

            users_data.append(
                {
                    "email": email,
                    "quota": quota
                }
            )

    except Exception as e:

        error = str(e)

        users_data = []

    return render_template(
        "users.html",
        users=users_data,
        error=error
    )


# =========================================================
# Add User
# =========================================================

@app.route(
    "/users/add",
    methods=["GET", "POST"]
)
@login_required
def add_user_page():

    error = None
    success = None

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        quota = request.form.get(
            "quota",
            ""
        ).strip()

        quota_unit = request.form.get(
            "quota_unit",
            "M"
        )

        receive = request.form.get(
            "receive"
        )

        send = request.form.get(
            "send"
        )

        if not email:

            error = (
                "آدرس ایمیل را وارد کنید."
            )

        elif not password:

            error = (
                "رمز عبور را وارد کنید."
            )

        elif "@" not in email:

            error = (
                "آدرس ایمیل معتبر نیست."
            )

        else:

            try:

                add_user(
                    email,
                    password
                )

                if quota:

                    set_quota(
                        email,
                        f"{quota}{quota_unit}"
                    )

                if not send:

                    restrict_send(
                        email
                    )

                if not receive:

                    restrict_receive(
                        email
                    )

                success = (
                    f"کاربر {email} "
                    "با موفقیت ایجاد شد."
                )

            except Exception as e:

                error = str(e)

    return render_template(
        "add_user.html",
        error=error,
        success=success
    )


# =========================================================
# Set Quota
# =========================================================

@app.route(
    "/users/quota",
    methods=["POST"]
)
@login_required
def quota_user():

    email = request.form.get(
        "email",
        ""
    ).strip()

    quota = request.form.get(
        "quota",
        ""
    ).strip()

    quota_unit = request.form.get(
        "quota_unit",
        "M"
    )

    try:

        if email and quota:

            set_quota(
                email,
                f"{quota}{quota_unit}"
            )

    except Exception as e:

        print(
            f"Quota error: {e}"
        )

    return redirect(
        url_for("users")
    )


# =========================================================
# Change Password
# =========================================================

@app.route(
    "/users/password",
    methods=["POST"]
)
@login_required
def change_password():

    email = request.form.get(
        "email",
        ""
    ).strip()

    password = request.form.get(
        "password",
        ""
    )

    try:

        if email and password:

            update_password(
                email,
                password
            )

    except Exception as e:

        print(
            f"Password error: {e}"
        )

    return redirect(
        url_for("users")
    )


# =========================================================
# Delete User
# =========================================================

@app.route(
    "/users/delete",
    methods=["POST"]
)
@login_required
def delete_user_page():

    email = request.form.get(
        "email",
        ""
    ).strip()

    try:

        if email:

            delete_user(
                email
            )

    except Exception as e:

        print(
            f"Delete error: {e}"
        )

    return redirect(
        url_for("users")
    )


# =========================================================
# Send
# =========================================================

@app.route(
    "/users/send",
    methods=["POST"]
)
@login_required
def user_send():

    email = request.form.get(
        "email",
        ""
    ).strip()

    action = request.form.get(
        "action",
        ""
    )

    try:

        if action == "disable":

            restrict_send(
                email
            )

        elif action == "enable":

            allow_send(
                email
            )

    except Exception as e:

        print(
            f"Send error: {e}"
        )

    return redirect(
        url_for("users")
    )


# =========================================================
# Receive
# =========================================================

@app.route(
    "/users/receive",
    methods=["POST"]
)
@login_required
def user_receive():

    email = request.form.get(
        "email",
        ""
    ).strip()

    action = request.form.get(
        "action",
        ""
    )

    try:

        if action == "disable":

            restrict_receive(
                email
            )

        elif action == "enable":

            allow_receive(
                email
            )

    except Exception as e:

        print(
            f"Receive error: {e}"
        )

    return redirect(
        url_for("users")
    )


# =========================================================
# Start
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )