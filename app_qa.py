import streamlit as st
from services import RagService

st.title("买衣服智能体")
st.divider()

ragService = RagService()

model_chain = ragService.get_chain()

print(st.session_state)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "msg": "你好，有什么可以帮助你的？"}]

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["msg"])

prompt = st.chat_input()

config = {
    "configurable": {
        "session_id": "2"
    }
}

if prompt:
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "msg": prompt})
    with st.spinner("正在思考..."):
        response = model_chain.stream({"question": prompt}, config=config)
        response_msg = ""

        def save_and_res(stream):
            global response_msg
            for chunk in stream:
                response_msg += chunk
                yield chunk


        st.chat_message("assistant").write_stream(save_and_res(response))
        st.session_state.messages.append({"role": "assistant", "msg": response_msg})
