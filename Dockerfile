# - 1
FROM rasa/rasa:3.7.0-full

# Copy project files
COPY . /app
WORKDIR /app

# Expose Rasa port
EXPOSE 5005

# Default command
CMD ["run", "--enable-api", "--cors", "*", "--debug"]
