# - 1
FROM rasa/rasa:3.6.10-full

# Copy project files
COPY . /app
WORKDIR /app

# Expose Rasa port
EXPOSE 5005

# Default command
CMD ["run", "--enable-api", "--cors", "*", "--debug"]
