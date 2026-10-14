import streamlit as st
import requests

st.set_page_config(page_title="RAG Demo")
st.title("RAG Knowledge Assistant")
st.caption("Cisco PDF | DeepSeek | pgvector | Redis")
if "messages" not in st.session_state:
    st.session_state.messages = []
if st.button("Clear chat"):
    st.session_state.messages = []
    st.rerun()
def show(m):
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m.get("citations"):
            with st.expander("Sources"):
                for c in m["citations"]:
                    st.write(c.get("document_title", "?"), "chunk", c.get("chunk_index", "?"))
                    st.caption(c.get("snippet", ""))
for m in st.session_state.messages:
    show(m)
question = st.chat_input("Ask about the Cisco PDF...")
if question:
    user = {"role": "user", "content": question}
    st.session_state.messages.append(user)
    show(user)
    try:
        with st.spinner("Searching..."):
            r = requests.post("http://127.0.0.1:8000/query", json={"question": question, "top_k": 3}, timeout=90)
            r.raise_for_status()
            data = r.json()
        bot = {"role": "assistant", "content": data.get("answer", "No answer."), "citations": data.get("citations", [])}
        st.session_state.messages.append(bot)
        show(bot)
    except (requests.RequestException, ValueError) as e:
        st.error(f"Request failed: {e}")
