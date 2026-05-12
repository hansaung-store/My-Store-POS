import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import os
import json

st.set_page_config(page_title="My Store POS", layout="wide")

# Google Sheets Connection Function
def connect_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_json = os.getenv("GOOGLE_CREDENTIALS")
    
    if not creds_json:
        st.error("GitHub Secrets missing!")
        return None

    try:
        # JSON ထဲက ပြဿနာတက်တတ်တဲ့ စာလုံးတွေကို အလိုအလျောက် ပြင်ပေးခြင်း
        creds_dict = json.loads(creds_json, strict=False)
        if "private_key" in creds_dict:
            creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
            
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)
        # လူကြီးမင်း၏ Sheet ID
        SHEET_ID = "156iRKWXZIspmqZSb5TkZV02Z2830q-PNzucbSAKDwhI"
        return client.open_by_key(SHEET_ID).get_worksheet(0)
    except Exception as e:
        st.error(f"Connection Error: {str(e)}")
        return None

sheet = connect_sheet()

st.title("🏪 My Store POS")
menu = ["ပစ္စည်းကြည့်ရန်", "ပစ္စည်းအသစ်ထည့်ရန်"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "ပစ္စည်းကြည့်ရန်":
    if sheet:
        data = sheet.get_all_records()
        st.dataframe(pd.DataFrame(data), use_container_width=True)

elif choice == "ပစ္စည်းအသစ်ထည့်ရန်":
    with st.form("add_form", clear_on_submit=True):
        p_id = st.text_input("Product ID")
        p_name = st.text_input("Item Name")
        p_price = st.number_input("Price", min_value=0)
        p_stock = st.number_input("Stock", min_value=0)
        
        if st.form_submit_button("စာရင်းသွင်းမည်"):
            if sheet and p_id and p_name:
                sheet.append_row([p_id, p_name, p_price, p_stock])
                st.success("အောင်မြင်စွာ သိမ်းဆည်းပြီးပါပြီ!")
            else:
                st.error("အချက်အလက် ပြည့်စုံစွာ ဖြည့်ပေးပါ!")


