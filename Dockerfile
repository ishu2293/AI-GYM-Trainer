FROM python:3.10-slim

# Install system dependencies for MediaPipe, OpenCV, and WebRTC
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Render dynamically assigns a port via the $PORT variable
ENV PORT=8501
EXPOSE $PORT

# Start Streamlit bound to 0.0.0.0 and Render's dynamic $PORT
CMD streamlit run main.py --server.port $PORT --server.address 0.0.0.0