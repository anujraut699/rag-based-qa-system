import time
from fastapi import HTTPException, Request

# Store request timestamps per IP
request_log = {}

REQUEST_LIMIT = 5        # max requests
TIME_WINDOW = 60         # seconds


def rate_limit(request: Request):
    client_ip = request.client.host
    current_time = time.time()

    if client_ip not in request_log:
        request_log[client_ip] = []

    # Remove old requests
    request_log[client_ip] = [
        t for t in request_log[client_ip]
        if current_time - t < TIME_WINDOW
    ]

    if len(request_log[client_ip]) >= REQUEST_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again later."
        )

    request_log[client_ip].append(current_time)
