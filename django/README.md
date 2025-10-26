
# Python Exercises Django REST API

A comprehensive Django REST API implementing 5 Python practice exercises from Sun* - Talent & Product Incubator Vietnam Unit.

## 🎯 Exercises Implemented

1. **Student Grade Management System** - OOP-based student grade tracking with CRUD operations
2. **Overtime Calculator** - Calculate OT hours and meal allowances based on work schedule
3. **Vacation Days Calculator** - Calculate vacation days based on seniority
4. **Name Formatter** - Format Vietnamese names with initials
5. **Frequency Counter** - Count element occurrences and sort by frequency

## ✨ Features

- **Django REST Framework** with comprehensive API views
- **OpenAPI/Swagger** interactive documentation
- **SQLite database** (default) or MySQL support
- **Automated test suite** included
- **Clean code architecture** with serializers and viewsets
- **Environment-based configuration**

## Prerequisites

- Python 3.12+
- pip or uv package manager
- (Optional) MySQL database - SQLite is used by default

## 🚀 Quick Start (5 minutes)

```bash
# 1. Install dependencies
pip3 install -r requirements.txt

# 2. Run migrations
python3 src/manage.py migrate

# 3. Start the server
python3 src/manage.py runserver

# 4. Visit the interactive API documentation
# Open: http://127.0.0.1:8000/api/schema/swagger-ui/
```

## Installation

### Option 1: Using pip (Recommended)
```bash
cd /Users/phucnt/PycharmProjects/learning/django
pip3 install -r requirements.txt
```

### Option 2: Using uv (Fast Package Manager)
```bash
uv sync
```

## Environment Configuration

A `.env` file is already created with SQLite configuration (no setup needed!).

For MySQL, update `.env`:
```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database Configuration (MySQL)
DB_ENGINE=django.db.backends.mysql
DB_NAME=django_exercises
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

## Database Setup

### Using SQLite (Default - No Setup Required!)
The project is pre-configured with SQLite. Just run:
```bash
python3 src/manage.py migrate
```

### Using MySQL (Optional)
1. Create database:
```sql
CREATE DATABASE django_exercises CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Update `.env` with MySQL credentials

3. Install MySQL client:
```bash
pip3 install mysqlclient
```

4. Run migrations:
```bash
python3 src/manage.py migrate
```

## Running the Application

Start the development server:
```bash
python3 src/manage.py runserver
```

The API will be available at:
- **API Documentation**: `http://127.0.0.1:8000/api/schema/swagger-ui/` ⭐
- **API Base URL**: `http://127.0.0.1:8000/api/exercises/`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`
- **ReDoc**: `http://127.0.0.1:8000/api/schema/redoc/`

## 📚 API Documentation

The project includes comprehensive interactive documentation:

- **Swagger UI**: `http://127.0.0.1:8000/api/schema/swagger-ui/` - Interactive API testing
- **ReDoc**: `http://127.0.0.1:8000/api/schema/redoc/` - Beautiful API documentation
- **API_DOCUMENTATION.md** - Complete endpoint reference with examples

### Available Endpoints

**Exercise 1 - Student Management:**
- `POST /api/exercises/students/` - Create student
- `GET /api/exercises/students/` - List all students
- `GET /api/exercises/students/formatted_list/` - Formatted output
- `GET /api/exercises/students/highest_average/` - Get highest average
- `GET /api/exercises/students/top_students/` - Get top students

**Exercise 2 - Overtime Calculator:**
- `POST /api/exercises/overtime/` - Calculate OT hours and meal allowances

**Exercise 3 - Vacation Days:**
- `POST /api/exercises/vacation-days/` - Calculate vacation days

**Exercise 4 - Name Formatter:**
- `POST /api/exercises/format-name/` - Format Vietnamese names

**Exercise 5 - Frequency Counter:**
- `POST /api/exercises/frequency-counter/` - Count and sort elements

## 🧪 Testing

### Run Automated Test Suite
```bash
python3 test_all_exercises.py
```

### Test with curl
```bash
# Create a student
curl -X POST http://127.0.0.1:8000/api/exercises/students/ \
  -H "Content-Type: application/json" \
  -d '{"name": "ngoc", "math_grade": 3, "literature_grade": 4, "english_grade": 5}'

# Calculate overtime
curl -X POST http://127.0.0.1:8000/api/exercises/overtime/ \
  -H "Content-Type: application/json" \
  -d '{"check_in": "08:00", "check_out": "18:00"}'
```

## 📁 Project Structure

```
django/
├── src/
│   ├── core/                    # Django project settings
│   │   ├── settings.py          # Main settings file
│   │   ├── urls.py              # Root URL configuration
│   │   ├── wsgi.py              # WSGI configuration
│   │   └── asgi.py              # ASGI configuration
│   ├── exercises/               # Exercises app
│   │   ├── models.py            # Student model
│   │   ├── views.py             # API views for all exercises
│   │   ├── serializers.py       # DRF serializers
│   │   ├── urls.py              # App URL patterns
│   │   └── admin.py             # Django admin configuration
│   └── manage.py                # Django management script
├── .env                         # Environment variables
├── requirements.txt             # Python dependencies
├── pyproject.toml               # Project metadata
├── README.md                    # This file
├── QUICKSTART.md                # 5-minute setup guide
├── SETUP_GUIDE.md               # Detailed setup instructions
├── API_DOCUMENTATION.md         # Complete API reference
└── test_all_exercises.py        # Automated test suite
```

## Development

### Running Django Tests

```bash
python3 src/manage.py test
```

### Making Model Changes

When you modify models:

```bash
python3 src/manage.py makemigrations
python3 src/manage.py migrate
```

### Django Shell

```bash
python3 src/manage.py shell
```

### Create Superuser

```bash
python3 src/manage.py createsuperuser
```

## 📖 Documentation

- **QUICKSTART.md** - Get started in 5 minutes
- **SETUP_GUIDE.md** - Detailed setup instructions with troubleshooting
- **API_DOCUMENTATION.md** - Complete API reference with curl and Python examples
- **Swagger UI** - Interactive API testing at `/api/schema/swagger-ui/`

## 🎓 Learning Resources

This project demonstrates:
- Django REST Framework best practices
- Clean architecture with serializers and viewsets
- OpenAPI/Swagger documentation
- Model design with computed properties
- Input validation and error handling
- Custom API views and actions
- Django admin configuration

## 🤝 Contributing

Feel free to:
1. Add more exercises
2. Improve documentation
3. Add unit tests
4. Enhance error handling
5. Add authentication/authorization

## 📝 License

This project is licensed under the MIT License.

---

**Built for Sun* Python Practice Exercises** | Django 5.0 | DRF | SQLite/MySQL