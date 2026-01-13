# Event Management API

A comprehensive Django REST Framework API for managing events with user authentication, CRUD operations, and event registration functionality.

## Features

- **User Authentication**: Secure registration and login system
- **Event Management**: Complete CRUD operations with permission controls
- **Event Registration**: Users can register/unregister for events with capacity management
- **Search & Filtering**: Filter events by title, location, and date range
- **API Documentation**: Interactive Swagger and ReDoc documentation
- **Admin Interface**: Django admin panel for management
- **Pagination**: Efficient handling of large datasets

## Technology Stack

- **Backend**: Django 4.1.13, Django REST Framework 3.14.0
- **Database**: SQLite (development) / PostgreSQL (production)
- **Documentation**: drf-yasg (Swagger/OpenAPI)
- **Authentication**: Django Session Authentication

## Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ajok-2022/alx_backend_Capstone.git
   cd alx_backend_Capstone
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

3. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - API Home: http://127.0.0.1:8000/
   - Swagger Documentation: http://127.0.0.1:8000/swagger/
   - ReDoc Documentation: http://127.0.0.1:8000/redoc/
   - Admin Panel: http://127.0.0.1:8000/admin/

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | User registration |
| POST | `/api/auth/login/` | User login |
| GET/PUT | `/api/auth/profile/` | User profile management |

### Events
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/events/` | List all events (with filtering) |
| POST | `/api/events/` | Create new event |
| GET | `/api/events/{id}/` | Get event details |
| PUT | `/api/events/{id}/` | Update event (organizer only) |
| DELETE | `/api/events/{id}/` | Delete event (organizer only) |
| GET | `/api/events/upcoming/` | List upcoming events |
| GET | `/api/events/my-events/` | List user's created events |
| POST | `/api/events/{id}/register/` | Register for event |
| DELETE | `/api/events/{id}/unregister/` | Unregister from event |

## API Usage Examples

### Register a New User
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123"
  }'
```

### Create an Event
```bash
curl -X POST http://127.0.0.1:8000/api/events/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Tech Conference 2024",
    "description": "Annual technology conference",
    "date_time": "2024-12-15T10:00:00Z",
    "location": "Convention Center",
    "capacity": 100
  }'
```

### Filter Events
```bash
# Filter by title and location
curl "http://127.0.0.1:8000/api/events/?title=tech&location=center"

# Get upcoming events only
curl "http://127.0.0.1:8000/api/events/upcoming/"
```

## Query Parameters

### Event Filtering
- `title` - Filter by title (case-insensitive)
- `location` - Filter by location (case-insensitive)
- `date_from` - Filter events from date (YYYY-MM-DD HH:MM)
- `date_to` - Filter events to date (YYYY-MM-DD HH:MM)

### Pagination
- `page` - Page number
- `page_size` - Items per page (default: 20)

## Data Models

### Event Model
```python
{
  "id": 1,
  "title": "Event Title",
  "description": "Event description",
  "date_time": "2024-12-15T10:00:00Z",
  "location": "Event Location",
  "organizer": "username",
  "capacity": 100,
  "available_spots": 85,
  "is_full": false,
  "is_upcoming": true,
  "created_date": "2024-01-01T12:00:00Z"
}
```

### User Registration
```python
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "securepassword123"
}
```

## Business Rules

- Events must have future dates
- Capacity must be greater than 0
- Users can only modify their own events
- Users cannot register for their own events
- Users cannot register for full events
- Users cannot register for past events
- Duplicate registrations are prevented

## Interactive Documentation

The API includes comprehensive interactive documentation:

- **Swagger UI**: `/swagger/` - Test endpoints directly in the browser
- **ReDoc**: `/redoc/` - Clean, responsive API documentation

Both interfaces provide:
- Complete endpoint documentation
- Request/response schemas
- Interactive testing capabilities
- Authentication support

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Contact

- **Author**: Ajok Kuech Ajok Deng
- **Email**: ajokkuechajokdeng@gmail.com
- **GitHub**: [Ajok-2022](https://github.com/Ajok-2022)