# Challenges & Solutions

Bugs, errors, and fixes encountered while building the Spotify Clone with modular architecture.

---

## 🐛 Bug #1: Generator Type Hint Error

**Error:** `Return type of generator function must be compatible with "Generator[Any, Any, Any]"`

**Location:** `app/core/database.py:29`

**Cause:** Used `-> Session` instead of `-> Generator[Session, None, None]` for a function with `yield`

**Fix:**
```python
from typing import Generator

def get_db() -> Generator[Session, None, None]:  # Changed from -> Session
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## 🐛 Bug #2: Pydantic CORS Parsing Error

**Error:** `error parsing value for field "allowed_origins" from source "DotEnvSettingsSource"`

**Location:** `app/core/config.py:36`

**Cause:** Type annotation was `str` but validator returned `list`

**Fix:**
```python
allowed_origins: list[str] = Field(default=["http://localhost:3000"])

@field_validator("allowed_origins", mode="before")
@classmethod
def parse_cors(cls, v):
    if isinstance(v, str):
        return [origin.strip() for origin in v.split(",")]
    return v
```

**Alternative:** Removed `ALLOWED_ORIGINS` from `.env` to use default value

---

## 🐛 Bug #3: Verbose API Responses

**Issue:** Responses included unnecessary audit fields (created_at, updated_at, created_by, updated_by)

**Fix:** Removed audit fields from response schemas

```python
# Before
class ArtistResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    created_by: str | None
    updated_by: str | None

# After
class ArtistResponse(BaseModel):
    id: int
    name: str
```

---

## 🎯 Architecture Decisions

### **1. MVC → Modular Architecture**
- **Problem:** Code scattered across layers, hard to maintain
- **Solution:** Organized by feature/domain instead of technical layer
- **Benefit:** Changes localized to single module

### **2. Merged Two Services into One**
- **Problem:** Separate auth and main services required HTTP calls
- **Solution:** Single service with auth as a module
- **Benefit:** Simpler deployment, faster, easier testing

### **3. Use Case Pattern**
- **Problem:** Service classes had multiple responsibilities
- **Solution:** Split into individual use cases (one operation each)
- **Benefit:** Better testability, single responsibility

---

## 🔧 Development Issues

| Issue | Solution |
|-------|----------|
| Virtual environment | `python -m venv venv` + `venv\Scripts\activate` |
| Dependencies | Merged requirements from both services |
| Database | Created `spotify_db` in PostgreSQL |
| Testing | SQLite in-memory database with fixtures |

---

## 🎓 Key Lessons

1. **Type Hints:** Use `Generator[T, None, None]` for functions with `yield`
2. **Pydantic:** Validators run after type validation, use `mode="before"` for transformations
3. **API Design:** Return only necessary data, keep responses minimal
4. **Architecture:** Modular > Layered for maintainability
5. **Testing:** In-memory DB + fixtures = fast, isolated tests

---

## 📊 Metrics

| Metric | Before (MVC) | After (Modular) |
|--------|--------------|------------------|
| Services | 2 | 1 |
| Files | ~40 | 50+ (organized) |
| Use Cases | 0 | 18 |
| Files Changed per Feature | 3-4 | 1 module |
| Communication | HTTP | Direct calls |

---

**Total Bugs Fixed:** 3  
**Architecture Improvements:** 3  
**Test Files Created:** 15
