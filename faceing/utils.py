
from fastapi import UploadFile
import aiofiles


async def write_content(content: UploadFile, content_path: str):
    async with aiofiles.open(content_path, 'wb') as uploaded_content:
        data = await content.read()
        await uploaded_content.write(data)

