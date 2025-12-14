# DHCP Lease Manager

Django web application for viewing and managing DHCP leases from Kea DHCP server stored in PostgreSQL.

## Features

- View DHCP lease information from Kea database
- Sort leases by hostname, IP address, MAC address, subnet, or expiration time
- Delete individual leases
- User authentication system
- Auto-refresh every 30 seconds
- Bootstrap UI

## Prerequisites

- Docker and Docker Compose
- PostgreSQL database with Kea DHCP lease data
- Python 3.x (if running without Docker)

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <repository-name>
```

### 2. Configure environment variables

Copy the example environment file and edit it with your credentials:

```bash
cp .env.example .env
```

Edit `.env` and set the following variables:

```
POSTGRES_NAME=your_database_name
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=your_postgres_host
POSTGRES_PORT=5432

DJANGO_SECRET_KEY=your-secret-key-here
ALLOWED_HOST=yourdomain.com|localhost
DEBUG=True
```

**Generate a new Django secret key:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 3. Build and start the application

```bash
docker-compose up -d --build
```

### 4. Run migrations

```bash
docker exec -it django-web-1 python manage.py migrate
```

### 5. Create a superuser

```bash
docker exec -it django-web-1 python manage.py createsuperuser
```

Follow the prompts to create your admin user.

### 6. Access the application

Open your browser and navigate to:
- Main application: `http://localhost:8800/leases/`
- Login page: `http://localhost:8800/login/`
- Admin panel: `http://localhost:8800/admin/`

## Project Structure

```
.
├── dhcplease/          # Django project configuration
│   ├── settings.py     # Main settings
│   ├── urls.py         # URL routing
│   └── wsgi.py         # WSGI configuration
├── lease4/             # Django app for lease management
│   ├── models.py       # Database models
│   ├── views.py        # View functions
│   ├── urls.py         # App URL routing
│   └── templates/      # HTML templates
├── docker-compose.yaml # Docker Compose configuration
├── Dockerfile          # Docker image definition
├── requirements.txt    # Python dependencies
└── manage.py           # Django management script
```

## Security Notes

- Never commit the `.env` file to version control
- Always use strong passwords for database and Django secret key
- Set `DEBUG=False` in production environments
- Update `ALLOWED_HOST` with your actual domain names
- Ensure PostgreSQL is not publicly accessible

## Development

To run in development mode:

```bash
docker-compose up
```

To view logs:

```bash
docker-compose logs -f
```

To stop the application:

```bash
docker-compose down
```

## License

[Your License Here]
