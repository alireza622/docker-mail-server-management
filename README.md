# Mail Server Management System

A self-hosted mail server environment with Docker, Roundcube Webmail, and a custom Flask-based administration panel.

This project provides a complete environment for deploying and managing an email server using containerized services, together with a web-based administration interface for mailbox management.

---

## 🚀 Overview

The system is built around a Dockerized mail infrastructure and provides a custom administration panel for managing mail users and mailbox resources.

### Main Components

* Docker Mail Server
* Postfix
* Dovecot
* Roundcube Webmail
* Flask Administration Panel
* Docker Compose
* Persistent mail storage
* Mailbox quota management

---

## 🏗️ Architecture

```text
                    ┌──────────────────────┐
                    │      Administrator   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Flask Admin Panel  │
                    │      Port 5000       │
                    └──────────┬───────────┘
                               │
                         Docker CLI
                               │
                               ▼
              ┌────────────────────────────────┐
              │        Docker Mail Server      │
              │                                │
              │  Postfix     Dovecot           │
              │     │           │              │
              │     └──────┬────┘              │
              │            │                   │
              │       Mail Storage             │
              └────────────┬───────────────────┘
                           │
                           │ IMAP / SMTP
                           ▼
                    ┌──────────────────┐
                    │    Roundcube     │
                    │    Webmail       │
                    │    Port 8000     │
                    └──────────────────┘
```

---

## ✨ Features

### Administration Panel

The Flask administration panel provides:

* Administrator authentication
* Dashboard
* Mail server status monitoring
* Mailbox user management
* Create new mailbox
* Delete mailbox
* Change mailbox password
* Mailbox quota management
* Send restriction management
* Receive restriction management
* Mail server information
* Disk/storage monitoring

### Mail Server

The mail infrastructure provides:

* SMTP service through Postfix
* IMAP service through Dovecot
* Mailbox storage
* Mailbox quotas
* Docker-based deployment
* Persistent storage

### Webmail

Roundcube provides a browser-based email client for:

* Sending email
* Receiving email
* Reading messages
* Managing mailboxes

---

## 🐳 Docker Services

The project uses Docker Compose to manage the services.

### Mail Server

```text
Container: mailserver
Hostname:  mail.example.com
```

Exposed ports:

| Port | Service         |
| ---- | --------------- |
| 2525 | SMTP            |
| 587  | SMTP Submission |
| 993  | IMAPS           |

### Roundcube

```text
Container: roundcube
Port: 8000
```

Webmail:

```text
http://127.0.0.1:8000
```

---

## 🖥️ Administration Panel

The administration panel is developed using Flask.

Run the application from:

```text
admin-panel/
```

Start the Flask application:

```powershell
flask --app app run --port 5000
```

The administration panel will be available at:

```text
http://127.0.0.1:5000
```

---

## 👥 User Management

The administration panel allows administrators to:

### Create User

Create a new mailbox with:

* Email address
* Password
* Mailbox quota
* Send permission
* Receive permission

### Manage Existing Users

Administrators can:

* Change password
* Change quota
* Disable sending
* Enable sending
* Disable receiving
* Enable receiving
* Delete mailbox

---

## 💾 Storage

Mail data is stored using persistent Docker storage.

The project separates persistent runtime data from application source code.

Runtime mail data and logs are intentionally excluded from Git tracking.

```text
docker-data/
└── dms/
    ├── mail-data/
    ├── mail-state/
    ├── mail-logs/
    └── config/
```

Sensitive and runtime-generated mail data should not be committed to the repository.

---

## 📁 Project Structure

```text
mailserver/
│
├── README.md
├── .gitignore
├── docker-compose.yml
│
├── admin-panel/
│   ├── app.py
│   ├── mailserver.py
│   │
│   ├── templates/
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── users.html
│   │   └── add_user.html
│   │
│   └── static/
│
├── screenshots/
│   ├── login.JPG
│   ├── dash.JPG
│   ├── user.JPG
│   └── add-user.JPG
│
└── docker-data/
    └── dms/
```

---

## 🛠️ Technologies

* Python
* Flask
* Docker
* Docker Compose
* Postfix
* Dovecot
* Roundcube
* HTML5
* CSS3
* PowerShell
* Git

---

## 🔧 Installation

Clone the repository:

```powershell
git clone <repository-url>
cd mailserver
```

Start the Docker services:

```powershell
docker compose up -d
```

Check the running containers:

```powershell
docker ps
```

Expected services:

```text
mailserver
roundcube
```

---

## ▶️ Start Administration Panel

Move into the administration panel:

```powershell
cd admin-panel
```

Start Flask:

```powershell
flask --app app run --port 5000
```

Open:

```text
http://127.0.0.1:5000
```

---

## 📸 Screenshots

### Login

![Login](screenshots/login.JPG)

### Dashboard

![Dashboard](screenshots/dash.JPG)

### User Management

![User Management](screenshots/user.JPG)

### Create New User

![Create User](screenshots/add-user.JPG)

---

## 🔐 Security Notes

This repository is intended as a technical demonstration and development project.

The following data should never be committed to Git:

* Real mailbox passwords
* Administrator passwords
* Secret keys
* Private mail data
* Mail logs containing sensitive information
* Production credentials
* API keys

Use environment variables or a secure secret-management solution for production deployments.

---

## 📌 Current Status

The project currently provides a functional Dockerized mail server environment with:

* Mail server containers
* SMTP
* IMAP
* Roundcube Webmail
* Flask administration panel
* User management
* Password management
* Quota management
* Send/receive restrictions
* Storage monitoring
* Git-based source management

---

## 🎯 Project Goal

The goal of this project is to combine infrastructure administration and software development into a practical mail server management platform.

It demonstrates experience with:

```text
Linux / Docker Infrastructure
        +
Mail Server Administration
        +
Python / Flask Development
        +
Web Administration
        +
Git Version Control
```

---

## 📄 License

This project is provided for educational and development purposes.
