import streamlit as st
from ui.api.item_api import get_items_by_names, get_items_by_stock, get_items_by_price, get_all_items


def tab_items():
    items = get_all_items()
    st.header("Search by criteria")
    operators = {"select": "select",
                 "Greater Than": ">",
                 "Lower Than": "<",
                 "Equals to": "="}
    with st.form(key="search_by_names"):
        st.subheader("Search items by names")
        names = st.text_input("Item names: (if more than one, separate by space)",
                              key="names_input")
        search_names_btn = st.form_submit_button("Submit")

    if search_names_btn:
        if names:
            names = names.split(" ")
            names_list = []
            for name in names:
                names_list.append(name)

            items = get_items_by_names(names_list)
        else:
            st.error("Please provide an item name")

    st.divider()

    with st.form(key="search_by_stock"):
        st.subheader("Search items by stock")
        stock = st.text_input("Stock", key="stock_input")
        selected_value = st.selectbox("choose an operator", options=list(operators.keys()), key="stock_operator")
        stock_operator = operators[selected_value]
        search_stock_btn = st.form_submit_button("Submit")

    if search_stock_btn:
        if stock:
            try:
                stock = int(stock)
                items = get_items_by_stock(stock, stock_operator)
            except ValueError:
                st.error("Input must be a whole number")
        else:
            st.error("Please prove a stock quantity")

    st.divider()

    with st.form(key="search_by_price"):
        st.subheader("Search items by price")
        price = st.text_input("Price", key="price_input")
        selected_value = st.selectbox("choose an operator", options=list(operators.keys()), key="price_operator")
        price_operator = operators[selected_value]
        search_price = st.form_submit_button("Submit")

    if search_price:
        if price:
            try:
                price = float(price)
                items = get_items_by_price(price, price_operator)
            except ValueError:
                st.error("Input must be a number")
        else:
            st.error("Please provide an item price")

    if items:
        return items
    else:

        st.write("Items not found")
