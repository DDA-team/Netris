import json
import os
from pathlib import Path
from typing_extensions import Annotated
import uuid
import aiofiles
from fastapi import APIRouter, HTTPException, UploadFile, Form, Request, Response
from fastapi.responses import FileResponse, StreamingResponse
from fastapi import Header
from models import Item
from prestarted import Session
import aiofiles
from schemas.ItemScheme import ItemScheme

from utils import get_duration, get_first_frame
from video_streaming import generate_hls_streaming_response

items_router = APIRouter(prefix="/items", tags=["items"])
CHUNK_SIZE = 1024 * 1024


@items_router.get("/")
async def get_items():
    session = Session()
    items = []
    for item in session.query(Item).all():
        if item.events != "{}":
            with open(item.events, "r") as f:
                js_temp = json.loads(f.read())
        else:
            js_temp = None
        items.append(
            ItemScheme(
                id=item.id,
                title=item.title,
                input_video=item.input_video,
                output_video=item.output_video,
                data=js_temp,
                created_at=item.created_at,
                preview_img=item.preview_img,
                duration=item.duration,
                is_complete=item.is_complete,
            )
        )
    session.close()
    return items


@items_router.get("/status")
async def get_items():
    session = Session()
    items = []
    for item in session.query(Item).all():
        items.append((item.id, item.is_complete))
    session.close()
    return items


@items_router.get("/status/{id:str}")
async def get_items(id):
    session = Session()
    item = session.query(Item).filter_by(id=id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        item_scheme = item.is_complete
    session.close()
    return item_scheme


@items_router.get("/{id:str}")
async def get_item_by_id(id: str):
    session = Session()
    item = session.query(Item).filter_by(id=id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        if item.events != "{}":
            with open(item.events, "r") as f:
                js_temp = json.loads(f.read())
        else:
            js_temp = None
        item_scheme = ItemScheme(
            id=item.id,
            title=item.title,
            input_video=item.input_video,
            output_video=item.output_video,
            data=js_temp,
            created_at=item.created_at,
            preview_img=item.preview_img,
            duration=item.duration,
            is_complete=item.is_complete,
        )
    session.close()
    return item_scheme


@items_router.post("/remove/{id:str}")
async def remove_item_by_id(id: str):
    session = Session()
    item = session.query(Item).filter_by(id=id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        session.query(Item).filter_by(id=id).delete()
        session.commit()
    session.close()
    return True


# @items_router.get("/inputvideo/{id:str}")
# async def get_item_by_id(id: str, range: str = Header(None)):
#     session = Session()
#     item = session.query(Item).filter_by(id=id).first()
#     if item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     session.close()
#     path = Path(item.input_video)
#     print(range)
#     start, end = range.replace("bytes=", "").split("-")
#     print(start, end)
#     start = int(start)
#     end = int(end) if end else start + CHUNK_SIZE
#     with open(path, "rb") as video:
#         video.seek(start)
#         data = video.read(end - start)
#         filesize = str(path.stat().st_size)
#         # print(data)
#         headers = {
#             "Content-Range": f"bytes {str(start)}-{str(end)}/{filesize}",
#             "Accept-Ranges": "bytes",
#         }
#         print(Response(data, status_code=206, headers=headers, media_type="video/mp4"))
#         return Response(data, status_code=206, headers=headers, media_type="video/mp4")


@items_router.get("/outputvideo/{id:str}")
async def video_endpoint(
    id: str,
):
    session = Session()
    item = session.query(Item).filter_by(id=id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    session.close()

    def iterfile(video_path):
        with open(video_path, mode="rb") as file_like:
            yield from file_like

    return StreamingResponse(iterfile(item.input_video))


@items_router.get("/preview/{id:str}")
async def get_item_by_id(id: str):
    session = Session()
    item = session.query(Item).filter_by(id=id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    session.close()

    return FileResponse(
        path=item.preview_img,
        media_type="multipart/form-data",
    )


@items_router.get("/preview/output/{id:str}")
async def get_item_by_id(id: str):
    session = Session()
    item = session.query(Item).filter_by(id=id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    session.close()
    for i in os.listdir(f"temp/{item.seed}/"):
        print(i)
        return FileResponse(
            path=f"temp/{item.seed}/{i}",
            media_type="multipart/form-data",
        )


@items_router.get("/download/output/{id:str}")
async def video_download_endpoint(
    id: str,
):
    session = Session()
    item = session.query(Item).filter_by(id=id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    session.close()
    return FileResponse(
        item.output_video, filename="output.mp4", media_type="multipart/form-data"
    )


@items_router.get("/download/events/{id:str}")
async def video_download_endpoint(
    id: str,
):
    session = Session()
    item = session.query(Item).filter_by(id=id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    session.close()
    return FileResponse(
        item.events, filename="events.json", media_type="multipart/form-data"
    )


@items_router.get("/download/downtime/{id:str}")
async def video_download_endpoint(
    id: str,
):
    session = Session()
    item = session.query(Item).filter_by(id=id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    session.close()
    return FileResponse(
        item.downtime_events,
        filename="downtime_events.json",
        media_type="multipart/form-data",
    )


# @items_router.get("/inputvideo/{id:str}")
# async def video_endpoint(
#     id: str,
# ):
#     session = Session()
#     item = session.query(Item).filter_by(id=id).first()
#     if item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     session.close()
#     return await generate_hls_streaming_response(item.input_video)


@items_router.get("/events/{id:str}")
async def video_endpoint(
    id: str,
):
    session = Session()
    item = session.query(Item).filter_by(id=id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    session.close()
    with open(item.events, "r") as f:
        resp = json.loads(f.read())
    return resp


@items_router.get("/downtime/{id:str}")
async def video_endpoint(
    id: str,
):
    session = Session()
    item = session.query(Item).filter_by(id=id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    session.close()
    with open(item.downtime_events, "r") as f:
        resp = json.loads(f.read())
    return resp


@items_router.post("/add")
async def add_item(title: Annotated[str, Form()], file: Annotated[UploadFile, Form()]):
    session = Session()
    uuid_id = uuid.uuid4()
    async with aiofiles.open(f"temp/{uuid_id}.mp4", "wb") as out_file:
        content = await file.read()  # async read
        await out_file.write(content)

    new_item = Item(
        id=str(uuid_id),
        title=title,
        input_video=f"temp/{uuid_id}.mp4",
        preview_img=get_first_frame(
            f"temp/{uuid_id}.mp4", f"temp/{uuid_id}_preview.jpg"
        ),
        duration=get_duration(f"temp/{uuid_id}.mp4"),
    )
    session.add(new_item)
    session.commit()
    session.close()
    return True
