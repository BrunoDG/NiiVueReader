from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

origins = [
    'http://localhost',
    'http://localhost:5173',
    'http://localhost:8000',
    'https://localhost',
    'https://localhost:5173',
    'https://localhost:8000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directories
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Endpoints
@app.get("/api/volume")
def get_volume(filename: str | None = None):
    """Returns default NIfTI file URL

    Returns:
        url: File URL requested by frontend 
    """
    if filename == None:
        filename = "mpld_asl.nii.gz"
    
    print(f"name: {filename}")
    
    file_path = os.path.join(DATA_DIR, filename)
    print(f"Volume: {file_path}")
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found in data directory")
    
    file_url = f"http://localhost:8000/api/data/{filename}"
    return {"url": file_url}


@app.get("/api/files")
def list_files():
    """List all files in the uploads directory

    Raises:
        HTTPException: No Files found

    Returns:
        files: all files available at the directory
    """
    try:
        files = [
            file for file in os.listdir(DATA_DIR)
            if os.path.isfile(os.path.join(DATA_DIR, file)) and
            (file.endswith('.nii') or file.endswith('.nii.gz'))
        ]
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/data/{filename}")
def get_file(filename: str):
    """Returns requested file

    Args:
        filename (str): file requested from frontend

    Raises:
        HTTPException: Error informing that file does not existe

    Returns:
        FileResponse: File attachment with current file
    """
    file_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        file_path, 
        media_type='application/gzip',
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Uploads a .nii or .nii.gz file

    Args:
        file (UploadFile, optional): Requested upload file. Defaults to File(...).

    Raises:
        HTTPException: Error on uploaded file.

    Returns:
        _type_: _description_
    """
    if not (file.filename.endswith('.nii.gz') or file.filename.endswith('.nii')):
        raise HTTPException(status_code=400, detail="Unsupported file format")

    out_file_path = os.path.join(DATA_DIR, file.filename)
    with open(out_file_path, 'wb') as out_file:
        content = await file.read()
        out_file.write(content)

    return {
        "detail": "File uploaded successfully", 
        "filename": file.filename, 
        "path": f"http://localhost:8000/api/data/{file.filename}",
    }
