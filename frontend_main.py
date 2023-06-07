import streamlit as st
import json
import requests
import pandas as pd
from io import BytesIO
import zipfile
from modeltest import evaluate

# for service environment
# URL = "http://3.36.142.235:8000/visualize"
# for dev environment
URL = "http://localhost:8000/visualize"

st.sidebar.title("Input space")

st.title("Output space")

uploaded_file = st.sidebar.file_uploader("choose a excel file")
response = None
if uploaded_file is not None:
    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_excel(uploaded_file)
    st.sidebar.write(dataframe)

    response = requests.post(URL, headers={'Cache-Control': 'no-cache'}, json=json.loads(dataframe.to_json()))

if response is not None:
    zip_data = response.content
    zip_file = zipfile.ZipFile(BytesIO(zip_data), "r")
    png_file = zip_file.read("result.png")
    xlsx_file = zip_file.read("result.xlsx")

try:
    resultdf = pd.read_excel(xlsx_file)
    evaluation_result=evaluate(resultdf)
    st.text(evaluation_result[0])
    st.text(evaluation_result[1])
except:
    st.text("evaluate result will appear hear")

try:
    st.image(png_file, caption="This image is a visualization of input json")
    btn = st.download_button(
        label="Download visualization result",
        data=png_file,
        file_name="visualization_result.png",
        mime="image/png"
    )
except:
    st.text("image will appear hear")

try:
    result_df = pd.read_excel(xlsx_file)
    st.write(result_df)
    btn = st.download_button(
        label="Download result xlsx",
        data=xlsx_file,
        file_name="result_file.xlsx",
        mime="xlsx"
    )
except:
    st.text("result xlsx will appear hear")
