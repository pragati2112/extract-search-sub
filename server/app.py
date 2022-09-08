from pprint import pprint
from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from fastapi.responses import JSONResponse
from server.routes import router as media_router


async def catchall_exception_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        # you probably want some kind of logging here
        pprint(e)
        return JSONResponse({'detail': '"Internal server error"'}, status_code=500)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(media_router, prefix='/video', tags=["uploads and search operation"])


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome!"}
