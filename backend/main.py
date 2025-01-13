from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import os

app = FastAPI()

# 1) Serve example .nii.gz data
@app.get("/api/data")
def get_nii():
    file_path = "data/mpld_asl.nii.gz"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type='application/gzip')

# 2) Optional: upload .nii.gz
@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    if not (file.filename.endswith('.nii.gz') or file.filename.endswith('.nii')):
        raise HTTPException(status_code=400, detail="Unsupported file format")

    out_file_path = os.path.join("uploads", file.filename)
    with open(out_file_path, 'wb') as out_file:
        content = await file.read()
        out_file.write(content)

    return {"detail": "File uploaded successfully", "filename": file.filename}
