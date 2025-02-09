import pandas as pd
import streamlit as st

from model.enums.order_status import OrderStatus
from model.order_item import OrderItem
from model.order_item_remove import OrderItemRemove
from model.order_request import OrderRequest
from model.order_response import OrderResponse
from ui.api.item_api import get_all_items
from ui.api.order_api import get_all_orders, add_item_to_order, create_pending_order, remove_item_from_order, \
    delete_pending_order, purchase_order


def tab_orders():
    orders = get_all_orders(st.session_state.jwt_token)

    items = get_all_items()
    items_df = pd.DataFrame(items)

    temp_order = None
    for order in orders:
        if order["status"] == OrderStatus.TEMP.name:
            temp_order = order
            break

    if not temp_order:
        st.subheader("New Order")
        with st.expander("New Order"):
            new_order_form(items_df)

    if temp_order:
        st.subheader("Pending order")
        with st.expander("Pending order"):
            show_order_details(temp_order)

            temp_order_form(items_df, temp_order)

    st.divider()

    count = 0
    st.subheader("Purchased Orders")
    for order in orders:
        count += 1
        if order["status"] != OrderStatus.TEMP.value:
            with st.expander(f"Order No' {count}"):
                show_order_details(order)


def temp_order_form(items_df, temp_order):
    with st.form(key="add_item"):
        add_item = st.selectbox("Add item to order", options=items_df["name"], index=0)
        quantity = st.number_input("How many do you want?", min_value=0, format="%d")

        add_btn = st.form_submit_button("Add Item to order")
        if add_btn:
            if add_item and quantity:
                item = items_df[items_df["name"] == add_item]
                item_id = item["id"]
                order_item = OrderItem(
                    order_id=temp_order["id"],
                    item_id=item_id,
                    quantity=quantity
                )
                response = add_item_to_order(order_item.dict(), st.session_state.jwt_token)
                if response:
                    st.error(response["detail"])
                else:
                    st.success("Item added to order")
                    st.rerun()
            else:
                st.error("Please select item and quantity")

    with st.form("remove_item"):
        order_item_df = pd.DataFrame(temp_order["items"])
        remove_item = st.selectbox("Remove item to from order", options=order_item_df["item_name"], index=0)
        remove_btn = st.form_submit_button("Remove item from order")

        if remove_btn:

            order_item = order_item_df[order_item_df["item_name"] == remove_item]
            order_item_remove = OrderItemRemove(
                id=order_item["id"],
                order_id=temp_order["id"]
            )
            remove_item_from_order(order_item_remove.dict(), st.session_state.jwt_token)
            if len(order_item_df) == 1:
                delete_pending_order(int(temp_order["id"]), st.session_state.jwt_token)
            st.success("Item removed from order")
            st.rerun()

    if st.button("Purchase order"):
        response = purchase_order(int(temp_order["id"]), st.session_state.jwt_token)
        if not response:
            st.success("Order purchased")
        else:
            st.error(response["detail"])
        st.rerun()


def new_order_form(items_df):
    with st.form(key="new_order"):
        add_item = st.selectbox("Add item to order", options=items_df["name"], index=0)
        quantity = st.number_input("How many do you want?", min_value=0, format="%d")
        shipping_address = st.text_input("Shipping address", key="shipping_address")
        new_btn = st.form_submit_button("Add Item to order")

        if new_btn:
            if add_item and quantity and shipping_address:
                item = items_df[items_df["name"] == add_item]
                item_id = item["id"]
                order_request = OrderRequest(
                    shipping_address=shipping_address,
                    order_item=OrderItem(
                        item_id=item_id,
                        quantity=quantity
                    )
                )

                response = create_pending_order(order_request.dict(), st.session_state.jwt_token)
                if response:
                    st.write(response["detail"])
                else:
                    st.success("New pending order created")
                    st.rerun()
            else:
                st.error("Please fill item, quantity and shipping address")


def show_order_details(order: OrderResponse):
    st.write(f"Order Date: {order["order_date"]}")
    st.write(f"Shipping address: {order["shipping_address"]}")
    st.write(f"Total price: ${order["total_price"]}")
    if order["items"]:
        df = pd.DataFrame(order["items"])
        df = df.drop(columns=["id"], axis=1)
        st.dataframe(df, use_container_width=True, hide_index=True)
