import time

import streamlit as st
from knowledge_base import KnowledgeBaseService

st.title("知识库更新服务")

if "knowledgeService" not in st.session_state:
    st.session_state.knowledgeService = KnowledgeBaseService()

upload_file = st.file_uploader(
    "请上传txt文件",
    type=["txt"],
    accept_multiple_files=False,
    key="file_uploader"
)

if upload_file is not None:
    file_name = upload_file.name
    file_type = upload_file.type
    file_size = upload_file.size / 1024
    st.subheader(f"文件名:{file_name}")
    st.write(f"格式:{file_type} | 大小:{file_size:.2f}KB")
    file_str = upload_file.getvalue().decode("utf-8")
    with st.spinner("正在上传..."):
        time.sleep(1)
        status = st.session_state.knowledgeService.upload_by_str(file_str, file_name)
        st.write(status)
    st.write(file_str)