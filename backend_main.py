import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from visualize import object_visualize
from starlette.background import BackgroundTask
import os
from modeltest import test
import pandas as pd
import zipfile


app = FastAPI()


@app.post("/visualize/")
async def create_image(request: Request):
    json_val = await request.json()
    dataframe = pd.DataFrame(json_val)
    test_result = test(dataframe)
    test_result = test_result.drop(['Subtitle'], axis=1)
    object_visualize(test_result, "result.png")

    file_ls = ['result.png', 'result.xlsx']
    with zipfile.ZipFile("result_zip.zip", 'w') as result_zip:
        for entry in file_ls:
            result_zip.write(entry)
        result_zip.close()

    def cleanup():
        for entry in file_ls:
            os.remove(entry)
        os.remove("result_zip.zip")

    return FileResponse("result_zip.zip", background=BackgroundTask(cleanup))

@app.get("/test/")
async def test_func():
    return {"test": 765}
