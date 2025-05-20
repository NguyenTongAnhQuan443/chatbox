# - 1
FROM rasa/rasa-sdk:3.5.6

# Copy project files
COPY . /app
WORKDIR /app

# Expose Rasa port
EXPOSE 5005

# Default command
CMD ["run", "--enable-api", "--cors", "*", "--debug"]
