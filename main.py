from urllib.request import Request

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse

from containers import Container
from user.interface.controllers.user_controller import router as user_routers

app = FastAPI()
app.include_router(user_routers)
app.container = Container()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
):
    return JSONResponse(
        status_code=400,
        content=exc.errors()
    )