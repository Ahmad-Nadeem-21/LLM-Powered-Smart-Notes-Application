import uvicorn

# Run the FastAPI app defined in app/app.py
if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000)