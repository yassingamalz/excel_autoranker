FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pyqt5 \
    python3-pyqt5.qtsvg \
    libgl1-mesa-glx \
    libxcb-xinerama0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-xfixes0 \
    libxkbcommon-x11-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make sure the package is in the Python path
ENV PYTHONPATH=/app

# Set QT Platform to minimize display issues
ENV QT_QPA_PLATFORM=xcb
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:0

CMD ["python", "-m", "src.gui.main_window"]