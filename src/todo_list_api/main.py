import uvicorn
from fastapi import FastAPI

from todo_list_api.routers.task import router as task_router
from todo_list_api.routers.user import router as user_router

app = FastAPI()


app.include_router(task_router)
app.include_router(user_router)


def main():
    uvicorn.run(app, host="0.0.0.0")


if __name__ == "__main__":
    main()
