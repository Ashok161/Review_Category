# Import necessary modules for logging, Google Play reviews scraping, date manipulation, and database operations
import logging
from google_play_scraper import Sort, reviews  # Import Sort and reviews functions from the google_play_scraper library
from datetime import datetime, timedelta  # Import datetime and timedelta for date calculations
from database import save_review_to_db  # Import function to save reviews to the database

# Set up logging configuration to display INFO level messages and above
logging.basicConfig(level=logging.INFO)

# Define keywords for categorizing reviews into different categories
KEYWORDS = {
    'Bugs': ['bug', 'glitch', 'issue', 'problem', 'fix', 'stuck', 'loading', 'broken', 'unresponsive', 'freeze',
             'lag', 'delay', 'disconnect', 'error', 'server', 'hang', 'timeout', 'retry', 'unusable', 'defect'],
    'Complaints': ['dislike', 'hate', 'annoyed', 'upset', 'not satisfied', 'frustrated', 'worst', 'boring', 
                   'expensive', 'waste', 'bad experience', 'bad quality', 'negative', 'feedback', 
                   'disappointing', 'annoyance', 'irritated', 'confusing', 'complicated', 'downgrade'],
    'Crashes': ['crash', 'crashes', 'crashing', 'quit', 'exit', 'shutdown', 'close', 
                'restart', 'unexpected stop',  'reboot','terminated','freeze','hang','broken','malfunction',
                'fatal error','black screen','blank screen','shut down','deadlock'],
    'Praises': ['love','great','excellent','awesome','amazing','fun','enjoyable','best',
                'beautiful','fantastic','high quality','well made','recommend','happy',
                'satisfied','pleasant','impressive','user friendly','smooth','perfect'],
    # An empty list for any other categories not defined
    'Other': []
}

# Function to fetch reviews from Google Play Store for a specific app
def fetch_reviews(app_id="com.superplaystudios.dicedreams", max_reviews=1000):
    # Calculate the date for seven days ago from the current date
    seven_days_ago = datetime.now() - timedelta(days=7)
    continuation_token = None  # Initialize continuation token for paginated results
    total_reviews_fetched = 0  # Counter for total reviews fetched

    while total_reviews_fetched < max_reviews:  # Loop until the maximum number of reviews is fetched
        logging.info(f"Fetching reviews with continuation_token: {continuation_token}")
        
        # Try to fetch reviews using google-play-scraper
        try:
            result, continuation_token = reviews(
                app_id,
                lang="en",  # Set language to English
                country="us",  # Set country to US
                sort=Sort.NEWEST,  # Sort reviews by newest first
                count=200,  # Fetch up to 200 reviews at a time
                continuation_token=continuation_token  # Use continuation token for pagination
            )
        except Exception as e:
            logging.error(f"Error fetching reviews: {e}")  # Log any errors encountered during fetching
            break

        logging.info(f"Fetched {len(result)} reviews.")  # Log the number of reviews fetched
        
        for review in result:  # Iterate through each fetched review
            review_date = review['at'].date()  # Extract the review date
            if review_date < seven_days_ago.date():  # Check if the review is older than seven days
                logging.info("Reached reviews older than 7 days; stopping.")
                return  # Stop fetching if older than seven days

            # Prepare review data for saving to the database
            review_data = {
                'text': review['content'],  # Review content text
                'date': review_date,  # Review date
                # Categorize the review based on its content using categorize_review function
                'category': categorize_review(review['content'])
            }
            logging.info(f"Saving review: {review_data}")  # Log the review data being saved
            save_review_to_db(review_data)  # Save the review data to the database

        total_reviews_fetched += len(result)  # Update total count of fetched reviews
        logging.info(f"Total reviews fetched so far: {total_reviews_fetched}")  # Log total fetched so far

        if not continuation_token:  # Check if there are more reviews to fetch
            logging.info("No more reviews to fetch.")
            break

# Function to categorize a given review text based on predefined keywords
def categorize_review(text):
    text = text.lower()  # Convert text to lowercase for case-insensitive matching
    for category, keywords in KEYWORDS.items():  # Iterate through each category and its keywords
        if any(keyword in text for keyword in keywords):  # Check if any keyword exists in the review text
            return category  # Return the matched category name
    return 'Other'  # Return "Other" if no keywords match

# Main execution block to run fetch_reviews function when script is executed directly
if __name__ == "__main__":
    import logging  # Re-import logging (not necessary here since it's already imported)
    logging.basicConfig(level=logging.INFO)  # Set up logging again (not necessary)
    fetch_reviews()  # Call fetch_reviews function to start fetching reviews