import streamlit as st
import requests
import time

def get_exchange_rate(base_currency, target_currency):
    api_key = "your_api_key_here"  # Replace with your API key
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200 and "conversion_rates" in data:
        return data["conversion_rates"].get(target_currency, None)
    else:
        return None

def main():
    st.set_page_config(page_title="Currency Converter", page_icon="💰", layout="centered")
    st.title("💱 Currency Converter")
    st.markdown("### Convert currencies instantly with real-time exchange rates!")
    
    # Currency selection
    currencies = ["USD", "EUR", "GBP", "INR", "JPY", "CAD", "AUD", "CNY", "PKR", "AED", "SAR", "QAR", "MYR", "THB", "SGD", "TRY"]
    col1, col2 = st.columns(2)
    with col1:
        base_currency = st.selectbox("Select base currency:", currencies)
    with col2:
        target_currency = st.selectbox("Select target currency:", currencies)
    
    amount = st.number_input("Enter amount:", min_value=0.01, format="%.2f", value=1.00)
    
    if st.button("🔄 Convert"):
        with st.spinner("Fetching latest exchange rates..."):
            time.sleep(1)
            rate = get_exchange_rate(base_currency, target_currency)
        
        if rate:
            converted_amount = amount * rate
            st.success(f"💰 {amount} {base_currency} = {converted_amount:.2f} {target_currency}")
            st.metric(label=f"Exchange Rate ({base_currency} → {target_currency})", value=f"{rate:.4f}")
        else:
            st.error("❌ Failed to fetch exchange rate. Please try again later.")
    
    st.markdown("---")
    st.info("🔹 Exchange rates are fetched in real-time from ExchangeRate-API.")
    
if __name__ == "__main__":
    main()
