# Use a lightweight Python image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    espeak \
    build-essential \
    libasound2-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose ports for FastAPI and Streamlit
EXPOSE 8000
EXPOSE 8501

# Start FastAPI and Streamlit
CMD ["bash", "-c", "\
uvicorn orchestrator.main:app --host 0.0.0.0 --port 8000 & \
streamlit run streamlit_app/app.py --server.port=8501 --server.enableCORS false \
"]