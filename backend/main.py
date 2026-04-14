"""
AgentDesk Backend – FastAPI Server
In-memory user storage with REST endpoints for the admin panel.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("agentdesk-backend")

app = FastAPI(title="AgentDesk Backend", version="1.0.0")

# CORS – allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# In-memory data store
# ---------------------------------------------------------------------------
users: list[dict] = [
    {"email": "john@company.com", "created_at": "2026-04-14T00:00:00", "password_reset": False},
    {"email": "jane@company.com", "created_at": "2026-04-14T00:00:00", "password_reset": False},
]


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------
class UserEmail(BaseModel):
    email: str


class UserResponse(BaseModel):
    email: str
    created_at: str
    password_reset: bool


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@app.get("/")
def root():
    return {"status": "ok", "service": "AgentDesk Backend"}


@app.get("/users", response_model=list[UserResponse])
def get_users():
    """Return all users."""
    logger.info("GET /users – returning %d users", len(users))
    return users


@app.post("/create-user")
def create_user(payload: UserEmail):
    """Create a new user by email."""
    email = payload.email.strip().lower()

    # Check for duplicates
    for u in users:
        if u["email"] == email:
            logger.warning("POST /create-user – duplicate email: %s", email)
            raise HTTPException(status_code=400, detail=f"User {email} already exists")

    new_user = {
        "email": email,
        "created_at": datetime.utcnow().isoformat(),
        "password_reset": False,
    }
    users.append(new_user)
    logger.info("POST /create-user – created user: %s", email)
    return {"message": f"User {email} created successfully", "user": new_user}


@app.post("/reset-password")
def reset_password(payload: UserEmail):
    """Simulate password reset for a user."""
    email = payload.email.strip().lower()

    for u in users:
        if u["email"] == email:
            u["password_reset"] = True
            logger.info("POST /reset-password – password reset for: %s", email)
            return {"message": f"Password reset successful for {email}"}

    logger.warning("POST /reset-password – user not found: %s", email)
    raise HTTPException(status_code=404, detail=f"User {email} not found")
