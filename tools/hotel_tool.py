import os
import requests
from dotenv import load_dotenv

load_dotenv()

AMADEUS_API_KEY = os.getenv("AMADEUS_API_KEY")
AMADEUS_API_SECRET = os.getenv("AMADEUS_API_SECRET")

TOKEN_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
HOTEL_LIST_URL = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city"
HOTEL_OFFERS_URL = "https://test.api.amadeus.com/v3/shopping/hotel-offers"

_cached_token = None


def _get_access_token():
    """Amadeus uses OAuth2 client-credentials flow. Token is short-lived."""
    global _cached_token

    response = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": AMADEUS_API_KEY,
            "client_secret": AMADEUS_API_SECRET,
        },
    )
    response.raise_for_status()
    _cached_token = response.json()["access_token"]
    return _cached_token


def search_hotels(city_code: str, check_in: str, check_out: str, adults: int = 1) -> str:
    """
    Search real hotel offers for a city.

    Args:
        city_code: IATA city code, e.g. "PAR" (Paris), "DXB" (Dubai), "BKK" (Bangkok).
                    NOT the same as an airport code in every case -- check
                    https://developers.amadeus.com/self-service/category/hotels
        check_in:  "YYYY-MM-DD"
        check_out: "YYYY-MM-DD"
        adults:    number of adults per room

    Returns a human-readable string summary (so it can be dropped straight
    into an LLM prompt, same pattern as the other tools in this project).
    """
    if not AMADEUS_API_KEY or not AMADEUS_API_SECRET:
        return "Hotel search unavailable: AMADEUS_API_KEY / AMADEUS_API_SECRET not set in .env"

    try:
        token = _get_access_token()
        headers = {"Authorization": f"Bearer {token}"}

        # Step 1: get hotel IDs in the city
        hotel_list_resp = requests.get(
            HOTEL_LIST_URL,
            headers=headers,
            params={"cityCode": city_code},
        )
        hotel_list_resp.raise_for_status()
        hotels = hotel_list_resp.json().get("data", [])[:10]

        if not hotels:
            return f"No hotels found for city code '{city_code}'."

        hotel_ids = [h["hotelId"] for h in hotels]

        # Step 2: get live offers (price/availability) for those hotel IDs
        offers_resp = requests.get(
            HOTEL_OFFERS_URL,
            headers=headers,
            params={
                "hotelIds": ",".join(hotel_ids),
                "checkInDate": check_in,
                "checkOutDate": check_out,
                "adults": adults,
            },
        )
        offers_resp.raise_for_status()
        offers_data = offers_resp.json().get("data", [])

        if not offers_data:
            return f"No live offers found for hotels in '{city_code}' for those dates."

        results = []
        for item in offers_data[:5]:
            hotel_name = item.get("hotel", {}).get("name", "Unknown Hotel")
            offer = item.get("offers", [{}])[0]
            price = offer.get("price", {}).get("total", "N/A")
            currency = offer.get("price", {}).get("currency", "")
            room_type = offer.get("room", {}).get("typeEstimated", {}).get("category", "N/A")

            results.append(
                f"Hotel: {hotel_name}\n"
                f"Room: {room_type}\n"
                f"Price: {price} {currency} (total stay)\n"
            )

        return "\n".join(results)

    except requests.exceptions.RequestException as e:
        return f"Hotel search failed: {e}"
