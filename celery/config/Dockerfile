FROM mcr.microsoft.com/playwright/python:v1.52.0


# Set work directory
WORKDIR /app

# Copy your requirements
COPY ./config/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . .

# Optional: install only Firefox (skip chromium/webkit if not needed)
RUN playwright install firefox