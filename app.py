import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Kite Paing Store Manager", layout="wide")

# --- DATA INITIALIZATION ---
# တကယ့်လက်တွေ့မှာတော့ ဒီ Data တွေကို Database မှာ သိမ်းရပါမယ်
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame([
        {"ID": "1001", "Name": "Coke", "Category": "Drinks", "Stock": 50, "Buy": 800, "Sell": 1000},
        {"ID": "1002", "Name": "Mama Noodles", "Category": "Food", "Stock": 5, "Buy": 400, "Sell": 600}
    ])

if 'sales' not in st.session_state:
    st.session_state.sales = pd.DataFrame(columns=["Date", "Name", "Qty", "Total", "Profit"])

# --- SIDEBAR MENU ---
st.sidebar.title("🏪 Ko Paing Store")
menu = ["📊 Dashboard", "🛒 POS (အရောင်း)", "📦 ပစ္စည်းစာရင်း", "💸 အသုံးစရိတ်/အစီရင်ခံစာ"]
choice = st.sidebar.radio("Menu", menu)

# --- 1. DASHBOARD ---
if choice == "📊 Dashboard":
    st.header("အရောင်းအနှစ်ချုပ်")
    
    total_sales = st.session_state.sales['Total'].sum()
    total_profit = st.session_state.sales['Profit'].sum()
    low_stock_count = len(st.session_state.inventory[st.session_state.inventory['Stock'] <= 5])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("စုစုပေါင်း ရောင်းရငွေ", f"{total_sales:,.0f} MMK")
    col2.metric("စုစုပေါင်း အမြတ်", f"{total_profit:,.0f} MMK")
    col3.metric("လက်ကျန်နည်းနေသော ပစ္စည်း", f"{low_stock_count} မျိုး", delta_color="inverse")

    if not st.session_state.sales.empty:
        fig = px.line(st.session_state.sales, x="Date", y="Total", title="နေ့စဉ်အရောင်းတက်နှုန်း")
        st.plotly_chart(fig, use_container_width=True)

# --- 2. POS (SALES) ---
elif choice == "🛒 POS (အရောင်း)":
    st.header("အရောင်းဌာန")
    p_id = st.text_input("Barcode ဖတ်ရန် သို့မဟုတ် ID ရိုက်ထည့်ပါ", placeholder="Scan here...")
    
    if p_id:
        items = st.session_state.inventory
        item = items[items['ID'] == p_id]
        
        if not item.empty:
            st.success(f"တွေ့ရှိသည်: {item.iloc[0]['Name']}")
            qty = st.number_input("အရေအတွက်", min_value=1, max_value=int(item.iloc[0]['Stock']), value=1)
            
            if st.button("ရောင်းမည် (Confirm)"):
                # စာရင်းပြင်ဆင်ခြင်း
                total = qty * item.iloc[0]['Sell']
                profit = qty * (item.iloc[0]['Sell'] - item.iloc[0]['Buy'])
                
                new_sale = {
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Name": item.iloc[0]['Name'],
                    "Qty": qty,
                    "Total": total,
                    "Profit": profit
                }
                
                # Update Session State
                st.session_state.sales = pd.concat([st.session_state.sales, pd.DataFrame([new_sale])], ignore_index=True)
                st.session_state.inventory.loc[st.session_state.inventory['ID'] == p_id, 'Stock'] -= qty
                st.balloons()
                st.success(f"ရောင်းပြီးပါပြီ။ ကျသင့်ငွေ - {total:,.0f} MMK")
        else:
            st.warning("ဒီ ID နဲ့ ပစ္စည်းရှာမတွေ့ပါ။")

# --- 3. INVENTORY ---
elif choice == "📦 ပစ္စည်းစာရင်း":
    st.header("ပစ္စည်းလက်ကျန် စစ်ဆေးခြင်း")
    
    # ပစ္စည်းအသစ်ထည့်ရန် Form
    with st.expander("➕ ပစ္စည်းအသစ်ထည့်ရန်"):
        with st.form("add_form"):
            new_id = st.text_input("ID / Barcode")
            new_name = st.text_input("ပစ္စည်းအမည်")
            new_cat = st.selectbox("အမျိုးအစား", ["Food", "Drinks", "Cosmetic", "Other"])
            new_stock = st.number_input("အရေအတွက်", min_value=1)
            new_buy = st.number_input("ရင်းဈေး")
            new_sell = st.number_input("ရောင်းဈေး")
            
            if st.form_submit_button("စာရင်းသွင်းမည်"):
                new_data = {"ID": new_id, "Name": new_name, "Category": new_cat, "Stock": new_stock, "Buy": new_buy, "Sell": new_sell}
                st.session_state.inventory = pd.concat([st.session_state.inventory, pd.DataFrame([new_data])], ignore_index=True)
                st.rerun()

    # ပြသခြင်း
    st.table(st.session_state.inventory)

# --- 4. EXPENSE / REPORT ---
elif choice == "💸 အသုံးစရိတ်/အစီရင်ခံစာ":
    st.header("အရောင်းမှတ်တမ်း အပြည့်အစုံ")
    st.dataframe(st.session_state.sales, use_container_width=True)
    
    if st.button("Excel File ထုတ်ယူမည်"):
        st.write("Excel ထုတ်ယူခြင်း လုပ်ဆောင်ချက်...")
