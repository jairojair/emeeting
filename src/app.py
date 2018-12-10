from molten import App, Include, Route
from molten.openapi import Metadata, OpenAPIHandler, OpenAPIUIHandler
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
Include or add routes
"""

routes = [
    Route("/", get_docs),
    Route("/schema", get_schema),
    Include("/v1/rooms", routes=room.routes),
    Include("/v1/meetings", routes=meeting.routes),
]

"""
Start application
"""

app = App(routes=routes)

log.info("Start application successfully.")
