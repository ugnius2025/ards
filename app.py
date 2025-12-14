import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup

# -----------------------
# CONFIG
# -----------------------
HEADERS = {
    "User-Agent": "Mozilla/5.0 (experimental research)"
}

# -----------------------
# SCRAPING FUNCTION
# -----------------------
@st.cache_data(ttl=300)
def get_latest_vilnius_ads(limit=10):
    url = "https://www.aruodas.lt/butai/vilniuje/"
    r = requests.get(url, headers=HEADERS, timeout=10)

    if r.status_code != 200:
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    ads = []

    for card in soup.select("div.list-row")[:limit]:
        title_el = card.select_one("h3")
        price_el = card.select_one(".price")
        link_el = card.select_one("a")

        title = title_el.get_text(strip=True) if title_el else "No title"
        price = price_el.get_text(strip=True) if price_el else "No price"

        link = (
            "https://www.aruodas.lt" + link_el["href"]
            if link_el and link_el.get("href", "").startswith("/")
            else None
        )

        ads.append({
            "Title": title,
            "Price": price,
            "Link": link
        })

    return ads


# -----------------------
# STREAMLIT UI
# -----------------------
st.set_page_config(page_title="Aruodas – Experimental", layout="wide")

st.title("🏠 Latest Vilnius Apartment Listings (Aruodas)")
st.caption("Experimental, read-only, low-frequency scraping")

with st.spinner("Loading latest listings…"):
    ads = get_latest_vilnius_ads(limit=10)

if not ads:
    st.error("No listings found or site unavailable.")
else:
    df = pd.DataFrame(ads)

    for _, row in df.iterrows():
        st.markdown(f"### {row['Title']}")
        st.write(row["Price"])
        if row["Link"]:
            st.markdown(f"[Open listing]({row['Link']})")
        st.divider()

