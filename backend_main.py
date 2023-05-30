import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from visualize import object_visualize
from starlette.background import BackgroundTask
import os


class ModelResult(BaseModel):
    series_name: str
    episode_num: int
    current_classify: str
    evaluation: dict


app = FastAPI()


@app.post("/visualize/")
async def create_image(result: ModelResult):
    result_dict = result.dict()
    file_path = str(result_dict['series_name']) + '_' + str(result_dict['episode_num']) + '.png'
    object_visualize(result_dict, file_path)

    def cleanup():
        os.remove(file_path)

    return FileResponse(file_path, background=BackgroundTask(cleanup))

@app.get("/test/")
async def test_func():
    return {"test": 765}
