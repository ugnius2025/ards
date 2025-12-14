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

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    }

    r = requests.get(url, headers=headers, timeout=10)

    if r.status_code != 200:
        st.error(f"HTTP status: {r.status_code}")
        return []

    soup = BeautifulSoup(r.text, "html.parser")

    cards = soup.select("div.list-row")

    ads = []
    for card in cards[:limit]:
        title = card.select_one("h3")
        price = card.select_one(".price")
        link = card.select_one("a")

        ads.append({
            "title": title.get_text(strip=True) if title else "No title",
            "price": price.get_text(strip=True) if price else "No price",
            "link": (
                "https://www.aruodas.lt" + link["href"]
                if link and link.get("href", "").startswith("/")
                else None
            ),
        )

    return ads


# -----------------------
# STREAMLIT UI
# -----------------------
st.set_page_config(page_title="Aruodas – Experimental", layout="wide")

st.title("🏠 Latest Vilnius Apartment Listings (Aruodas)")
st.caption("Experimental, read-only, low-frequency scraping")

with st.spinner("Loading latest listings…"):
    ads = get_latest_vilnius_ads(limit=10)

st.write(ads)

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

