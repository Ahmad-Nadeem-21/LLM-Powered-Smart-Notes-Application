import pydantic

class FileResponse(pydantic.BaseModel):
    file_id: str
    filename: str
    message: str