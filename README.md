# Real-Time System Monitoring Service

This project is a backend service designed to monitor and display real-time system performance metrics (CPU, Memory, Network) from remote devices. It uses a modern, asynchronous architecture to collect data and stream it to a client dashboard via WebSockets.

## Key Features

- **Real-Time Metrics:** Pushes live system data to clients without polling.
- **Asynchronous Architecture:** Built with Django/ASGI, Celery, and Channels for a non-blocking, scalable, and efficient backend.
- **Secure API:** Uses `django-ninja` for a fast, modern REST API with JWT-based authentication for users and devices.
- **Multi-Device Monitoring:** Allows a single user to monitor multiple registered devices.
- **Background Data Collection:** Leverages Celery workers to handle long-running data collection tasks without impacting API responsiveness.

## Technology Stack

- **Backend:** Django 5
- **API:** Django Ninja
- **Asynchronous Tasks:** Celery
- **Real-time Communication:** Django Channels (WebSockets)
- **Message Broker:** Redis (for Celery)
- **Database:** SQLite (for development)
- **Dependency Management:** Pipenv

## Local Setup and Installation

Follow these steps to set up and run the project on your local machine.

### Prerequisites

- Python 3.10
- Pipenv
- Redis

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Install Dependencies

This project uses `pipenv` for dependency management. Install the required packages using:

```bash
pipenv install
pipenv shell
```

This will create a virtual environment and install all packages from the `Pipfile.lock`.

### 3. Configure Environment Variables

The project uses a `.env` file for configuration. Create a `.env` file in the `SysMonitor` directory (alongside `settings.py`):

```
SECRET_KEY='your-secret-django-key'
```

You can generate a new secret key using a Django secret key generator.

### 4. Run Database Migrations

Apply the database schema:

```bash
python SysMonitor/manage.py migrate
```

### 5. Start the Services

This application requires three separate services to be running concurrently: the Redis server, the Celery worker, and the Django development server.

**A. Start Redis**

Ensure your Redis server is running. If you installed it via a package manager like `brew` or `apt`, it may already be running as a service. Otherwise, start it manually:

```bash
redis-server
```

**B. Start the Celery Worker**

In a new terminal (inside the `pipenv shell`), start the Celery worker:

```bash
celery -A SysMonitor.celery worker -l info
```

**C. Start the Django Server**

In a third terminal (inside the `pipenv shell`), start the Django ASGI server:

```bash
python SysMonitor/manage.py runserver
```

The application should now be running at `http://127.0.0.1:8000`. You can interact with the API endpoints and establish WebSocket connections.
