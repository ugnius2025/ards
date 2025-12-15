import streamlit as st

st.title("🏠 AI Real Estate Assistant (Experimental)")

DISTRICT_AVG = {
    "Centras": 3500,
    "Žirmūnai": 2600,
    "Antakalnis": 3000,
    "Pilaitė": 2400,
    "Pašilaičiai": 2300,
}

price = st.number_input("Price (€)", min_value=10000, step=5000)
size = st.number_input("Size (m²)", min_value=10.0, step=1.0)
district = st.selectbox("District", DISTRICT_AVG.keys())

if price and size:
    ppm2 = price / size
    avg = DISTRICT_AVG[district]
    diff = (ppm2 - avg) / avg

    st.metric("Price per m²", f"{ppm2:,.0f} €")

    if diff < -0.15:
        verdict = "🟢 Potentially undervalued"
    elif diff > 0.15:
        verdict = "🔴 Likely overpriced"
    else:
        verdict = "🟡 Around market price"

    st.subheader(verdict)

year = st.number_input("Year built", min_value=1900, max_value=2025, step=1)
renovated = st.checkbox("Renovated")

flags = []

if year < 1960 and renovated:
    flags.append("⚠ Old building + renovation — check quality")

if diff < -0.25:
    flags.append("⚠ Very cheap — verify documents & condition")

if flags:
    st.subheader("Risk flags")
    for f in flags:
        st.write(f)

