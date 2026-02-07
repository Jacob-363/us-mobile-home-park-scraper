import time
import logging
from typing import List, Dict, Optional

import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://www.mobilehomeparkstore.com"
STATES_URL = f"{BASE_URL}/mobile-home-park-directory/states"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ParkScraper/1.0)"
}

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


def get_soup(session: requests.Session, url: str) -> BeautifulSoup:
    response = session.get(url, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def get_contact_info(session: requests.Session, park_url: str) -> Optional[str]:
    try:
        soup = get_soup(session, park_url)

        contact_anchor = soup.select_one("div.d-grid a[href]")
        if not contact_anchor:
            return None

        contact_page_url = BASE_URL + contact_anchor["href"]
        contact_soup = get_soup(session, contact_page_url)

        phone_link = contact_soup.find("a", href=lambda h: h and h.startswith("tel:"))
        return phone_link["href"].replace("tel:", "") if phone_link else None

    except requests.RequestException as exc:
        logging.warning(f"Failed to fetch contact info for {park_url}: {exc}")
        return None


def parse_park_element(
        session: requests.Session,
        park
) -> Optional[Dict[str, Optional[str]]]:
    name_div = park.find("div", class_="col-sm-5 mb-1")
    address_divs = park.find_all("div", class_="col-sm-5")
    lot_div = park.find("div", class_="col-sm-2")

    if not name_div or not address_divs:
        return None

    name_anchor = name_div.find("a")
    name = name_anchor.get_text(strip=True) if name_anchor else None
    park_url = name_anchor["href"] if name_anchor else None

    address = address_divs[1].get_text(strip=True) if len(address_divs) > 1 else None

    lot_count = (
        lot_div.get_text(strip=True).replace("Lots", "").strip()
        if lot_div else None
    )

    phone = get_contact_info(session, park_url) if park_url else None

    time.sleep(0.5)  # polite scraping

    return {
        "Park Name": name,
        "Address": address,
        "Space Count": lot_count,
        "Phone Number": phone,
    }


def get_data_from_state_page(
        session: requests.Session,
        url: str
) -> List[Dict[str, Optional[str]]]:
    soup = get_soup(session, url)
    park_elements = soup.find_all("div", class_="row my-2")

    data = []

    for park in park_elements:
        park_data = parse_park_element(session, park)
        if park_data:
            data.append(park_data)

    return data


def scrape_data_from_states() -> List[Dict[str, Optional[str]]]:
    all_data = []

    with requests.Session() as session:
        session.headers.update(HEADERS)

        soup = get_soup(session, STATES_URL)

        state_links = {
            BASE_URL + a["href"]
            for a in soup.find_all("a", href=True)
            if a["href"].startswith("/mobile-home-park-directory/")
        }

        for state_url in sorted(state_links):
            logging.info(f"Scraping {state_url}")
            state_data = get_data_from_state_page(session, state_url)
            all_data.extend(state_data)

    return all_data


def main() -> None:
    data = scrape_data_from_states()
    df = pd.DataFrame(data)
    df.to_csv("mobile_parks_2.csv", index=False)
    logging.info("Data saved to mobile_parks.csv")


if __name__ == "__main__":
    main()
