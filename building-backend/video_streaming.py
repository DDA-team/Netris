import subprocess
from starlette.responses import StreamingResponse


async def generate_hls_streaming_response(video_path):
    hls_cmd = [
        "ffmpeg",
        "-i",
        video_path,
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-hls_time",
        "10",
        "-hls_list_size",
        "0",
        "-f",
        "hls",
        "pipe:1",
    ]

    p = subprocess.Popen(hls_cmd, stdout=subprocess.PIPE, bufsize=10**8)

    async def stream(response):
        while True:
            chunk = p.stdout.read(1024 * 1024)
            print(chunk)
            if not chunk:
                break
            await response.write(chunk)

    headers = {
        "Content-Type": "application/x-mpegURL",
        "Cache-Control": "no-cache",
        "Transfer-Encoding": "chunked",
    }

    return StreamingResponse(stream, headers=headers)
