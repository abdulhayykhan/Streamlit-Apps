import streamlit as st
import requests

def get_exchange_rate(api_key, base_currency, target_currency):
    if not api_key:
        st.error("❌ API key is missing! Please enter a valid API key.")
        return None

    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "conversion_rates" in data and target_currency in data["conversion_rates"]:
            return data["conversion_rates"][target_currency]
        else:
            st.error(f"❌ Unexpected API response: {data}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"❌ API Request failed: {e}")
        return None

def main():
    st.set_page_config(page_title="Currency Converter", page_icon="💰", layout="centered")
    st.title("💱 Currency Converter")
    st.markdown("### Convert currencies instantly with real-time exchange rates!")

    # API Key Input
    api_key = st.text_input("🔑 Enter your ExchangeRate-API key:", type="password")

    # Currency selection
    currencies = ["USD", "EUR", "GBP", "INR", "JPY", "CAD", "AUD", "CNY", "PKR", "AED", "SAR", "QAR", "MYR", "THB", "SGD", "TRY"]
    
    col1, col2 = st.columns(2)
    with col1:
        base_currency = st.selectbox("Select base currency:", currencies, index=currencies.index("USD"))
    with col2:
        target_currency = st.selectbox("Select target currency:", currencies, index=currencies.index("PKR"))

    amount = st.number_input("Enter amount:", min_value=0.01, format="%.2f", value=1.00)

    if st.button("🔄 Convert"):
        rate = get_exchange_rate(api_key, base_currency, target_currency)

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
