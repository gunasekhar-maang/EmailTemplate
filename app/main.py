from pydantic import BaseModel, EmailStr
from app.email.email_sender import send_email
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Optional, List
import secrets
import os
import tempfile
from fastapi import APIRouter

app = FastAPI()
security = HTTPBasic()

# Authentication function
def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "gunasekhar123")
    correct_password = secrets.compare_digest(credentials.password, "gunasekhar123")
    
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Pydantic model for email request body (without files)
class EmailRequestBody(BaseModel):
    subject: str
    message: str
    to_mail: EmailStr

# Endpoint for sending email without attachments
@app.post("/send_email_without_attachments/")
async def send_email_without_attachments(
    to_mail:str,
    subject:str,
    message:str,
    username: str = Depends(authenticate)
):
    try:
        await send_email(subject=subject, to_email=to_mail, message_body=message, attachments=None)
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

# Endpoint for sending email with attachments
@app.post("/send_email_with_attachments/")
async def send_email_with_attachments(
    to_mail:str,
    subject:str,
    message:str,
    files: List[UploadFile] = File(None),
    username: str = Depends(authenticate)
):
    try:
        attachments = []
        with tempfile.TemporaryDirectory() as temp_dir:
            if files:
                for index, file in enumerate(files, start=1):
                    file_path = os.path.join(temp_dir, f"attachment-{index}{os.path.splitext(file.filename)[1]}")
                    with open(file_path, "wb") as buffer:
                        buffer.write(await file.read())
                    attachments.append(file_path)
            await send_email(subject=subject, to_email=to_mail, message_body=message, attachments=attachments if attachments else None)

        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
