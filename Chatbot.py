import openai
import streamlit as st

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")
    st.stop()
openai.api_key = openai_api_key

st.title("💬 Tireless German tutor")
st.text("I am a chatbot and will help you with your German language practice.")
st.text("I will ask you questions and will correct your answers. Lets start!")
if "messages" not in st.session_state:
 #   initial_prompt = "Please act as my German teacher. You ask me questions in German at level B2. You then wait for my response. Do not answer your own question. You then correct my answer, including providing a grammatical explanation of the correction. After correcting, you ask me a new question in German and await my answer."
    st.session_state["messages"] = [{"role": "system", "content":"Please act as my German teacher. You ask me questions in German. You then wait for my response. You do not answer your own questions. When I have answered your question, you correct it and provide a grammatical explanation of the correction. After correcting, you ask me a new question in German and again await my answer."}]
 #   st.session_state.messages.append({"role": "system", "content": initial_prompt})
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)

for msg in st.session_state.messages:
    if msg["role"] != "system":
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message
    st.session_state.messages.append(msg)
    st.chat_message("assistant").write(msg.content)
