from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import asyncio
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
import uuid
from datetime import datetime, timezone
import resend

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Resend config
resend.api_key = os.environ.get('RESEND_API_KEY', '')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'onboarding@resend.dev')

# Create the main app
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Models
class ContactForm(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    service_type: Optional[str] = None
    message: str


class ContactResponse(BaseModel):
    id: str
    status: str
    message: str


@api_router.get("/")
async def root():
    return {"message": "ABSCO API Running"}


@api_router.post("/contact", response_model=ContactResponse)
async def submit_contact(form: ContactForm):
    contact_id = str(uuid.uuid4())

    # Store in MongoDB
    doc = {
        "id": contact_id,
        "name": form.name,
        "email": form.email,
        "phone": form.phone or "",
        "service_type": form.service_type or "General",
        "message": form.message,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.contacts.insert_one(doc)

    # Send email via Resend
    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2 style="color: #7c3aed;">New Contact from ABSCO Website</h2>
        <table style="width: 100%; border-collapse: collapse;">
            <tr><td style="padding: 8px; font-weight: bold;">Name:</td><td style="padding: 8px;">{form.name}</td></tr>
            <tr><td style="padding: 8px; font-weight: bold;">Email:</td><td style="padding: 8px;">{form.email}</td></tr>
            <tr><td style="padding: 8px; font-weight: bold;">Phone:</td><td style="padding: 8px;">{form.phone or 'N/A'}</td></tr>
            <tr><td style="padding: 8px; font-weight: bold;">Service:</td><td style="padding: 8px;">{form.service_type or 'General'}</td></tr>
        </table>
        <div style="padding: 16px; background: #f3f4f6; border-radius: 8px; margin-top: 16px;">
            <p style="font-weight: bold; margin: 0 0 8px;">Message:</p>
            <p style="margin: 0;">{form.message}</p>
        </div>
    </div>
    """

    try:
        params = {
            "from": SENDER_EMAIL,
            "to": ["abscocleaning@yahoo.com"],
            "subject": f"ABSCO Website Contact - {form.name}",
            "html": html_content
        }
        email_result = await asyncio.to_thread(resend.Emails.send, params)
        logger.info(f"Email sent successfully: {email_result}")
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        # Still return success since we saved to DB

    return ContactResponse(
        id=contact_id,
        status="success",
        message="Thank you! We'll get back to you soon."
    )


# Include the router
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
