from fastapi import FastAPI, Query
from typing import List, Optional
import requests
import re
from urllib.parse import urlencode

app = FastAPI()

def convert_price_to_number(price_str: Optional[str]) -> Optional[int]:
    if not price_str:
        return None
    price_str = price_str.lower().replace(",", "").strip()
    match = re.search(r"(\d+(?:\.\d+)?)(\s*(tr|triệu|t|trieu)?)", price_str)
    if match:
        number = float(match.group(1))
        return int(number * 1_000_000)
    elif price_str.isdigit():
        return int(price_str)
    return None

def normalize_area_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^ \w\s]", "", text)
    text = re.sub(r"m(?:\s*et)?\s*(vuong|v|2)", "m2", text)
    text = re.sub(r"met\s*(vuong|v|2)", "m2", text)
    text = re.sub(r"\s+", "", text)
    return text

def parse_area_range(area_str: Optional[str]) -> Optional[str]:
    if not area_str:
        return None
    area_str = normalize_area_text(area_str)
    if '-' in area_str:
        parts = area_str.split('-')
        try:
            low = int(re.findall(r'\d+', parts[0])[0])
            high = int(re.findall(r'\d+', parts[1])[0])
            return f"{low}-{high}"
        except:
            return None
    match = re.match(r"^(\d+)(m2)?$", area_str)
    if match:
        value = int(match.group(1))
        lower = max(0, value - 10)
        upper = value + 10
        return f"{lower}-{upper}"
    return None

@app.post("/search-room")
def search_room(
    district: Optional[str] = None,
    province: Optional[str] = None,
    street: Optional[str] = None,
    minPrice: Optional[str] = None,
    maxPrice: Optional[str] = None,
    areaRange: Optional[str] = None,
    amenities: Optional[List[str]] = Query(None),
    environment: Optional[str] = None,
    targetAudience: Optional[str] = None,
    hasVideoReview: Optional[bool] = None
):
    min_price = convert_price_to_number(minPrice)
    max_price = convert_price_to_number(maxPrice)
    area_range = parse_area_range(areaRange)

    params = {
        "page": 0,
        "size": 10,
        "sort": "createdAt,desc"
    }
    if street: params["street"] = street
    if district: params["district"] = district
    if province: params["city"] = province
    if min_price: params["minPrice"] = min_price
    if max_price: params["maxPrice"] = max_price
    if area_range: params["areaRange"] = area_range
    if amenities: params["amenities"] = amenities
    if environment: params["environment"] = environment
    if targetAudience: params["targetAudience"] = targetAudience
    if hasVideoReview is not None: params["hasVideoReview"] = hasVideoReview

    try:
        url = "http://localhost:8222/api/v1/rooms/search"
        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()
        rooms = data.get("data", {}).get("content", [])
        if not rooms:
            return {"message": "Không tìm thấy phòng phù hợp"}
        results = []
        for room in rooms[:10]:
            results.append({
                "id": room.get("id"),
                "title": room.get("title"),
                "price": room.get("price"),
                "area": room.get("area"),
                "address": room.get("address"),
                "images": room.get("imageUrls")
            })
        return {"results": results}
    except requests.RequestException as e:
        return {"error": str(e)}
