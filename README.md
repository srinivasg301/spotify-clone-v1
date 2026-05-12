# Spotify Clone - Modular Architecture

A production-ready Spotify-like application built with **modular architecture** and **use case pattern**.

## 🏗️ Architecture Overview

```
spotify-clone/
├── app/
│   ├── core/              # Infrastructure layer
│   ├── shared/            # Reusable components
│   └── modules/           # Business modules
│       ├── auth/          # Authentication & authorization
│       ├── artist/        # Artist management
│       └── song/          # Song management
```

### Architecture Pattern: **Modular + Use Cases**

- **Core**: Infrastructure (database, config, security)
- **Shared**: Reusable components (base repository, schemas)
- **Modules**: Independent business domains
- **Use Cases**: Single-responsibility business operations

---

## 🎯 Key Features

✅ **Modular Architecture** - Independent, scalable modules  
✅ **Use Case Pattern** - Single-responsibility business logic  
✅ **Clean Separation** - Core, Shared, Modules  
✅ **JWT Authentication** - Secure token-based auth  
✅ **Role-Based Access** - User/Admin permissions  
✅ **API Versioning** - `/api/v1/` prefix  
✅ **Type Safety** - Pydantic v2 validation  
✅ **Production Ready** - Exception handling, logging  

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL running on localhost:5432

### 1. Setup Database

```sql
CREATE DATABASE spotify_db;
```

### 2. Install Dependencies

```bash
cd spotify-clone
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 4. Run Application

```bash
uvicorn app.main:app --reload --port 8000
```

### 5. Access API

- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 📋 API Endpoints

### Authentication (`/api/v1/auth`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/register` | Register new user | Public |
| POST | `/token` | Login (OAuth2) | Public |
| POST | `/refresh` | Refresh access token | Public |
| POST | `/verify` | Verify token | Internal |

### Artists (`/api/v1/artists`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | List artists | User |
| GET | `/search` | Search artists | User |
| GET | `/{id}` | Get artist | User |
| GET | `/{id}/songs` | Get artist songs | User |
| POST | `/` | Create artist | Admin |
| PUT | `/{id}` | Update artist | Admin |
| DELETE | `/{id}` | Delete artist | Admin |

### Songs (`/api/v1/songs`)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/` | List songs | User |
| GET | `/search` | Search songs | User |
| GET | `/{id}` | Get song | User |
| GET | `/{id}/stream` | Get stream URL | User |
| POST | `/` | Create song | Admin |
| PUT | `/{id}` | Update song | Admin |
| DELETE | `/{id}` | Delete song | Admin |

---

## 🔐 Authentication Flow

### 1. Register User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@test.com",
    "password": "admin123",
    "role": "admin"
  }'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/token \
  -F "username=admin" \
  -F "password=admin123"
```

Response:
```json
{
  "success": true,
  "data": {
    "access_token": "eyJ...",
    "refresh_token": "eyJ...",
    "token_type": "bearer"
  }
}
```

### 3. Use API with Token

```bash
curl -X GET http://localhost:8000/api/v1/artists \
  -H "Authorization: Bearer <access_token>"
```

---

## 🏛️ Architecture Details

### Module Structure

Each module follows the same pattern:

```
modules/artist/
├── models.py          # SQLAlchemy models
├── schemas.py         # Pydantic DTOs
├── repository.py      # Data access layer
├── service.py         # Use case orchestration
├── router.py          # FastAPI endpoints
└── use_cases/         # Business logic
    ├── create_artist.py
    ├── update_artist.py
    ├── delete_artist.py
    ├── list_artists.py
    ├── get_artist.py
    ├── search_artists.py
    └── get_artist_songs.py
```

### Request Flow

```
Client Request
    ↓
Router (FastAPI endpoint)
    ↓
Service (orchestrates use cases)
    ↓
Use Case (business logic)
    ↓
Repository (data access)
    ↓
Database
```

### Benefits

| Aspect | Benefit |
|--------|---------|
| **Modularity** | Add/remove modules independently |
| **Testability** | Test use cases in isolation |
| **Maintainability** | Changes localized to modules |
| **Scalability** | Easy to split into microservices |
| **Clarity** | Clear separation of concerns |

---

## 🧪 Testing

### Test Suite Overview

**Total Tests: 182** | **Coverage: 93%** ✅

| Module | Tests | Coverage | Status |
|--------|-------|----------|--------|
| **Auth** | 47 tests | 98% | ✅ Excellent |
| **Artist** | 50 tests | 100% | ✅ Perfect |
| **Song** | 54 tests | 95% | ✅ Excellent |
| **Core** | 23 tests | 93% | ✅ Excellent |
| **Shared** | 8 tests | 45% | ⚠️ Utilities |

### Test Structure

```
tests/
├── core/                      # Core infrastructure tests
│   ├── test_security.py       # JWT, password hashing
│   └── test_exceptions.py     # Custom exceptions
├── factories/                 # Test data factories
│   ├── user_factory.py
│   ├── artist_factory.py
│   ├── song_factory.py
│   └── refresh_token_factory.py
├── modules/                   # Module-specific tests
│   ├── auth/
│   │   ├── conftest.py        # Auth fixtures
│   │   ├── test_auth_schemas.py
│   │   ├── test_auth_service.py
│   │   ├── test_auth_repository.py
│   │   ├── test_auth_routes.py
│   │   └── test_auth_use_cases.py
│   ├── artist/
│   │   ├── conftest.py
│   │   ├── test_artist_schemas.py
│   │   ├── test_artist_service.py
│   │   ├── test_artist_repository.py
│   │   ├── test_artist_routes.py
│   │   └── test_artist_use_cases.py
│   └── song/
│       ├── conftest.py
│       ├── test_song_schemas.py
│       ├── test_song_service.py
│       ├── test_song_repository.py
│       ├── test_song_routes.py
│       └── test_song_use_cases.py
└── conftest.py                # Global test fixtures
```

### Running Tests

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific module tests
pytest tests/modules/auth/ -v
pytest tests/modules/artist/ -v
pytest tests/modules/song/ -v

# Run specific test file
pytest tests/modules/auth/test_auth_schemas.py -v

# Run specific test class
pytest tests/modules/auth/test_auth_use_cases.py::TestRegisterUserUseCase -v

# Run specific test function
pytest tests/modules/auth/test_auth_use_cases.py::TestRegisterUserUseCase::test__register_user__with_valid_data__creates_user_successfully -v

# Stop on first failure
pytest -x

# Run tests in parallel (faster)
pip install pytest-xdist
pytest -n auto
```

### Code Coverage

```bash
# Run tests with coverage report
pytest --cov=app --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=app --cov-report=html

# Open HTML report
start htmlcov\index.html  # Windows
open htmlcov/index.html   # macOS
xdg-open htmlcov/index.html  # Linux

# Coverage for specific module
pytest tests/modules/auth/ --cov=app.modules.auth --cov-report=term-missing

# Fail if coverage below threshold
pytest --cov=app --cov-fail-under=90
```

### Test Markers

```bash
# Run only unit tests
pytest -m unit

# Run only slow tests
pytest -m slow

# Skip slow tests
pytest -m "not slow"
```

### Test Standards

All tests follow strict playbook standards:

✅ **AAA Pattern**: Arrange, Act, Assert with comment labels  
✅ **Naming Convention**: `test__{unit}__{condition}__{expected_result}`  
✅ **Factory Pattern**: Test data generated with factory-boy + Faker  
✅ **Mocking**: All dependencies mocked with `spec=` parameter  
✅ **No I/O**: Pure unit tests with no database or network calls  
✅ **Comprehensive**: Both success and error paths tested  
✅ **Deterministic**: Faker.seed(42) for reproducible tests

---

## 📦 Tech Stack

### Production Dependencies

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0
- **Authentication**: JWT (python-jose)
- **Password Hashing**: Passlib with bcrypt
- **Validation**: Pydantic v2
- **Server**: Uvicorn

### Development Dependencies

- **Testing**: pytest >= 8.0
- **Coverage**: pytest-cov >= 5.0
- **Async Testing**: pytest-asyncio >= 0.23
- **Test Randomization**: pytest-randomly >= 3.15
- **Test Data**: factory-boy >= 3.3, Faker >= 25.0
- **Time Mocking**: freezegun >= 1.4
- **HTTP Mocking**: respx >= 0.20

### Installation

```bash
# Production dependencies only
pip install -r requirements.txt

# Development dependencies (includes production)
pip install -r requirements.txt -r requirements-dev.txt
```

---

## 🔄 Migration from Old Structure

### Old (MVC/Layered)
```
app/
├── api/          # All routes
├── services/     # All business logic
├── repositories/ # All data access
└── models/       # All models
```

### New (Modular)
```
app/
├── core/         # Infrastructure
├── shared/       # Reusable
└── modules/      # Independent domains
    ├── auth/
    ├── artist/
    └── song/
```

### Key Differences

| Aspect | Old | New |
|--------|-----|-----|
| **Organization** | By layer | By feature |
| **Changes** | Touch multiple layers | Touch one module |
| **Testing** | Complex mocking | Simple, focused |
| **Scalability** | Monolithic | Modular |

---

## 📝 Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/spotify_db

# JWT
SECRET_KEY=your-secret-key-min-32-chars
ACCESS_TOKEN_EXPIRE_MINUTES=20
REFRESH_TOKEN_EXPIRE_DAYS=7

# Application
DEBUG=False
ALLOWED_ORIGINS=http://localhost:3000
```

---

## 🚢 Deployment

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt -r requirements-dev.txt

# Run application
uvicorn app.main:app --reload --port 8000

# Run tests
pytest

# Check coverage
pytest --cov=app --cov-report=html
```

### Docker (Coming Soon)

```bash
docker-compose up
```

### Production Checklist

- [ ] Change `SECRET_KEY` in production (min 32 characters)
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_ORIGINS`
- [ ] Use production database with connection pooling
- [ ] Enable HTTPS/TLS
- [ ] Setup structured logging
- [ ] Configure monitoring and alerting
- [ ] Run database migrations
- [ ] Setup backup strategy
- [ ] Configure rate limiting
- [ ] Enable CORS properly
- [ ] Use environment-specific configs

---

## 📚 Documentation

- **API Docs**: `/docs` (Swagger UI)
- **Alternative Docs**: `/redoc` (ReDoc)
- **Architecture**: See `ARCHITECTURE.md` (coming soon)

---

## 🤝 Contributing

1. Follow the module structure
2. Write use cases for business logic
3. Add tests for new features
4. Update documentation

---

## 📄 License

MIT

---

## 🎓 Learning Resources

- **FastAPI**: https://fastapi.tiangolo.com
- **SQLAlchemy 2.0**: https://docs.sqlalchemy.org
- **Pydantic v2**: https://docs.pydantic.dev
- **Clean Architecture**: https://blog.cleancoder.com

---

**Built with ❤️ using Modular Architecture**
