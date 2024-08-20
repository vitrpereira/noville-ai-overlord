import streamlit as st
from context_retrieval.pinecone_search import PineconeSearch
import os

pinecone_search = PineconeSearch()


@st.cache_resource(show_spinner=False)
def setup_index():
    return pinecone_search.get_index()


def streamlit():
    index = setup_index()

    if "chat_engine" not in st.session_state.keys():
        st.session_state.chat_engine = index.as_chat_engine(
            chat_mode="context", verbose=True
        )

    st.set_page_config(
        page_title="Investment profiler",
        page_icon="$",
        layout="centered",
        initial_sidebar_state="auto",
        menu_items=None,
    )
    st.title("Testing chat")

    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Let's analyse your investment profile! Please answer the following questions",
            }
        ]

    if prompt := st.chat_input("Answer:"):
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("thinking..."):
                response = st.session_state.chat_engine.chat(message=prompt)
                st.write(response.response)
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message)


if __name__ == "__main__":
    streamlit()