import pandas as pd
import streamlit as st

from model.favorite_item import FavoriteItem
from ui.api.favorite_items_api import get_favorite_items, create_favorite_item, remove_favorite_item
from ui.api.item_api import get_all_items


def tab_favorite_items():

    with st.form("add_favorite_item"):
        items = get_all_items()
        items_df = pd.DataFrame(items)
        add_item = st.selectbox("choose a column", options=items_df["name"], index=0)
        add_favorite_btn = st.form_submit_button("Add Favorite Item")
        if add_favorite_btn:
            item = items_df[items_df["name"] == add_item]
            item_id = item["id"]

            favorite_item = FavoriteItem(
                item_id=item_id
            )

            response = create_favorite_item(favorite_item.dict(), st.session_state.jwt_token)
            if response:
                st.error(response["detail"])
            else:
                st.success("Favorite item added")

    favorite_items = get_favorite_items(st.session_state.jwt_token)

    if favorite_items:
        remove_form(favorite_items)
        st.subheader("Your Favorite Items:")
        favorite_items_df = pd.DataFrame(favorite_items)
        favorite_items_df = favorite_items_df.drop(["id", "user_id"], axis=1)
        st.dataframe(favorite_items_df, use_container_width=True, hide_index=True)
    else:
        st.write("No favorite items added")


def remove_form(favorite_items):
    with st.form("remove_favorite_item"):
        options = []
        for favorite_item in favorite_items:
            options.append(favorite_item["item_name"])
        remove_item = st.selectbox("choose a column", options=options, index=0)
        remove_favorite_btn = st.form_submit_button("Remove Favorite Item")
        if remove_favorite_btn:
            favorite_item_id = -1
            for favorite_item in favorite_items:
                if favorite_item["item_name"] == remove_item:
                    favorite_item_id = favorite_item["id"]
            response = remove_favorite_item(int(favorite_item_id), st.session_state.jwt_token)
            if response:
                st.error(response["detail"])
            else:
                st.success("Favorite item removed")
                st.rerun()
