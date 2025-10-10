import logging
from fastapi import Request, Response
import time

log = logging.getLogger(__name__)


async def time_to_request(
    request: Request,
    call_next,
):
    start_time = time.perf_counter()
    response: Response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-time-request-counter"] = f"{process_time:.3f}"
    return response
