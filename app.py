
import streamlit as st
import pandas as pd
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="Ko Paing Store Manager", layout="wide")

# Initialize Session State for Inventory and Sales
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame(columns=['ID', 'Name', 'Price', 'Stock'])
if 'sales' not in st.session_state:
    st.session_state.sales = pd.DataFrame(columns=['Date', 'ID', 'Name', 'Qty', 'Total'])

st.title("🛒 Ko Paing Store Manager")

# Sidebar Menu
menu = ["Dashboard", "POS (အရောင်း)", "ပစ္စည်းစာရင်း", "အစီရင်ခံစာ"]
choice = st.sidebar.selectbox("Menu", menu)

# --- 1. Dashboard ---
if choice == "Dashboard":
    st.subheader("အရောင်းအနှစ်ချုပ်")
    col1, col2, col3 = st.columns(3)
    total_revenue = st.session_state.sales['Total'].sum()
    total_items = len(st.session_state.inventory)
    
    col1.metric("စုစုပေါင်း ရောင်းရငွေ", f"{total_revenue:,} MMK")
    col2.metric("လက်ရှိပစ္စည်းအမျိုးအမည်", f"{total_items} မျိုး")
    col3.metric("ယနေ့အော်ဒါ", len(st.session_state.sales))

# --- 2. POS (အရောင်း) ---
elif choice == "POS (အရောင်း)":
    st.subheader("🛍 အရောင်းဌာန")
    
    # Scan အကွက် (Scan စက်ရော ဖုန်းအတွက်ပါ သုံးနိုင်သည်)
    barcode_input = st.text_input("Barcode ကို Scan ဖတ်ပါ သို့မဟုတ် ID ရိုက်ထည့်ပါ", key="barcode_scan")
    
    if barcode_input:
        product = st.session_state.inventory[st.session_state.inventory['ID'] == barcode_input]
        
        if not product.empty:
            p_name = product.iloc[0]['Name']
            p_price = product.iloc[0]['Price']
            st.success(f"တွေ့ရှိသည့်ပစ္စည်း: {p_name} | ဈေးနှုန်း: {p_price} MMK")
            
            qty = st.number_input("အရေအတွက်", min_value=1, value=1)
            if st.button("ရောင်းမည်"):
                new_sale = {
                    'Date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                    'ID': barcode_input,
                    'Name': p_name,
                    'Qty': qty,
                    'Total': p_price * qty
                }
                st.session_state.sales = pd.concat([st.session_state.sales, pd.DataFrame([new_sale])], ignore_index=True)
                st.balloons()
                st.success("ရောင်းချမှု အောင်မြင်ပါသည်!")
        else:
            st.error("ဤ Barcode ဖြင့် ပစ္စည်းစာရင်း ရှာမတွေ့ပါ။ အရင် စာရင်းသွင်းပေးပါ။")

# --- 3. ပစ္စည်းစာရင်း ---
elif choice == "ပစ္စည်းစာရင်း":
    st.subheader("📦 ပစ္စည်းအသစ်သွင်းရန်")
    
    with st.form("inventory_form"):
        # ဤနေရာတွင် Cursor ချပြီး Scan စက်ဖြင့် ဖတ်နိုင်သည်
        p_id = st.text_input("Barcode ID (Scan ဖတ်ပါ)")
        p_name = st.text_input("ပစ္စည်းအမည်")
        p_price = st.number_input("ဈေးနှုန်း (MMK)", min_value=0)
        p_stock = st.number_input("လက်ကျန်အရေအတွက်", min_value=0)
        
        if st.form_submit_button("စာရင်းသွင်းမည်"):
            new_item = {'ID': p_id, 'Name': p_name, 'Price': p_price, 'Stock': p_stock}
            st.session_state.inventory = pd.concat([st.session_state.inventory, pd.DataFrame([new_item])], ignore_index=True)
            st.success("စာရင်းသွင်းပြီးပါပြီ!")
    
    st.write("### လက်ရှိပစ္စည်းစာရင်း")
    st.dataframe(st.session_state.inventory, use_container_width=True)

# --- 4. အစီရင်ခံစာ ---
elif choice == "အစီရင်ခံစာ":
    st.subheader("📊 အရောင်းမှတ်တမ်း")
    st.dataframe(st.session_state.sales, use_container_width=True)
