import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Page Configuration
st.set_page_config(page_title="My Store POS", layout="wide")

def connect_sheet():
    # Streamlit Secrets ထဲက PRIVATE_KEY ကို ယူခြင်း
    try:
        private_key = st.secrets["PRIVATE_KEY"]
    except Exception:
        st.error("GitHub Secrets missing! ကျေးဇူးပြု၍ Streamlit Cloud Settings > Secrets ထဲမှာ PRIVATE_KEY ကို အရင်ထည့်ပေးပါ။")
        return None

    # Google Service Account Credentials
    creds_info = {
        "type": "service_account",
        "project_id": "my-store-pos-496112",
        "private_key_id": "97d4a09955630e08ec946cdab8d914aa9e538de1",
        "private_key": private_key.replace("\\n", "\n"),
        "client_email": "mystore-manager@my-store-pos-496112.iam.gserviceaccount.com",
        "client_id": "113930516733930481428",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/mystore-manager%40my-store-pos-496112.iam.gserviceaccount.com"
    }

    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(creds_info, scopes=scope)
        client = gspread.authorize(creds)
        # Google Sheet ID
        return client.open_by_key("156iRKWXZIspmqZSb5TkZV02Z2830q-PNzucbSAKDwhI").get_worksheet(0)
    except Exception as e:
        st.error(f"Sheet ချိတ်ဆက်မှု အမှား: {e}")
        return None

# App UI
st.title("🏪 My Store POS")
sheet = connect_sheet()

if sheet:
    menu = ["ပစ္စည်းကြည့်ရန်", "ပစ္စည်းအသစ်ထည့်ရန်"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "ပစ္စည်းကြည့်ရန်":
        st.subheader("📦 လက်ရှိပစ္စည်းစာရင်း")
        data = sheet.get_all_records()
        st.dataframe(pd.DataFrame(data), use_container_width=True)

    elif choice == "ပစ္စည်းအသစ်ထည့်ရန်":
        st.subheader("➕ ပစ္စည်းအသစ်ထည့်ရန်")
        with st.form("add_form", clear_on_submit=True):
            p_id = st.text_input("Product ID")
            p_name = st.text_input("Item Name")
            p_price = st.number_input("Price", min_value=0)
            p_stock = st.number_input("Stock", min_value=0)
            if st.form_submit_button("သိမ်းဆည်းမည်"):
                sheet.append_row([p_id, p_name, p_price, p_stock])
                st.success("အောင်မြင်စွာ စာရင်းသွင်းပြီးပါပြီ!")
