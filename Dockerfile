FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    wget \
    curl \
    unzip \
    fonts-liberation \
    libnss3 \
    libx11-6 \
    libx11-xcb1 \
    libxcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \

ENV CHROME_BIN=/usr/bin/chromium
ENV CHROME_DRIVER=/usr/bin/chromedriver
ENV DISPLAY=:99
RUN chromium --version
RUN chromedriver --version

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY check_iphone_availability.py .
RUN chmod +x /usr/bin/chromedriver
CMD ["python", "check_iphone_availability.py"]
