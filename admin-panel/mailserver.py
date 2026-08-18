import subprocess

CONTAINER_NAME = "mailserver"
ROUNDCUBE_CONTAINER = "roundcube"


def run_setup_command(*args):
    command = ["docker", "exec", CONTAINER_NAME, "setup", *args]
    result = subprocess.run(command, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "Mailserver command failed")
    return result.stdout.strip()


def run_docker_command(*args):
    command = ["docker", "exec", CONTAINER_NAME, *args]
    result = subprocess.run(command, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "Docker command failed")
    return result.stdout.strip()


def run_host_docker_command(*args):
    command = ["docker", *args]
    result = subprocess.run(command, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "Docker command failed")
    return result.stdout.strip()


# =========================================================
# Users
# =========================================================

def get_users():
    output = run_setup_command("email", "list")
    users = []
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("*"):
            line = line[1:].strip()
        if "@" in line:
            email = line.split("(")[0].strip()
            if email and email not in users:
                users.append(email)
    return users


def add_user(email, password):
    return run_setup_command("email", "add", email, password)


def delete_user(email):
    return run_setup_command("email", "del", email)


def update_password(email, password):
    return run_setup_command("email", "update", email, password)


# =========================================================
# Quota
# =========================================================

def set_quota(email, quota):
    return run_setup_command("quota", "set", email, quota)


def get_quota(email):
    output = run_docker_command("doveadm", "quota", "get", "-u", email)
    used_kb = 0
    limit_kb = 0
    percentage = 0

    for line in output.splitlines():
        line = line.strip()
        if not line.startswith("User quota STORAGE"):
            continue
        parts = line.split()
        try:
            used_kb = int(parts[3])
            limit_kb = int(parts[4])
            if limit_kb > 0:
                percentage = round((used_kb / limit_kb) * 100, 1)
        except (ValueError, IndexError):
            pass

    return {
        "used_kb": used_kb,
        "limit_kb": limit_kb,
        "used_mb": round(used_kb / 1024, 2),
        "limit_mb": round(limit_kb / 1024, 2) if limit_kb > 0 else None,
        "percentage": percentage,
    }


# =========================================================
# Send / Receive restrictions
# =========================================================

def restrict_send(email):
    return run_setup_command("email", "restrict", "add", "send", email)


def allow_send(email):
    return run_setup_command("email", "restrict", "del", "send", email)


def restrict_receive(email):
    return run_setup_command("email", "restrict", "add", "receive", email)


def allow_receive(email):
    return run_setup_command("email", "restrict", "del", "receive", email)


# =========================================================
# Server status
# =========================================================

def _container_running(container_name):
    try:
        output = run_host_docker_command(
            "inspect", "-f", "{{.State.Running}}", container_name
        )
        return output.strip().lower() == "true"
    except Exception:
        return False


def _mail_service_running(service):
    try:
        output = run_docker_command("sh", "-c", f"pgrep -x {service} >/dev/null && echo running || echo stopped")
        return output.strip() == "running"
    except Exception:
        return False


def _disk_status():
    try:
        output = run_docker_command("df", "-h", "/")
        lines = output.splitlines()
        if len(lines) < 2:
            return {}
        parts = lines[-1].split()
        if len(parts) >= 5:
            return {
                "filesystem": parts[0],
                "size": parts[1],
                "used": parts[2],
                "available": parts[3],
                "percentage": parts[4],
            }
    except Exception:
        pass
    return {}


def get_server_status():
    mailserver_running = _container_running(CONTAINER_NAME)
    roundcube_running = _container_running(ROUNDCUBE_CONTAINER)

    hostname = ""
    domain = ""
    protocols = ""

    if mailserver_running:
        try:
            hostname = run_docker_command("postconf", "-h", "myhostname")
        except Exception:
            hostname = "unknown"
        try:
            domain = run_docker_command("postconf", "-h", "mydomain")
        except Exception:
            domain = "unknown"
        try:
            protocols = run_docker_command("doveconf", "-h", "protocols")
        except Exception:
            protocols = "unknown"

    try:
        user_count = len(get_users()) if mailserver_running else 0
    except Exception:
        user_count = 0

    return {
        "mailserver": "running" if mailserver_running else "stopped",
        "roundcube": "running" if roundcube_running else "stopped",
        "hostname": hostname,
        "domain": domain,
        "protocols": protocols,
        "postfix": "running" if mailserver_running and _mail_service_running("master") else "stopped",
        "dovecot": "running" if mailserver_running and _mail_service_running("dovecot") else "stopped",
        "disk": _disk_status(),
        "user_count": user_count,
    }
