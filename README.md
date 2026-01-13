# Event Management API

A Django REST Framework API for managing events with user authentication, CRUD operations, and event registration functionality.

## Features

- User registration and JWT authentication
- Event CRUD operations with permission controls
- Event registration/unregistration system
- Capacity management with validation
- Search and filtering by title, location, and date range
- Pagination for large datasets
- Upcoming events filtering
- Admin interface for management

## API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login (JWT token)
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `GET/PUT /api/auth/profile/` - User profile

### Events
- `GET /api/events/` - List all events (with filtering)
- `POST /api/events/` - Create new event
- `GET /api/events/{id}/` - Get event details
- `PUT /api/events/{id}/` - Update event (organizer only)
- `DELETE /api/events/{id}/` - Delete event (organizer only)
- `GET /api/events/upcoming/` - List upcoming events
- `GET /api/events/my-events/` - List user's created events
- `POST /api/events/{id}/register/` - Register for event
- `DELETE /api/events/{id}/unregister/` - Unregister from event

## Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run development server:**
   ```bash
   python manage.py runserver
   ```

## Query Parameters

### Event Filtering
- `title` - Filter by title (case-insensitive)
- `location` - Filter by location (case-insensitive)
- `date_from` - Filter events from date (YYYY-MM-DD HH:MM)
- `date_to` - Filter events to date (YYYY-MM-DD HH:MM)
- `upcoming` - Filter upcoming events (true/false)

### Pagination
- `page` - Page number
- `page_size` - Items per page (default: 20)

## Example Usage

### Register User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "testpass123"}'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

### Create Event
```bash
curl -X POST http://localhost:8000/api/events/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Tech Conference 2024",
    "description": "Annual technology conference",
    "date_time": "2024-06-15T10:00:00Z",
    "location": "Convention Center",
    "capacity": 100
  }'
```

### Get Upcoming Events
```bash
curl -X GET "http://localhost:8000/api/events/upcoming/?title=tech&location=center" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Deployment

### Heroku
1. Create Heroku app: `heroku create your-app-name`
2. Set environment variables:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set DEBUG=False
   ```
3. Deploy: `git push heroku main`
4. Run migrations: `heroku run python manage.py migrate`

### PythonAnywhere
1. Upload code to PythonAnywhere
2. Set up virtual environment and install requirements
3. Configure WSGI file to point to `event_management.wsgi`
4. Set environment variables in WSGI file
5. Run migrations via console

## Models

### Event
- `title` - Event title (required)
- `description` - Event description
- `date_time` - Event date and time (required, must be future)
- `location` - Event location (required)
- `organizer` - Event creator (auto-set)
- `capacity` - Maximum attendees (required, > 0)
- `created_date` - Creation timestamp (auto-set)

### EventRegistration
- `user` - Registered user
- `event` - Event being registered for
- `registered_at` - Registration timestamp

## Validation Rules

- Events must have future dates
- Capacity must be greater than 0
- Users can only modify their own events
- Users cannot register for their own events
- Users cannot register for full events
- Users cannot register for past events
- Duplicate registrations are prevented

## Technology Stack

- Django 4.2.7
- Django REST Framework 3.14.0
- JWT Authentication
- SQLite (development) / PostgreSQL (production)
- Django Filters for search/filtering
- WhiteNoise for static files
- Gunicorn for production server