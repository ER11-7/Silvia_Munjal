from fastapi import FastAPI, Depends, HTTPException, status, APIRouter, Body, UploadFile, File
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from pwdlib import PasswordHash
import uvicorn
import os
import uuid
import time # For simulation delay

# --- CONFIGURATION & SECRETS ---

# CRITICAL: Reads SECRET_KEY from Render environment variable, falls back to a default locally
SECRET_KEY = os.environ.get("SECRET_KEY", "YOUR_SUPER_SECURE_DEFAULT_KEY_CHANGE_ME_NOW")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 24 hours

# CORS Settings (Crucial for Decoupled Frontend)
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "https://your-frontend-domain.com", # Replace this with the live domain
    "https://*.app.github.dev", # For Codespaces testing
    "https://your-live-api-name.onrender.com" # Allow self-access if needed
]

# --- DUMMY DATABASE/USER MOCK ---
class ClientUserDB(BaseModel):
    email: EmailStr
    hashed_password: str
    is_active: bool = True

password_hash = PasswordHash.recommended()
DUMMY_USER_DB = {
    "client@test.com": ClientUserDB(
        email="client@test.com",
        hashed_password=password_hash.hash("password")
    )
}

async def db_get_user(email: str) -> Optional[ClientUserDB]:
    """Simulates looking up user in PostgreSQL."""
    return DUMMY_USER_DB.get(email)

# --- SECURITY UTILITIES (Defined first to avoid NameError) ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against the stored hash."""
    return password_hash.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Creates a signed JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "sub": data.get("sub")})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> Dict[str, Any]:
    """Decodes and validates a JWT token and returns payload."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return payload

# --- DEPENDENCY INJECTION (Authentication Logic) ---

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependency that extracts and validates the user from the JWT token."""
    payload = decode_token(token)
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    user = await db_get_user(email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# --- INITIALIZE APP & MIDDLEWARE ---

app = FastAPI(
    title="Advocate Portfolio API Gateway",
    description="Backend for Secure Portal and AI/RAG Services.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SCHEMAS ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenRequest(BaseModel):
    email: EmailStr
    password: str

class QueryRequest(BaseModel):
    query: str

class DocumentMetadata(BaseModel):
    id: str
    filename: str
    uploaded_by: EmailStr
    upload_date: datetime
    status: str
    llm_summary: Optional[str] = None
    cloud_path: str


# --- API ENDPOINTS (ROUTERS) ---

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/login", response_model=Token)
async def login_for_access_token(form_data: TokenRequest = Body(...)):
    """
    Endpoint for Secure Client Login (FastAPI JWT Authentication).
    Demo User: client@test.com / password
    """
    user = await db_get_user(form_data.email)
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


public_router = APIRouter(tags=["Public & AI Services"])

@public_router.get("/")
async def root():
    return {"message": "Advocate Portfolio API Gateway is running."}

@public_router.post("/qa-chatbot")
async def ai_qa_chatbot(q: QueryRequest):
    """
    AI Q&A/Chatbot Endpoint (RAG Simulation).
    Simulates calling a LangChain/LlamaIndex pipeline to answer questions
    based ONLY on indexed internal documents (e.g., publications/FAQs).
    """
    # Simulation logic based on keywords
    llm_response_map = {
        "trade compliance": "The firm's expertise includes navigating post-Brexit trade compliance. A publication from Oct 2025 outlines the new documentation and tariff requirements for UK exports.",
        "dispute resolution": "Based on case studies, complex cross-border disputes are often resolved via mediation under SIAC rules, a method detailed in the firm's dispute resolution strategy.",
        "contract drafting": "Master Distributor Agreements require careful review of exclusive distribution clauses and automatic renewal terms, as highlighted in a recent document analysis on the EU market.",
    }

    query_lower = q.query.lower()
    
    if "trade" in query_lower or "export" in query_lower:
        answer = llm_response_map["trade compliance"]
    elif "dispute" in query_lower or "mediation" in query_lower:
        answer = llm_response_map["dispute resolution"]
    elif "contract" in query_lower or "renewal" in query_lower:
        answer = llm_response_map["contract drafting"]
    else:
        answer = "I apologize, but I cannot provide a definitive answer based on the indexed knowledge base. Please book a consultation for specific legal advice."

    return {"answer": answer}

# --- SECURE PORTAL ROUTER ---

portal_router = APIRouter(prefix="/portal", tags=["Secure Client Portal"])

@portal_router.post("/documents/upload", response_model=DocumentMetadata)
async def upload_document(
    file: UploadFile = File(...),
    current_user: ClientUserDB = Depends(get_current_user)
):
    """
    Uploads a document to secure storage and initiates LLM summary.
    (Requires JWT Auth)
    """
    # 1. Validation and File Storage (S3/GCS simulation)
    file_id = str(uuid.uuid4())
    time.sleep(1) # Simulate upload time

    # 2. LLM Summary Initiation (Asynchronous Simulation)
    llm_summary = f"LLM Summary: Preliminary analysis of {file.filename} suggests high complexity. Key terms: Jurisdiction, Arbitration, and non-compete. Review needed."
    time.sleep(3) # Simulate LLM processing delay

    # 3. Save metadata to PostgreSQL DB
    doc_metadata = DocumentMetadata(
        id=file_id,
        filename=file.filename,
        uploaded_by=current_user.email,
        upload_date=datetime.now(timezone.utc),
        status="New",
        llm_summary=llm_summary,
        cloud_path=f"s3://secure-bucket/{file_id}/{file.filename}"
    )

    return doc_metadata

@portal_router.get("/documents", response_model=List[DocumentMetadata])
async def list_documents(current_user: ClientUserDB = Depends(get_current_user)):
    """
    Lists documents relevant to the authenticated client.
    (Requires JWT Auth)
    """
    # Simulates fetching client-specific documents from DB
    return [
        DocumentMetadata(
            id="doc1", filename="Master Distributor Agreement (EU).pdf", uploaded_by=current_user.email,
            upload_date=datetime.now(timezone.utc) - timedelta(days=5), status="Reviewed",
            llm_summary="LLM Summary: The document outlines exclusive distribution clauses for the EU market. Key finding: No automatic renewal clause is present.",
            cloud_path="s3://path/doc1.pdf"
        ),
        DocumentMetadata(
            id="doc2", filename="Draft Arbitration Notice - Project Beta.docx", uploaded_by=current_user.email,
            upload_date=datetime.now(timezone.utc) - timedelta(days=2), status="New",
            llm_summary="LLM Summary: A preliminary review suggests that the case is best suited for mediation under SIAC rules. Further document gathering on correspondence history is needed.",
            cloud_path="s3://path/doc2.docx"
        )
    ]

# --- INCLUDE ROUTERS ---

app.include_router(public_router)
app.include_router(auth_router)
app.include_router(portal_router)

# --- ENTRY POINT (for local development via uvicorn main:app) ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
