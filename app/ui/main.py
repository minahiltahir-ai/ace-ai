import streamlit as st

from app.agents.chat import chat


st.set_page_config(
    page_title="ACE AI",
    page_icon="🤖",
    layout="wide",
)

st.title("ACE AI")
st.caption("Your intelligent local AI assistant")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask ACE anything..."):
    # Show and save user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate ACE AI response
    with st.chat_message("assistant"):
        with st.spinner("ACE is thinking..."):
            response = chat(prompt)

        st.markdown(response)

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )