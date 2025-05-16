import os
from datetime import datetime
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
from supabase import create_client, Client

# Load .env (for local development)
load_dotenv()

# Read Supabase credentials from env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    # Missing credentials: will crash here and print a traceback => "unsuccessful"
    raise RuntimeError(
        "Missing Supabase credentials. "
        "Please set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY environment variables."
    )

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(
    title="Bolo API",
    description="Backend for the Bolo landing page",
    version="1.0.0"
)

# CORS configuration
origins = [
    "http://localhost:5173",                                              # local dev
    "https://bolo-landing-page-frontend-tw2z.vercel.app",                # your Vercel frontend
    "*"                                                                   # allow all during initial rollout
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Models ---

class WaitlistEntry(BaseModel):
    email: EmailStr

class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    message: str

class WaitlistResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class ContactResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    message: str
    created_at: datetime

# --- Startup Event ---

@app.on_event("startup")
async def on_startup():
    # If we reach here, everything initialized OK
    print("start successful")

# --- Root Endpoint ---

@app.get("/")
async def read_root():
    return {
        "message": "Welcome to Bolo API!",
        "frontend_url": "https://bolo-landing-page-frontend-tw2z.vercel.app"
    }

# --- Health Check ---

@app.get("/health")
async def health():
    return {"status": "ok"}

# --- Waitlist Endpoints ---

@app.post("/api/waitlist", response_model=WaitlistResponse)
async def add_to_waitlist(entry: WaitlistEntry):
    try:
        # prevent duplicates
        existing = supabase.table("waitlist")\
            .select("id, email, created_at")\
            .eq("email", entry.email)\
            .execute()

        if existing.data:
            item = existing.data[0]
            return WaitlistResponse(
                id=item["id"],
                email=item["email"],
                created_at=datetime.fromisoformat(item["created_at"])
            )

        now = datetime.utcnow().isoformat()
        inserted = supabase.table("waitlist")\
            .insert({"email": entry.email, "created_at": now})\
            .select("id, email, created_at")\
            .execute()

        data = inserted.data[0]
        return WaitlistResponse(
            id=data["id"],
            email=data["email"],
            created_at=datetime.fromisoformat(data["created_at"])
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/waitlist", response_model=List[WaitlistResponse])
async def get_all_waitlist():
    try:
        res = supabase.table("waitlist")\
            .select("id, email, created_at")\
            .execute()

        return [
            WaitlistResponse(
                id=item["id"],
                email=item["email"],
                created_at=datetime.fromisoformat(item["created_at"])
            )
            for item in res.data
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Contact Endpoints ---

@app.post("/api/contact", response_model=ContactResponse)
async def create_contact(contact: ContactMessage):
    try:
        now = datetime.utcnow().isoformat()
        inserted = supabase.table("contacts")\
            .insert({
                "name": contact.name,
                "email": contact.email,
                "message": contact.message,
                "created_at": now
            })\
            .select("id, name, email, message, created_at")\
            .execute()

        data = inserted.data[0]
        return ContactResponse(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            message=data["message"],
            created_at=datetime.fromisoformat(data["created_at"])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/contact", response_model=List[ContactResponse])
async def get_all_contacts():
    try:
        res = supabase.table("contacts")\
            .select("id, name, email, message, created_at")\
            .execute()

        return [
            ContactResponse(
                id=item["id"],
                name=item["name"],
                email=item["email"],
                message=item["message"],
                created_at=datetime.fromisoformat(item["created_at"])
            )
            for item in res.data
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))