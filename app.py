import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import os
import json

# Google Sheets Setup
# GitHub Secrets ထဲက GOOGLE_CREDENTIALS ကို ပြန်ဖတ်ခြင်း
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_json = os.getenv("GOOGLE_CREDENTIALS")

if creds_json:
    creds_dict = json.loads(creds_json)
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    
    # လူကြီးမင်းပေးထားသော Sheet ID ဖြင့် ချိတ်ဆက်ခြင်း
    SHEET_ID = "156iRKWXZIspmqZSb5TkZV02Z2830q-PNzucbSAKDwhI"
    sheet = client.open_by_key(SHEET_ID).worksheet("Inventory")
else:
    st.error("Google Credentials not found in Environment Variables!")

def get_data():
    return pd.DataFrame(sheet.get_all_records())

# Streamlit App UI
st.set_page_config(page_title="My Store POS", layout="wide")
st.title("🏪 My Store - POS System")

menu = ["အရောင်းဖွင့်ရန်", "ပစ္စည်းစာရင်းကြည့်ရန်", "ပစ္စည်းအသစ်ထည့်ရန်"]
choice = st.sidebar.selectbox("Menu ရွေးချယ်ပါ", menu)

if choice == "အရောင်းဖွင့်ရန်":
    st.header("🛒 အရောင်းစာမျက်နှာ")
    df = get_data()
    if not df.empty:
        item = st.selectbox("ပစ္စည်းရွေးပါ", df['Name'].tolist())
        qty = st.number_input("အရေအတွက်", min_value=1, value=1)
        price = df[df['Name'] == item]['Price'].values[0]
        
        if st.button("ရောင်းမည်"):
            st.success(f"{item} {qty} ခု ရောင်းပြီးပါပြီ။ စုစုပေါင်း: {qty * price} Ks")
            # ဒီနေရာတွင် Stock နှုတ်သည့် Code ထပ်ထည့်နိုင်သည်

elif choice == "ပစ္စည်းစာရင်းကြည့်ရန်":
    st.header("📊 လက်ရှိပစ္စည်းစာရင်း")
    df = get_data()
    st.dataframe(df, use_container_width=True)

elif choice == "ပစ္စည်းအသစ်ထည့်ရန်":
    st.header("➕ ပစ္စည်းအသစ်စာရင်းသွင်းရန်")
    with st.form("add_form"):
        new_id = st.text_input("Product ID")
        new_name = st.text_input("Item Name")
        new_price = st.number_input("Price", min_value=0)
        new_stock = st.number_input("Stock Amount", min_value=0)
        
        if st.form_submit_button("စာရင်းသွင်းမည်"):
            sheet.append_row([new_id, new_name, new_price, new_stock])
            st.success("စာရင်းထဲသို့ ထည့်သွင်းပြီးပါပြီ!")

