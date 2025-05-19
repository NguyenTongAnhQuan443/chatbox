FROM python:3.10-slim

# Tạo thư mục app
WORKDIR /app

# Copy toàn bộ code vào image
COPY . .

# Cài pip và các thư viện
RUN pip install --upgrade pip
RUN pip install rasa[full] requests

# Mở cổng mặc định
EXPOSE 5005

# Lệnh để start chatbot
CMD ["rasa", "run", "--enable-api", "--cors", "*", "--debug"]
