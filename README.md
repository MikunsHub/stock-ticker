# Stock Ticker

Welcome to the Stock Ticker API, a Flask-based RESTful API that provides users with access to stock data and watchlist management features. This API enables developers to build applications that require real-time stock data and watchlist functionality.

## Features

1. Calculate Adjusted Close Data: Allows users to calculate adjusted close data for a given stock symbol.
2. Get Watchlist Cursors: Returns a list of watchlist cursors (tickers) stored in the database.
3. Search for Stock Ticker: Searches for stock tickers using the Alpha Vantage API and caches results for faster retrieval.
4. Watchlist Management: Enables users to manage their watchlist by adding them to mongodb
5. Real-time Data: Provides real-time stock data and adjusted close data calculations.
6. Validation and Serialization: Includes validation and serialization using Pydantic models for robust data handling and error handling.


## Prerequisites

- Python 3.11
- Docker
- AlphaVantage API Key
- EODHD API Key

## Local Installation

1. Clone this repository to your local machine.
   
   ```bash
   git clone https://github.com/MikunsHub/stock-ticker.git
   ```

2. Create a virtual environment and install the required dependencies..
   
   ```bash
   pipenv install
   ```


3. Create a `.env` file in the project directory and fill in the required API Keys.

   ```ini
    ALPHA_VANTAGE_API_KEY=
    ALPHA_VANTAGE_BASE_URL=https://www.alphavantage.co
    MONGO_USER=test_user
    MONGO_HOST=localhost
    MONGO_PASSWORD=test_pwd
    EODHD_API_TOKEN=
    EODHD_BASE_URL=https://eodhd.com
   ```

4. Run the application.
   
   ```bash
   make docker-run
   make run-local
   ```

## Contributing

Contributions are welcome! Feel free to open issues, submit pull requests, or suggest improvements.



