import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import os
import json

# --- Google Sheets Configuration ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# GitHub Secrets ထဲက GOOGLE_CREDENTIALS ကို ဖတ်ခြင်း
creds_json = os.getenv("GOOGLE_CREDENTIALS")

# Sheet ကို ချိတ်ဆက်ရန် Variable ကို ကြိုတင်သတ်မှတ်ခြင်း
sheet = None

if creds_json:
    try:
        creds_dict = json.loads(creds_json)
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)
        
        # လူကြီးမင်း၏ Sheet ID
        SHEET_ID = "156iRKWXZIspmqZSb5TkZV02Z2830q-PNzucbSAKDwhI"
        # လူကြီးမင်း Google Sheet အောက်ခြေက နာမည် (Sheet1 လို့ပဲ ထားလိုက်ပါတယ်)
        sheet = client.open_by_key(SHEET_ID).get_worksheet(0) 
    except Exception as e:
        st.error(f"Google Sheet ချိတ်ဆက်မှု အမှားရှိနေပါသည်: {e}")
else:
    st.error("GitHub Secrets ထဲမှာ GOOGLE_CREDENTIALS ကို ရှာမတွေ့ပါ။")

def get_data():
    if sheet:
        try:
            data = sheet.get_all_records()
            return pd.DataFrame(data)
        except:
            return pd.DataFrame()
    return pd.DataFrame()

# --- Streamlit App UI ---
st.set_page_config(page_title="My Store POS", layout="wide")
st.title("🏪 My Store - POS System")

menu = ["အရောင်းဖွင့်ရန်", "ပစ္စည်းစာရင်းကြည့်ရန်", "ပစ္စည်းအသစ်ထည့်ရန်"]
choice = st.sidebar.selectbox("Menu ရွေးချယ်ပါ", menu)

if choice == "အရောင်းဖွင့်ရန်":
    st.header("🛒 အရောင်းစာမျက်နှာ")
    df = get_data()
    if not df.empty and 'Name' in df.columns:
        item_list = df['Name'].tolist()
        selected_item = st.selectbox("ပစ္စည်းရွေးပါ", item_list)
        qty = st.number_input("အရေအတွက်", min_value=1, value=1)
        
        # ဈေးနှုန်းရှာခြင်း
        price_val = df[df['Name'] == selected_item]['Price'].values[0]
        
        if st.button("ရောင်းမည်"):
            total = qty * price_val
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
            if sheet:
                if p_id and p_name:
                    try:
                        sheet.append_row([p_id, p_name, p_price, p_stock])
                        st.success(f"{p_name} ကို စာရင်းထဲသို့ ထည့်သွင်းပြီးပါပြီ!")
                    except Exception as e:
                        st.error(f"Error adding row: {e}")
                else:
                    st.warning("ID နှင့် နာမည်ကို ဖြည့်ပေးပါ။")
            else:
                st.error("Google Sheet နှင့် ချိတ်ဆက်မ



