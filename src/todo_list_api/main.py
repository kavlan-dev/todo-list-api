import uvicorn
from fastapi import FastAPI

from todo_list_api.routers.task import router

app = FastAPI()


app.include_router(router)


def main():
    uvicorn.run(app)


if __name__ == "__main__":
    main()
