from pathlib import Path

import streamlit as st

from app.agents.chat import chat_stream
from app.memory.database import (
    add_message,
    create_conversation,
    delete_conversation,
    get_conversations,
    get_messages,
    initialize_database,
    update_conversation_title,
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ACE AI",
    page_icon="✦",
    layout="wide",
)


# =========================================================
# INITIALIZE DATABASE
# =========================================================

initialize_database()


# =========================================================
# LOAD CUSTOM CSS
# =========================================================

css_path = Path(__file__).parent / "style.css"

with open(css_path, "r", encoding="utf-8") as css_file:
    css = css_file.read()

st.markdown(
    f"<style>{css}</style>",
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def load_chat(conversation_id: int) -> None:
    """Load a saved conversation into the current session."""

    database_messages = get_messages(conversation_id)

    st.session_state.conversation_id = conversation_id

    st.session_state.messages = [
        {
            "role": message["role"],
            "content": message["content"],
        }
        for message in database_messages
    ]


def generate_chat_title(message: str) -> str:
    """Create a short title from the first user message."""

    cleaned = " ".join(message.strip().split())

    if not cleaned:
        return "New Chat"

    if len(cleaned) <= 32:
        return cleaned

    return cleaned[:32].rstrip() + "..."


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="ace-brand">
            <span class="ace-brand-symbol">✦</span>
            <span>ACE AI</span>
        </div>

        <div class="ace-brand-subtitle">
            Intelligent AI Assistant
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-divider"></div>',
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # NEW CHAT
    # -----------------------------------------------------

    if st.button(
        "＋  New Chat",
        use_container_width=True,
    ):
        # IMPORTANT:
        # Do NOT create a database conversation here.
        # A conversation will only be created when
        # the user sends the first message.

        st.session_state.conversation_id = None
        st.session_state.messages = []

        st.rerun()

    # -----------------------------------------------------
    # CHAT HISTORY TITLE
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="sidebar-section-title">
            CHAT HISTORY
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------------------------------
    # LOAD SAVED CHATS
    # -----------------------------------------------------

    conversations = get_conversations()

    if not conversations:

        st.markdown(
            """
            <div class="recent-chat">
                No conversations yet.
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        for conversation in conversations:

            conversation_id = conversation["id"]

            title = conversation["title"]

            is_active = (
                conversation_id
                == st.session_state.conversation_id
            )

            # ---------------------------------------------
            # OPEN CHAT
            # ---------------------------------------------

            button_label = (
                f"●  {title}"
                if is_active
                else f"○  {title}"
            )

            if st.button(
                button_label,
                key=f"open_chat_{conversation_id}",
                use_container_width=True,
            ):
                load_chat(conversation_id)
                st.rerun()

            # ---------------------------------------------
            # DELETE CHAT
            # ---------------------------------------------

            if st.button(
                "🗑️ Delete",
                key=f"delete_chat_{conversation_id}",
                use_container_width=True,
            ):
                delete_conversation(conversation_id)

                if (
                    st.session_state.conversation_id
                    == conversation_id
                ):
                    st.session_state.conversation_id = None
                    st.session_state.messages = []

                st.rerun()


# =========================================================
# MAIN HEADER
# =========================================================

# IMPORTANT:
# This header remains visible during the active chat.
# The large welcome screen is shown only when there
# are no messages.

if st.session_state.messages:

    st.html(
        """
        <div class="ace-chat-header">

            <div class="chat-header-title">
                <span>✦</span> ACE AI
            </div>

            <div class="chat-header-status">
                ● READY
            </div>

        </div>
        """
    )


# =========================================================
# EMPTY / WELCOME STATE
# =========================================================

if not st.session_state.messages:

    st.html(
        """
        <div class="ace-empty-state">

            <div class="ace-main-title">
                <span>✦</span> ACE AI
            </div>

            <div class="ace-main-subtitle">
                Your intelligent AI assistant
            </div>

            <div class="ace-orb-wrapper">
                <div class="ace-orb ace-orb-idle"></div>
            </div>

            <div class="ace-ready">
                <span class="ready-dot"></span>
                READY
            </div>

            <div class="ace-welcome-title">
                How can I help you today?
            </div>

            <div class="ace-welcome-subtitle">
                Ask anything. ACE is ready to assist.
            </div>

        </div>
        """
    )


# =========================================================
# ACTIVE CONVERSATION
# =========================================================

if st.session_state.messages:

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            # ---------------------------------------------
            # DISPLAY SAVED SOURCES
            # ---------------------------------------------

            sources = message.get("sources", [])

            if sources:

                st.markdown(
                    "### 📚 Sources"
                )

                for source in sources:

                    source_name = Path(
                        source["source"]
                    ).name

                    page = source.get("page")

                    if page:
                        st.markdown(
                            f"📄 **{source_name}** — Page {page}"
                        )
                    else:
                        st.markdown(
                            f"📄 **{source_name}**"
                        )


# =========================================================
# CHAT INPUT
# =========================================================

if prompt := st.chat_input("Ask ACE anything..."):

    cleaned_prompt = prompt.strip()

    if not cleaned_prompt:
        st.stop()

    # -----------------------------------------------------
    # CREATE DATABASE CONVERSATION ONLY NOW
    # -----------------------------------------------------

    if st.session_state.conversation_id is None:

        conversation_title = generate_chat_title(
            cleaned_prompt
        )

        conversation_id = create_conversation(
            conversation_title
        )

        st.session_state.conversation_id = (
            conversation_id
        )

    else:

        conversation_id = (
            st.session_state.conversation_id
        )

    # -----------------------------------------------------
    # BUILD HISTORY
    # -----------------------------------------------------

    conversation_history = []

    for message in st.session_state.messages:

        role = (
            "human"
            if message["role"] == "user"
            else "assistant"
        )

        conversation_history.append(
            (
                role,
                message["content"],
            )
        )

    # -----------------------------------------------------
    # SAVE USER MESSAGE
    # -----------------------------------------------------

    user_message = {
        "role": "user",
        "content": cleaned_prompt,
    }

    st.session_state.messages.append(
        user_message
    )

    add_message(
        conversation_id=conversation_id,
        role="user",
        content=cleaned_prompt,
    )

    # -----------------------------------------------------
    # DISPLAY USER MESSAGE
    # -----------------------------------------------------

    with st.chat_message("user"):

        st.markdown(cleaned_prompt)

        # -----------------------------------------------------
    # GENERATE ACE RESPONSE
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        response_stream, sources = chat_stream(
            message=cleaned_prompt,
            history=conversation_history,
        )

        response_placeholder = st.empty()

        response_parts = []

        for chunk in response_stream:

            response_parts.append(chunk)

            response_placeholder.markdown(
                "".join(response_parts)
            )

        response = "".join(response_parts).strip()

        # -------------------------------------------------
        # DISPLAY SOURCES
        # -------------------------------------------------

        if sources:

            st.markdown(
                "### 📚 Sources"
            )

            for source in sources:

                source_name = Path(
                    source["source"]
                ).name

                page = source.get("page")

                if page:
                    st.markdown(
                        f"📄 **{source_name}** — Page {page}"
                    )
                else:
                    st.markdown(
                        f"📄 **{source_name}**"
                    )


    # -----------------------------------------------------
    # SAVE ASSISTANT MESSAGE
    # -----------------------------------------------------

    assistant_message = {
        "role": "assistant",
        "content": response,
        "sources": sources,
    }

    st.session_state.messages.append(
        assistant_message
    )

    add_message(
        conversation_id=conversation_id,
        role="assistant",
        content=response,
    )

    # -----------------------------------------------------
    # UPDATE CHAT TITLE
    # -----------------------------------------------------

    if len(st.session_state.messages) == 2:

        update_conversation_title(
            conversation_id=conversation_id,
            title=generate_chat_title(
                cleaned_prompt
            ),
        )

    # -----------------------------------------------------
    # REFRESH SIDEBAR
    # -----------------------------------------------------

    st.rerun()