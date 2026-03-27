# INDpay — Digital Payment Web App

A college project built with Flask and MySQL that simulates a digital payment system with blockchain-backed transaction logging.

---

## Features

- User registration & login with hashed passwords
- Send money between users
- Buy (add funds) from the bank
- Transaction history on dashboard
- Blockchain layer for transaction integrity
- Fully containerized with Docker

---

## Project Structure

```
indpay/
├── app.py               # Main Flask app — routes & logic
├── forms.py             # WTForms form definitions
├── blockchain.py        # Block & Blockchain classes
├── sqlhelpers.py        # DB helper utilities (legacy blockchain sync)
├── requirements.txt     # Python dependencies
├── init.sql             # DB schema + default admin user
│
├── Dockerfile           # Flask app container
├── docker-compose.yml   # Orchestrates Flask + MySQL
├── .dockerignore        # Files excluded from Docker build
├── .gitignore           # Files excluded from Git
│
├── templates/           # Jinja2 HTML templates
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── transection.html
│   ├── buy.html
│   └── includes/
│       ├── _messages.html
│       └── _formhelper.html
│
└── static/
    ├── css/             # Stylesheets
    ├── js/              # Chart.js and custom scripts
    └── images/          # Static images
```

---

## Quick Start (Docker — recommended)

> Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.

```bash
# 1. Clone or download the project
cd indpay

# 2. Build and start everything
docker compose up --build

# 3. Open in browser
http://localhost:5005
```

That's it. MySQL starts automatically, the schema is applied, and the Flask app connects to it.

---

## Default Admin Account

| Field    | Value           |
|----------|-----------------|
| Username | `admin`         |
| Password | `Admin@123`     |

Change the password after first login.

---

## Environment Variables

These are set in `docker-compose.yml`. Override them for production:

| Variable        | Default      | Description              |
|-----------------|--------------|--------------------------|
| `MYSQL_HOST`    | `mysql`      | DB hostname              |
| `MYSQL_USER`    | `indpay`     | DB username              |
| `MYSQL_PASSWORD`| `indpaypass` | DB password              |
| `MYSQL_DB`      | `INDpay`     | Database name            |
| `SECRET_KEY`    | `secret123`  | Flask session secret key |

---

## Useful Commands

```bash
# Start in background
docker compose up -d --build

# View logs
docker compose logs -f

# Stop containers
docker compose down

# Stop and delete all data (fresh start)
docker compose down -v
```

---

## Running Locally (without Docker)

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export MYSQL_HOST=localhost
export MYSQL_USER=root
export MYSQL_PASSWORD=yourpassword
export MYSQL_DB=INDpay

# Run the app
python app.py
```

Make sure MySQL is running locally and the schema from `init.sql` has been applied.

---

## Tech Stack

| Layer      | Technology          |
|------------|---------------------|
| Backend    | Python / Flask      |
| Database   | MySQL 8             |
| ORM/DB     | Flask-MySQLdb       |
| Forms      | WTForms             |
| Auth       | passlib (sha256)    |
| Frontend   | Jinja2 + Bootstrap  |
| Charts     | Chart.js            |
| Container  | Docker + Compose    |

<img width="1680" height="1050" alt="Image" src="https://github.com/user-attachments/assets/d65b79a6-9150-4894-975f-5a773ab45dc0" />

https://github.com/user-attachments/assets/7fa34d35-1878-4d15-aca5-65884bb42438


[INDpay.pptx](https://github.com/user-attachments/files/26297011/INDpay.pptx)
