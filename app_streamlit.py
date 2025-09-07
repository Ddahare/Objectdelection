import streamlit as st
import os
from aws_utils import upload_file, download_file
from detect_image import detect_image
from detect_video import detect_video

st.set_page_config(page_title='YOLO S3 Demo', layout='wide')
st.title('YOLOv8 + S3 Demo')

st.sidebar.header('Upload media (images and videos)')
uploaded = st.sidebar.file_uploader('Choose an image or video', type=['jpg','jpeg','png','mp4','mov'])

S3_PREFIX_UPLOAD = 'uploads/'

if uploaded is not None:
    st.sidebar.write('Filename:', uploaded.name)
    local_path = os.path.join('tmp', uploaded.name)
    os.makedirs('tmp', exist_ok=True)
    with open(local_path, 'wb') as f:
        f.write(uploaded.getbuffer())

    s3_key = S3_PREFIX_UPLOAD + uploaded.name
    if upload_file(local_path, s3_key):
        st.sidebar.success(f'Uploaded to S3: {s3_key}')

    if uploaded.type.startswith('image'):
        out = detect_image(local_path, out_path='tmp/out_' + uploaded.name)
        st.image(out, caption='Detection result', use_column_width=True)
        upload_file(out, 'processed/' + os.path.basename(out))

    elif uploaded.type.startswith('video'):
        out_vid = detect_video(local_path, out_path='tmp/out_' + uploaded.name)
        st.video(out_vid)
        upload_file(out_vid, 'processed/' + os.path.basename(out_vid))
