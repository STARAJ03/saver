FROM python:3.10.4-slim-buster

# Install system dependencies
RUN apt update && apt install -y \
    git curl ffmpeg wget bash neofetch \
    software-properties-common python3-pip \
    && apt clean

# Set the working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -U pip wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port used by Flask
EXPOSE 5000

# Run your Python app (Flask + asyncio) as the main process
CMD ["python3", "main.py"]
