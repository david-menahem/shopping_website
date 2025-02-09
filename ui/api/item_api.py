from typing import List

import streamlit as st
import requests

from config.config import Config


config = Config()


@st.cache_data
def get_all_items():
    url = f"{config.BASE_URL}/item"
    response = requests.get(url)
    return response.json()


def get_items_by_names(names: List[str]):
    url = f"{config.BASE_URL}/item/names"
    response = requests.get(url, json=names)
    return response.json()


def get_items_by_stock(stock, operator):
    url = f"{config.BASE_URL}/item/stock"
    params = {"stock": stock, "operator": operator}
    response = requests.get(url, params=params)
    return response.json()


def get_items_by_price(price, operator):
    url = f"{config.BASE_URL}/item/price"
    params = {"price": price, "operator": operator}
    response = requests.get(url, params=params)
    return response.json()
