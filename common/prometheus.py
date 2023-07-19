import socket

from prometheus_client import Counter, Histogram


PROJECT_NAME = 'fish'
HOST_NAME = socket.gethostname()


# PROJECT API
ApiReqCounter = Counter(
    "api_counter",
    "different url req counter",
    labelnames=["event", "hostname", "method", "endpoint"],
)
EventResponseTimeHis = Histogram(
    "http_response_seconds",
    "req response time",
    labelnames=["event", "hostname", "method", "endpoint"],
)
