from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import os

app = FastAPI()

@app.get("/api/volume")
def get_volume():
    filename = "mpld_asl.nii.gz"
    file_url = f"http://localhost:8000/api/data/{filename}"
    
    return {"url": file_url}

@app.get("/api/data/{filename}")
def get_file(filename: str):
    file_path = os.path.join("data", filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        file_path, 
        media_type='application/gzip',
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    if not (file.filename.endswith('.nii.gz') or file.filename.endswith('.nii')):
        raise HTTPException(status_code=400, detail="Unsupported file format")

    out_file_path = os.path.join("uploads", file.filename)
    with open(out_file_path, 'wb') as out_file:
        content = await file.read()
        out_file.write(content)

    return {"detail": "File uploaded successfully", "filename": file.filename}
