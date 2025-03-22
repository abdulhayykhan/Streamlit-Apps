import streamlit as st
import requests
import time

def get_exchange_rate(base_currency, target_currency):
    api_key = "your_api_key_here"  # Replace with your API key
    if api_key == "your_api_key_here" or not api_key:
        st.error("❌ API key is missing! Please provide a valid API key.")
        return None
    
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        data = response.json()
        
        if "conversion_rates" in data:
            return data["conversion_rates"].get(target_currency, None)
        else:
            st.error("❌ Unexpected API response format.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ API Request failed: {e}")
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
            st.error("❌ Failed to fetch exchange rate. Please check your API key or try again later.")
    
    st.markdown("---")
    st.info("🔹 Exchange rates are fetched in real-time from ExchangeRate-API.")
    
if __name__ == "__main__":
    main()
