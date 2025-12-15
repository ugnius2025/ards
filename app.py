import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup

# -----------------------
# CONFIG
# -----------------------
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
}

# -----------------------
# SCRAPING FUNCTION
# -----------------------
def get_latest_vilnius_ads(limit=10):
    url = "https://www.aruodas.lt/butai/vilniuje/?days=1"
    r = requests.get(url, headers=HEADERS, timeout=10)
    if r.status_code != 200:
        return []

    soup = BeautifulSoup(r.text, "html.parser")

    # Try a more general listing selector
    items = soup.select(".list-card") or soup.select("article") or soup.find_all("h3")

    ads = []
    count = 0

    for item in items:
        # Stop once we reach the limit
        if count >= limit:
            break

        # Try to get title-like text
        text = item.get_text(separator=" ", strip=True)
        if not text:
            continue

        # Try to find price inside this section
        price_el = item.find_next(string=lambda t: "€" in t)

        # Try to find link
        link_el = item.find("a", href=True)
        link = link_el["href"] if link_el else None
        if link and link.startswith("/"):
            link = "https://www.aruodas.lt" + link

        ads.append({
            "title": text,
            "price": price_el.strip() if price_el else "No price",
            "link": link,
        })
        count += 1

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

