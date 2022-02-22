from unicodedata import name
from fastapi import FastAPI, WebSocket, Depends, Request, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.websockets import WebSocketDisconnect
from fastapi.security import HTTPBearer, HTTPBasic, OAuth2PasswordBearer, OAuth2PasswordRequestForm
import database
from pydantic import BaseModel
from json import dumps
from ConnectionManager import ConnectionManager
from starlette.staticfiles import StaticFiles
from json import loads
import binascii
import os

app = FastAPI(name="hacksec_tempmail", title="hacksec_tempmail", description="hacksec_tempmail", version="1.0")
auth_schema = HTTPBearer(auto_error=False)
app.mount("/home", StaticFiles(directory="hacksec-webmail",
          html=True), name="hacksec-webmail")
database = database.db()
manager = ConnectionManager()

config = {}
try:
    with open("/opt/hacksec_tempmail/hacksec_tempmail/config.json", "r") as config:
        config = loads(config.read())
except:
    print('No config file found. Please create a config.json file.')
    exit()

auth = config['auth']
origins = ["*"]
#app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class User(BaseModel):
    username: str
    password: str


class Settings(BaseModel):
    authjwt_secret_key: str = binascii.hexlify(os.urandom(32)).decode()


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@app.get("/")
def index():
    return RedirectResponse("/home")


@app.websocket('/mailbox')
async def websocket(websocket: WebSocket, token: str = Query(...), Authorize: AuthJWT = Depends()):
    await websocket.accept()
    try:
        Authorize.jwt_required("websocket", token=token)
        await websocket.send_text(dumps({"success": True, "email": database.view()}))
    except AuthJWTException as err:
        await websocket.send_text(err.message)
        await websocket.close()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get('/mailbox')
async def mailbox(Authorize: AuthJWT = Depends(auth_schema)):
    """Get all emails from the database"""
    Authorize.jwt_required()
    try:
        return JSONResponse(dumps({"success": True, "email": database.view()}))
    except Exception as err:
        return JSONResponse({"success": False, "error": str(err)})


@app.websocket('/mailbox/{id}')
async def websocket(websocket: WebSocket, id: int, token: str = Query(...), Authorize: AuthJWT = Depends()):
    await websocket.accept()
    try:
        Authorize.jwt_required("websocket", token=token)
        await websocket.send_text(dumps({"success": True, "email": database.view_single(id)}))
    except AuthJWTException as err:
        await websocket.send_text(err.message)
        await websocket.close()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get('/mailbox/{id}')
async def mailbox_id(id: int, Authorize: AuthJWT = Depends(auth_schema)):
    """Get a single email with given id"""
    Authorize.jwt_required()
    try:
        return JSONResponse(dumps({"success": True, "email": database.view_single(id)}))
    except Exception as err:
        return JSONResponse({"success": False, "error": str(err)})


@app.websocket('/mailbox/search/{search_term}')
async def websocket(websocket: WebSocket, search_term: str, token: str = Query(...), Authorize: AuthJWT = Depends()):
    await websocket.accept()
    try:
        Authorize.jwt_required("websocket", token=token)
        await websocket.send_text(dumps({"success": True, "email": database.search(search_term)}))
    except AuthJWTException as err:
        await websocket.send_text(err.message)
        await websocket.close()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get('/mailbox/search/{search_term}')
async def mailbox_search(search_term: str, Authorize: AuthJWT = Depends(auth_schema)):
    """Search email with a search term"""
    Authorize.jwt_required()
    try:
        return JSONResponse(dumps({"success": True, "email": database.search(search_term)}))
    except Exception as err:
        return JSONResponse({"success": False, "error": str(err)})


@app.websocket('/mailbox/delete/{id}')
async def websocket(websocket: WebSocket, id: int, token: str = Query(...), Authorize: AuthJWT = Depends()):
    await websocket.accept()
    try:
        Authorize.jwt_required("websocket", token=token)
        await websocket.send_text(dumps({"success": True, "email": database.delete(id)}))
    except AuthJWTException as err:
        await websocket.send_text(err.message)
        await websocket.close()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get('/mailbox/delete/{id}')
async def mailbox_del(id: int, Authorize: AuthJWT = Depends(auth_schema)):
    """Delete an email with the given id"""
    Authorize.jwt_required()
    try:
        return JSONResponse(dumps({"success": True, "email": database.delete(id)}))
    except Exception as err:
        return JSONResponse({"success": False, "error": str(err)})


@app.websocket('/mailbox/delete')
async def websocket(websocket: WebSocket, token: str = Query(...), Authorize: AuthJWT = Depends()):
    await websocket.accept()
    try:
        Authorize.jwt_required("websocket", token=token)
        await websocket.send_text(dumps({"success": True, "email": database.delete_all()}))
    except AuthJWTException as err:
        await websocket.send_text(err.message)
        await websocket.close()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get('/mailbox/delete')
async def mailbox_delete_all(Authorize: AuthJWT = Depends(auth_schema)):
    """Delete all emails"""
    Authorize.jwt_required()
    try:
        return JSONResponse(dumps({"success": True, "email": database.delete_all()}))
    except Exception as err:
        return JSONResponse({"success": False, "error": str(err)})


@app.post('/login')
def login(user: User, Authorize: AuthJWT = Depends()):
    if user.username != auth["username"] or user.password != auth["password"]:
        raise HTTPException(status_code=401, detail="Bad username or password")

    access_token = Authorize.create_access_token(
        subject=user.username, expires_time=False)
    refresh_token = Authorize.create_refresh_token(subject=user.username)
    return {"access_token": access_token, "refresh_token": refresh_token}
