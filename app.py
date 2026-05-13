import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="My Store POS", layout="wide")

def connect_sheet():
    try:
        # Secrets ထဲက gcp_service_account တစ်ခုလုံးကို ယူမယ်
        creds_dict = dict(st.secrets["gcp_service_account"])
        
        # \n ပြဿနာကို ရှင်းဖို့ private_key ကို format ပြန်ပြင်မယ်
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")

        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)
        
        return client.open_by_key("156iRKWXZIspmqZSb5TkZV02Z2830q-PNzucbSAKDwhI").get_worksheet(0)
    except Exception as e:
        st.error(f"Sheet ချိတ်ဆက်မှု အမှား: {e}")
        return None

st.title("🏪 My Store POS")
sheet = connect_sheet()

if sheet:
    st.success("Google Sheet နဲ့ ချိတ်ဆက်မိပါပြီ။")
    data = sheet.get_all_records()
    if data:
        st.dataframe(pd.DataFrame(data), use_container_width=True)
    else:
        st.info("ပြသရန် ဒေတာမရှိသေးပါ။")


