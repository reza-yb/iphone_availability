# iPhone Availability Checker

A Dockerized Python application that monitors the availability of specific iPhone models on Apple's reservation website and sends real-time notifications via Telegram. This tool leverages Selenium for web automation and the Telegram Bot API for notifications.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Configure Environment Variables](#2-configure-environment-variables)
  - [3. Build and Run with Docker Compose](#3-build-and-run-with-docker-compose)
- [Configuration](#configuration)
  - [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Security Considerations](#security-considerations)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Automated Availability Checks**: Continuously monitors Apple's reservation page for the specified iPhone model, color, and capacity.
- **Real-Time Notifications**: Sends instant Telegram messages when the desired iPhone configuration becomes available.
- **Dockerized Deployment**: Easily deployable using Docker and Docker Compose for consistent environments.
- **Configurable Parameters**: Customize the iPhone model, color, capacity, Telegram tokens, and chat IDs via environment variables.

## Prerequisites

Before setting up the iPhone Availability Checker, ensure you have the following installed on your system:

- **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)
- **Telegram Bot**: Create a Telegram bot and obtain the Bot Token. Instructions can be found [here](https://core.telegram.org/bots#6-botfather).

## Project Structure

```
iphone-availability-checker/
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── requirements.txt
├── check_iphone_availability.py
└── README.md
```

- **Dockerfile**: Defines the Docker image configuration.
- **docker-compose.yml**: Configures Docker services and environment variables.
- **.env.example**: Example environment variables file. Rename to `.env` and fill in your values.
- **requirements.txt**: Python dependencies.
- **check_iphone_availability.py**: The main Python script that performs the availability checks and sends Telegram notifications.
- **README.md**: Documentation for the project.

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/iphone-availability-checker.git
cd iphone-availability-checker
```

### 2. Configure Environment Variables

1. **Create a `.env` File**:

   Copy the `.env.example` file to `.env`:

   ```bash
   cp .env.example .env
   ```

2. **Edit the `.env` File**:

   Open the `.env` file in your preferred text editor and fill in the required values.

   ```env
   # Telegram Configuration
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   TELEGRAM_AVAILABILITY_CHAT_ID=your_availability_chat_id_here
   TELEGRAM_DEBUG_CHAT_ID=your_debug_chat_id_here

   # iPhone Reservation Configuration
   RESERVATION_URL=https://reserve-prime.apple.com/AE/en_AE/reserve/A/availability?&iUP=N
   MODEL_NAME=iPhone 16 Pro
   COLOR_NAME=Natural Titanium
   CAPACITY_NAME=512GB
   ```

   - **TELEGRAM_BOT_TOKEN**: Your Telegram bot's API token.
   - **TELEGRAM_AVAILABILITY_CHAT_ID**: Chat ID for availability alerts.
   - **TELEGRAM_DEBUG_CHAT_ID**: Chat ID for debug and error messages.
   - **RESERVATION_URL**: URL to check for iPhone availability.
   - **MODEL_NAME**: Desired iPhone model (e.g., `iPhone 16 Pro`).
   - **COLOR_NAME**: Desired color variant (e.g., `Natural Titanium`).
   - **CAPACITY_NAME**: Desired storage capacity (e.g., `512GB`).

### 3. Build and Run with Docker Compose

1. **Build the Docker Image**:

   ```bash
   docker-compose build
   ```

2. **Run the Docker Container**:

   ```bash
   docker-compose up -d
   ```

   - **`-d`**: Runs the container in detached mode.

3. **Verify the Container is Running**:

   ```bash
   docker-compose ps
   ```

   You should see `iphone_checker` service up and running.

## Configuration

### Environment Variables

All configurations are managed via environment variables defined in the `.env` file. Ensure that you have correctly set all required variables before running the Docker container.

#### `.env` Variables Explained

```env
# Telegram Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_AVAILABILITY_CHAT_ID=your_availability_chat_id_here
TELEGRAM_DEBUG_CHAT_ID=your_debug_chat_id_here

# iPhone Reservation Configuration
RESERVATION_URL=https://reserve-prime.apple.com/AE/en_AE/reserve/A/availability?&iUP=N
MODEL_NAME=iPhone 16 Pro
COLOR_NAME=Natural Titanium
CAPACITY_NAME=512GB
```

- **TELEGRAM_BOT_TOKEN**: Obtain this from [BotFather](https://t.me/BotFather) on Telegram.
- **TELEGRAM_AVAILABILITY_CHAT_ID**: The chat ID where availability alerts will be sent.
- **TELEGRAM_DEBUG_CHAT_ID**: The chat ID for debug and error messages.
- **RESERVATION_URL**: The URL to monitor for iPhone availability.
- **MODEL_NAME**: The specific iPhone model to check (e.g., `iPhone 16 Pro`).
- **COLOR_NAME**: The color variant of the iPhone (e.g., `Natural Titanium`).
- **CAPACITY_NAME**: The storage capacity of the iPhone (e.g., `512GB`).

## Usage

Once the Docker container is running, the script will automatically start checking the availability of the specified iPhone configuration every 60 seconds. Notifications will be sent to the configured Telegram chat IDs based on the availability status.

### Logs

To view the logs of the running container:

```bash
docker-compose logs -f
```

This will display real-time logs, including messages about availability checks and Telegram notifications.

### Stopping the Container

To stop the Docker container, run:

```bash
docker-compose down
```

This command stops and removes the containers defined in your `docker-compose.yml`.

## Security Considerations

- **Protect Sensitive Data**: Ensure that your `.env` file is **never** committed to version control systems like Git. The provided `.gitignore` includes `.env` to prevent accidental commits.

  ```gitignore
  # .gitignore

  .env
  ```

- **Use Strong Telegram Tokens**: Keep your Telegram Bot Token secure. Do not share it publicly or expose it in logs.

- **Limit Chat IDs**: Only grant your bot access to necessary chat IDs to minimize exposure.

## Troubleshooting

### Common Issues

1. **Chromium or ChromeDriver Compatibility**:
   - **Issue**: Incompatible versions of Chromium and ChromeDriver can cause Selenium to fail.
   - **Solution**: Ensure that the versions of Chromium and ChromeDriver installed in the Docker container are compatible. You can specify specific versions in the `Dockerfile` if necessary.

2. **Telegram Message Failures**:
   - **Issue**: Messages are not being sent to Telegram.
   - **Solution**:
     - Verify that the `TELEGRAM_BOT_TOKEN` is correct.
     - Ensure that the bot has permission to send messages to the specified chat IDs.
     - Check network connectivity from within the Docker container.

3. **Script Crashes or Exceptions**:
   - **Issue**: The Python script encounters errors and stops.
   - **Solution**:
     - Inspect the logs using `docker-compose logs -f` to identify the error.
     - Ensure that all environment variables are correctly set.
     - Check the reservation URL and XPaths in the script for any changes on the Apple reservation page.

4. **High Resource Usage**:
   - **Issue**: The Docker container consumes excessive CPU or memory.
   - **Solution**:
     - Adjust the `time.sleep` interval in the script to reduce the frequency of checks.
     - Monitor the container's resource usage and optimize the script if necessary.

### Viewing Logs

Use Docker Compose to view logs and identify issues:

```bash
docker-compose logs -f
```

Look for error messages or stack traces that can help diagnose problems.

## Contributing

Contributions are welcome! If you'd like to contribute to the iPhone Availability Checker, please follow these steps:

1. **Fork the Repository**:

   Click the "Fork" button at the top right of the repository page.

2. **Clone Your Fork**:

   ```bash
   git clone https://github.com/yourusername/iphone-availability-checker.git
   cd iphone-availability-checker
   ```

3. **Create a New Branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**:

   Implement your feature or bug fix.

5. **Commit Your Changes**:

   ```bash
   git commit -m "Add feature: your feature description"
   ```

6. **Push to Your Fork**:

   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**:

   Go to the original repository and create a pull request from your fork.

## License

This project is licensed under the [MIT License](LICENSE).

---

*Disclaimer: This project is intended for personal use to monitor iPhone availability. Ensure compliance with Apple's terms of service and avoid excessive or abusive requests to their servers.*