import pandas as pd
import streamlit as st

from ui.api.item_api import get_all_items
from ui.chat_assistant import tab_chat_assistant
from ui.favorite_items import tab_favorite_items
from ui.login_sidebar import login_sidebar
from ui.items import tab_items
from ui.order import tab_orders

if "jwt_token" not in st.session_state:
    st.session_state.jwt_token = None


st.title("Amazing shopping experience")

login_sidebar()

main_tab, order_tab, favorite_items_tab, chat_assistant_tab = st.tabs(['Main', 'Order',
                                                                       'Favorite Items', 'Chat Assistant'])
with main_tab:
    items = tab_items()
    st.write("Items")

    if items:
        items_df = pd.DataFrame(items)
        items_df = items_df.drop(["id"], axis=1)
        st.dataframe(items_df, use_container_width=True, hide_index=True)

with order_tab:
    st.header("Orders List")
    if st.session_state.jwt_token:
        tab_orders()
    else:
        st.write("Please login to view this content")

with favorite_items_tab:
    st.header("Favorite Items List")
    if st.session_state.jwt_token:
        tab_favorite_items()
    else:
        st.write("Please login to view this content")

with chat_assistant_tab:
    if st.session_state.jwt_token:
        if "queries" not in st.session_state:
            st.session_state.queries = 0
        available_items = get_all_items()
        message_buffer = []
        system_prompt = f"""
        You are a helpful assistant for a shopping website.
        The available items on the website are: {available_items}
        """
        message_buffer.append({"role": "system", "content": system_prompt})

        st.header("Welcome to the chat assistant")

        question_entered = True
        while question_entered and st.session_state.queries < 5:
            question_entered = False
            user_input = st.text_input("What do you want to know?: ", key=f"input: {st.session_state.queries}")
            if st.button("Send question", key=f"btn: {st.session_state.queries}"):
                message_buffer.append({"role": "user", "content": user_input})
                response = tab_chat_assistant(message_buffer)
                message_buffer.append(response)
                question_entered = True
                i = len(message_buffer) - 1
                while i > 0:
                    st.write(f'Question: {message_buffer[i - 1]["content"]}')
                    st.divider()
                    st.write(f'Answer: {message_buffer[i]["content"]}')
                    st.divider()
                    i = i - 2
                if st.session_state.queries == 5:
                    st.write("Query limit of 5 has been reached, you may reset the chat")
                    if st.button("Reset chat"):
                        st.session_state.queries = 0
                        message_buffer = [{"role": "system", "content": system_prompt}]
                        st.rerun()

    else:
        st.write("Please login to view this content")
