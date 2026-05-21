import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from todo_list_api.depends import get_config

from todo_list_api.routers.task import router as task_router
from todo_list_api.routers.user import router as user_router

app = FastAPI()

config = get_config()

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_cfg.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(task_router)


def main():
    uvicorn.run(app, host="0.0.0.0")


if __name__ == "__main__":
    main()
