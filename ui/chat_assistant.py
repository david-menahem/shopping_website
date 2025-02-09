import openai
import os
import streamlit as st

from config.config import Config

config = Config()


def tab_chat_assistant(message_buffer):
    openai.api_key = config.OPENAI_API_KEY

    try:

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message_buffer,
            temperature=0.5
        )
        return {"role": "assistant", "content": response.choices[0].message.content}

    except Exception as e:
        return f"Error: {e}"
