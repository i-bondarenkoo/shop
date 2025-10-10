from fastapi import Request, Response
from typing import Callable, Awaitable
import logging


log = logging.getLogger(__name__)


async def log_new_request(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    log.info("Запрос %s на %s", request.method, request.url)
    return await call_next(request)
