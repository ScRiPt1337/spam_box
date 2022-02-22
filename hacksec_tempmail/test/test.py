from fastapi import Depends, FastAPI
from fastapi.security import HTTPBearer

app = FastAPI()

oauth2_scheme = HTTPBearer(auto_error=False)


@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": "gfdsgdfsgf"}