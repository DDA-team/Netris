from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import prestarted
from routers.items_router import items_router
import asyncio

from worker import Worker


app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"])

app.include_router(items_router)


# @app.on_event("startup")
# async def startup_event():
#     worker_instanse = Worker("netris_8s(1280).pt", 0.25)
#     asyncio.create_task(worker_instanse.run_process())
