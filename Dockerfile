FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pyqt5 \
    libgl1-mesa-glx \
    python3-pyqt5.qtsvg \
    qt5-default \
    libx11-xcb1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make sure the package is in the Python path
ENV PYTHONPATH=/app

# Default QT Platform
ENV QT_QPA_PLATFORM=xcb

CMD ["python", "-m", "src.gui.main_window"]