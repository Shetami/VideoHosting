from pathlib import Path
from typing import IO, Generator

from django.shortcuts import get_object_or_404

from src.video_watcher.models import Video


def ranged(file: IO[bytes], start: int = 0, end: int = None, block_size: int = 8192) -> Generator[bytes, None, None]:
    consumed = 0

    file.seek(start)
    while True:
        data_length = min(block_size, end - start - consumed) if end else block_size
        if data_length <= 0:
            break
        data = file.read(data_length)
        if not data:
            break
        consumed += data_length
        yield data

    if hasattr(file, 'close'):
        file.close()


def open_file(request, pk: int) -> tuple:
    _video = get_object_or_404(Video, pk=pk)

    path = Path(_video.video.path)

    file = path.open('rb')
    file_size = path.stat().st_size

    content_length = file_size
    status = 200
    content_range = request.headers.get('range')

    if content_range is not None:
        ranges = content_range.strip().lower().split('=')[-1]
        start, end, *_ = map(str.strip, (ranges + '-').split('-'))
        start = max(0, int(start)) if start else 0
        end = min(file_size - 1, int(end)) if end else file_size - 1
        content_length = (end - start) + 1
        file = ranged(file, start=start, end=end + 1)
        status = 206
        content_range = f'bytes {start}-{end}/{file_size}'

    return file, status, content_length, content_range
