# Play Store Review Scraper

This project scrapes Google Play Store reviews for a specific game, categorizes them, and provides an interface for querying by date and category.

## Setup Instructions

### Local Setup

1. **Clone the Repository**:
    ```bash
    git clone <repository-url>
    cd PlayStoreReviewScraper
    ```

2. **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # For macOS/Linux
    venv\Scripts\activate     # For Windows
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up PostgreSQL**:
   - Ensure PostgreSQL is running.
   - Create a database of your choice .
   - Update the `SQLALCHEMY_DATABASE_URL` in `database.py` with your credentials.

5. **Run the Application**:
    ```bash
    python routes.py
    ```

6. **Access the Application**:
   - Open `http://127.0.0.1:5000/` in your browser.

### Docker Setup

1. **Build the Docker Image**:
    ```bash
    docker build -t playstore_review_scraper .
    ```

2. **Run the Docker Container**:
    ```bash
    docker run -p 5000:5000 playstore_review_scraper
    ```

3. **Access the Application**:
   - Open `http://127.0.0.1:5000/` in your browser.

## API Example

Sample API request:
```http
GET /search?date=2024-11-04&category=Bugs
