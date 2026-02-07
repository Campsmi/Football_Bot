from fastapi import FastAPI, UploadFile, File, HTTPException
from app.core.config import get_settings
from PIL import Image
import io

settings = get_settings()

app = FastAPI(title=settings.app_name)



@app.get("/")
def read_root():
    return {"message": "Hello! Football Bot is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "app": settings.app_name}


# Endpoint to upload image or video for analysis
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):  #async because the upload can take time and so it does not block (file operations -> async)
            
    content = await file.read()
    
    file_size = (len(content))
    
    
    try:
        # Convert bytes to image
        image = Image.open(io.BytesIO(content))
        
        # Get image information
        width, height = image.size
        image_format = image.format
        image_mode = image.mode
        
        return {
            "success": True,
            "filename": file.filename,
            "file_size_mb": round(file_size / (1024 * 1024), 2),
            "image_info": {
                "width": width,
                "height": height,
                "format": image_format,
                "mode": image_mode,
                "megapixels": round((width * height) / 1_000_000, 2)
            }
        }
        
    except Exception as e:
        return {
            "error": "Invalid image",
            "message": f"Could not open file as image: {str(e)}"
        }
