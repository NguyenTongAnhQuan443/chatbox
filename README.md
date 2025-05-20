# Training AI
0) Python Version 3.8.10
1) python -m venv .venv
2) .venv\Scripts\activate
3) pip install rasa
4) rasa train
### -----------------------
# Sau khi train
## Chạy server actions:
0) .venv\Scripts\activate
1) rasa run actions --debug

## Chạy chatbot trên terminal
2) .venv\Scripts\activate
3) rasa shell --debug
### -----------------------
# BỎ QUA PHẦN NÀY
## Sinh data bằng CHATITO
0) npm install -g chatito
1) chatito searchRoom.chatito --format rasa --output ./nlu 
## Ở trên là sinh dữ liệu
# Convert JSON sang yml để train 
0) python convert_to_yaml.py
### -------------------------------------------------------
# REST API CHAT BOX - BẮT ĐẦU TỪ ĐÂY
0) pip install fastapi uvicorn
1) pip install requests
2) Chạy server actions:
    .venv\Scripts\activate
    rasa run actions --debug
3) Chạy API: 
    .venv\Scripts\activate
    rasa run --enable-api --cors "*" --debug



