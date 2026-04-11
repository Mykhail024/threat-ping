import requests
from providers.base import Location

def resolve_location(region: str) -> Location:
    response = requests.get(
        "https://nominatim.openstreetmap.org/search",
        params={"q": region, "format": "json", "limit": 1, "addressdetails": 1},
        headers={"User-Agent": "threat-ping"},
    )
    data = response.json()
    if not data:
        raise ValueError(f"Could not resolve location: {region}")

    result = data[0]
    address = result.get("address", {})

    return Location(
        region=result["name"],
        country=address.get("country_code", "").upper(),
        lat=float(result["lat"]),
        lon=float(result["lon"]),
        display_name=result["display_name"],
    )
