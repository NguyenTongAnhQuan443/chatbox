import json
import re

# Đọc dữ liệu JSON
with open("rasa_dataset_training.json", "r", encoding="utf-8") as file:
    data = json.load(file)

examples = data.get("rasa_nlu_data", {}).get("common_examples", [])

# Các từ khóa có thể là địa danh (district)
district_patterns = r"(Quận\s+\w+(?:\s\w+)*|Huyện\s+\w+(?:\s\w+)*|Thành phố\s+\w+(?:\s\w+)*|TP\s+\w+(?:\s\w+)*|Thị xã\s+\w+(?:\s\w+)*|Phường\s+\w+(?:\s\w+)*|Xã\s+\w+(?:\s\w+)*)"


# Danh sách câu đã xử lý
processed_examples = []

for ex in examples:
    text = ex["text"]

    # Gắn entity district
    match_district = re.search(district_patterns, text, flags=re.IGNORECASE)
    if match_district:
        district = match_district.group(1)
        text = text.replace(district, f"[{district}](district)")

    # Gắn entity amenities
    match_amenity = re.search(r"có\s+([^\[\]()]*?)(?:\s+(?:ở|tại|trong|vùng|khu|khu vực|gần)\b|$)", text)
    if match_amenity:
        amenity = match_amenity.group(1).strip()
        text = text.replace(amenity, f"[{amenity}](amenities)")

    processed_examples.append(f"    - {text}")

# Gộp thành YAML chuẩn
yaml_text = "version: \"3.1\"\nnlu:\n- intent: searchRoom\n  examples: |\n" + "\n".join(processed_examples)

# Ghi file YAML
with open("search_room_nlu.yml", "w", encoding="utf-8") as file:
    file.write(yaml_text)

print("🎉 File YAML đã được tạo thành công: search_room_nlu.yml")
