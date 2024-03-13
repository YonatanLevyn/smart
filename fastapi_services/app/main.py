from fastapi import FastAPI, BackgroundTasks, HTTPException, UploadFile, File
from .storage_service.s3_uploader import upload_file_to_s3
from .email_service.email_sender import send_mail_with_ses
from pydantic import BaseModel, EmailStr


app = FastAPI()


class EmailSchema(BaseModel):
    email: EmailStr
    username: str

async def background_task_wrapper(task_func, *args, **kwargs):
    try:
        await task_func(*args, **kwargs)
    except Exception as e:
        print(f"Background task error: {e}")


@app.post("/send-email/")
async def send_email(background_tasks: BackgroundTasks, email_data: EmailSchema):
    
    #The background task runs independently, and its completion does not affect the function that scheduled it.
    background_tasks.add_task(background_task_wrapper, send_mail_with_ses, email_data.email, email_data.username)
    return {"message": "Email is being sent in the background"}


"""
@app.post("/upload/")
async def upload_to_s3(file: UploadFile = File(...)):
    try:
        upload_file_to_s3(file, "coursesbucket")
        return {"message": "File uploaded successfully"}
    except S3UploadError as e:
        # Return a 500 internal server error response with the error message
        raise HTTPException(status_code=500, detail=e.message)
"""