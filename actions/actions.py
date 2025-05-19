from typing import Any, Text, Dict, List, Optional
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from urllib.parse import urlencode
import re
import json

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

class ActionSearchRoom(Action):
    def name(self) -> Text:
        return "action_search_room"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        district = next(tracker.get_latest_entity_values("district"), None)
        province = next(tracker.get_latest_entity_values("province"), None)
        street = next(tracker.get_latest_entity_values("street"), None)

        raw_min_price = next(tracker.get_latest_entity_values("minPrice"), None)
        raw_max_price = next(tracker.get_latest_entity_values("maxPrice"), None)

        min_price = convert_price_to_number(raw_min_price)
        max_price = convert_price_to_number(raw_max_price)

        raw_area_range = next(tracker.get_latest_entity_values("areaRange"), None)
        area_range = parse_area_range(raw_area_range)

        # room_type = next(tracker.get_latest_entity_values("roomType"), None)
        amenities = list(tracker.get_latest_entity_values("amenities"))
        environment = next(tracker.get_latest_entity_values("environment"), None)
        target_audience = next(tracker.get_latest_entity_values("targetAudience"), None)
        has_video_review = next(tracker.get_latest_entity_values("has_video_review"), None)

        params = {
            "page": 0,
            "size": 10,
            "sort": "createdAt,desc"
        }

        if street:
            params["street"] = street
        if district:
            params["district"] = district
        if province:
            params["city"] = province
        if min_price:
            params["minPrice"] = min_price
        if max_price:
            params["maxPrice"] = max_price
        if area_range:
            params["areaRange"] = area_range
        # if room_type:
        #     params["roomType"] = room_type.upper()
        if amenities:
            params["amenities"] = amenities
        if environment:
            params["environment"] = environment
        if target_audience:
            params["targetAudience"] = target_audience
        if has_video_review:
            params["hasVideoReview"] = has_video_review

        url = "http://localhost:8222/api/v1/rooms/search"
        query_string = urlencode(params, doseq=True)
        print(f"Requesting API URL: {url}?{query_string}")

        try:
            res = requests.get(url, params=params)
            res.raise_for_status()
            data = res.json()
            rooms = data.get("data", {}).get("content", [])

            if not rooms:
                dispatcher.utter_message(text="Hiện tại chưa có phòng nào phù hợp với yêu cầu của bạn 😢")
            else:
                reply = "✨ Đây là các phòng phù hợp:\n"
            for room in rooms[:10]:
                idRoom = room.get('id')
                title = room.get("title", "Phòng trọ")
                price = room.get("price", 0)
                area = room.get("area", "?")
                imageUrls = room.get("imageUrls", "?")

                address = room.get("address", {}) or {}

                reply += (
                    f"\n ID_Room: {idRoom} – 🏠 {title} – {price:,.0f}đ – {area}m² – {imageUrls}"
                )

            dispatcher.utter_message(text=reply)

        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
            dispatcher.utter_message(text="Có lỗi xảy ra khi gọi API tìm phòng. Vui lòng thử lại sau.")
        except requests.exceptions.ConnectionError as errc:
            print(f"Connection Error: {errc}")
            dispatcher.utter_message(text="Lỗi kết nối API. Vui lòng thử lại sau.")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
            dispatcher.utter_message(text="Lỗi thời gian chờ kết nối API. Vui lòng thử lại sau.")
        except requests.exceptions.RequestException as err:
            print(f"OOps: Something Else: {err}")
            dispatcher.utter_message(text="Đã có lỗi không xác định xảy ra. Vui lòng thử lại sau.")

        return []
