from wsgicors import CORS
from molten import App, Include, Route
from molten.openapi import Metadata, OpenAPIHandler, OpenAPIUIHandler
from molten.contrib.prometheus import expose_metrics, prometheus_middleware

from settings import logging

from api.v1 import room, meeting


log = logging.getLogger(__name__)

"""
Open API
"""

get_schema = OpenAPIHandler(
    metadata=Metadata(
        title="Emeeting API",
        description="An API for managing your room meetings.",
        version="0.0.1",
    )
)

get_docs = OpenAPIUIHandler()


"""
Add middlewares
"""

middlewares = [prometheus_middleware]


"""
Include or add routes
"""

routes = [
    Route("/", get_docs),
    Route("/schema", get_schema),
    Route("/metrics", expose_metrics),
    Include("/v1/rooms", routes=room.routes),
    Include("/v1/meetings", routes=meeting.routes),
]

"""
Start application
"""

app = App(routes=routes, middleware=middlewares)
app = CORS(app, headers="*", methods="*", origin="*", maxage="86400")

log.info("Start application successfully.")
