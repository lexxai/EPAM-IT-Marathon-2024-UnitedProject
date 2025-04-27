from functools import wraps
import time
import logging

from fastapi import Request, Response

logger = logging.getLogger("main")


def a_measure_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        """
        Async Wraps a function with a time measurement.

        It logs the request and response with corresponding time.
        Also sets a header 'X-Process-Time' with process time in seconds.

        :param func: function to be wrapped.
        :return: wrapped function.
        """
        request = args[0]
        if isinstance(request, Request):
            logger.info(f"Request: {request.method} {request.url}")
        start_time = time.perf_counter()
        response = await func(*args, **kwargs)
        process_time = round(time.perf_counter() - start_time, 4)
        if isinstance(response, Response):
            logger.info(f"Response: {process_time:2.4f}s | {response.status_code}")
            response.headers["X-Process-Time"] = str(process_time)
        else:
            logger.info(f"Response: {process_time:2.4f}s")
        return response

    return wrapper
