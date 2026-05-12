import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import os
import json

# Google Sheets Setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = os.getenv("GOOGLE_CREDENTIALS")

if creds_json:
    try:
        creds_dict = json.loads(creds_json)
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)
        
        # လူကြီးမင်း၏ Sheet ID
        SHEET_ID = "156iRKWXZIspmqZSb5TkZV02Z2830q-PNzucbSAKDwhI"
        sheet = client.open_by_key(SHEET_ID).worksheet("Inventory")
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
else:
    st.error("GitHub Secrets ထဲမှာ GOOGLE_CREDENTIALS ထည့်ဖို့ လိုအပ်နေပါသေးတယ်!")

def get_data():
    try:
        data = sheet.get_all_records()
        return pd.DataFrame(data)
    except:
        return pd.DataFrame()

# Streamlit App UI
st.set_page_config(page_title="My Store POS", layout="wide")
st.title("🏪 My Store - POS System")

menu = ["အရောင်းဖွင့်ရန်", "ပစ္စည်းစာရင်းကြည့်ရန်", "ပစ္စည်းအသစ်ထည့်ရန်"]
choice = st.sidebar.selectbox("Menu ရွေးချယ်ပါ", menu)

if choice == "အရောင်းဖွင့်ရန်":
    st.header("🛒 အရောင်းစာမျက်နှာ")
    df = get_data()
    if not df.empty:
        item_list = df['Name'].tolist()
        selected_item = st.selectbox("ပစ္စည်းရွေးပါ", item_list)
        qty = st.number_input("အရေအတွက်", min_value=1, value=1)
        
        # ဈေးနှုန်းရှာခြင်း
        price = df[df['Name'] == selected_item]['Price'].values[0]
        
        if st.button("ရောင်းမည်"):
            total = qty * price
            st.success(f"{selected_item} {qty} ခု ရောင်းပြီးပါပြီ။ စုစုပေါင်း: {total} Ks")
    else:
        st.warning("ပစ္စည်းစာရင်း မရှိသေးပါ။ အရင်ဆုံး ပစ္စည်းစာရင်းသွင်းပါ။")

elif choice == "ပစ္စည်းစာရင်းကြည့်ရန်":
    st.header("📊 လက်ရှိပစ္စည်းစာရင်း")
    df = get_data()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("စာရင်းထဲမှာ ဘာမှမရှိသေးပါဘူး။")

elif choice == "ပစ္စည်းအသစ်ထည့်ရန်":
    st.header("➕ ပစ္စည်းအသစ်စာရင်းသွင်းရန်")
    with st.form("add_form", clear_on_submit=True):
        p_id = st.text_input("Product ID")
        p_name = st.text_input("Item Name")
        p_price = st.number_input("Price", min_value=0)
        p_stock = st.number_input("Stock Amount", min_value=0)
        
        submit_button = st.form_submit_button("စာရင်းသွင်းမည်")
        
        if submit_button:
            if p_id and p_name:
                try:
                    # Google Sheet ထဲသို့ တိုက်ရိုက်သိမ်းခြင်း
                    sheet.append_row([p_id, p_name, p_price, p_stock])
                    st.success(f"{p_name} ကို စာရင်းထဲသို့ ထည့်သွင်းပြီးပါပြီ!")
                except Exception as e:
                    st.error(f"Error: {e}")
            else:
                st.warning("ID နဲ့ နာမည်ကို မဖြစ်မနေ ဖြည့်ပေးပါ။")


