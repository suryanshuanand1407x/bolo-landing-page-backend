import os
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.environ.get("SUPABASE_URL", "")
supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
print(f"Supabase URL: {supabase_url}")
print(f"Supabase Key: {supabase_key[:10]}...")  # Just print first 10 chars for safety

if not supabase_url or not supabase_key:
    raise ValueError("Missing Supabase credentials. Please set NEXT_PUBLIC_SUPABASE_URL and NEXT_PUBLIC_SUPABASE_ANON_KEY environment variables.")

supabase: Client = create_client(supabase_url, supabase_key)

# Create FastAPI app
app = FastAPI(title="Bolo API", description="API for Bolo landing page")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define models
class WaitlistEntry(BaseModel):
    email: EmailStr

class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    message: str

class WaitlistResponse(BaseModel):
    id: int
    email: str
    created_at: str

class ContactResponse(BaseModel):
    id: int
    name: str
    email: str
    message: str
    created_at: str

# Routes
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Bolo API"}

@app.post("/api/waitlist", response_model=dict)
async def add_to_waitlist(entry: WaitlistEntry):
    try:
        # Check if email already exists
        response = supabase.table("waitlist").select("*").eq("email", entry.email).execute()
        
        if response.data and len(response.data) > 0:
            return {"message": "This email is already on our waitlist"}
        
        # Add to waitlist
        now = datetime.now().isoformat()
        response = supabase.table("waitlist").insert({
            "email": entry.email,
            "created_at": now
        }).execute()
        
        return {"message": "Successfully added to waitlist", "id": response.data[0]["id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/contact", response_model=dict)
async def create_contact(contact: ContactMessage):
    try:
        now = datetime.now().isoformat()
        response = supabase.table("contacts").insert({
            "name": contact.name,
            "email": contact.email,
            "message": contact.message,
            "created_at": now
        }).execute()
        
        return {"message": "Message sent successfully", "id": response.data[0]["id"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/waitlist", response_model=List[WaitlistResponse])
async def get_all_waitlist():
    try:
        response = supabase.table("waitlist").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/contact", response_model=List[ContactResponse])
async def get_all_contacts():
    try:
        response = supabase.table("contacts").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the application with uvicorn if this file is run directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)