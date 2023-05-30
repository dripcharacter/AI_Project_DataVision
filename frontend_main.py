import streamlit as st
import json
import requests

URL = "http://localhost:8000/visualize"
st.sidebar.title("Input space")

st.title("Output space")
input = st.sidebar.text_area("please input your json here")
try:
    st.sidebar.json(json.loads(input), expanded=False)
except:
    st.sidebar.text("json form will appear here")
try:
    response = requests.post(URL, headers={'Cache-Control': 'no-cache'}, json=json.loads(input))

    st.image(response.content, caption="This image is a visualization of input json")
    btn = st.download_button(
        label="Download visualization result",
        data=response.content,
        file_name="visualization_result.png",
        mime="image/png"
    )
except:
    st.text("image will appear hear")
