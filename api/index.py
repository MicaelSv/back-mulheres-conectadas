from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/home")
def read_root():
    return JSONResponse(content={"message": "Hello from FastAPI on Vercel!"})
