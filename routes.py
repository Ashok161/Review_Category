# Import necessary modules from Flask and other libraries
from flask import Flask, request, render_template
from database import session, Review  # Import database session and Review model
from scraper import fetch_reviews  # Import the function to fetch reviews from an external source
from apscheduler.schedulers.background import BackgroundScheduler  # Import BackgroundScheduler for scheduling tasks

# Initialize a Flask application
app = Flask(__name__)

# Initialize the BackgroundScheduler to run tasks in the background
scheduler = BackgroundScheduler()
# Schedule the fetch_reviews function to run every 24 hours
scheduler.add_job(func=fetch_reviews, trigger="interval", hours=24)
# Start the scheduler to begin executing scheduled jobs
scheduler.start()

# Define the route for the home page
@app.route('/')
def index():
    # Render and return the index.html template for the home page
    return render_template('index.html')

# Define the route to search for reviews based on date and category
@app.route('/search')
def search_reviews():
    # Get 'date' and 'category' parameters from the query string of the request
    date = request.args.get('date')
    category = request.args.get('category')
    # Query the database for reviews that match the provided date and category
    reviews = session.query(Review).filter_by(date=date, category=category).all()
    # Return a JSON-like response containing the review texts and count of reviews found
    return {
        "reviews": [review.text for review in reviews],  # List of review texts
        "count": len(reviews)  # Total count of reviews found
    }

# Define a function to clean up resources when shutting down the app context
@app.teardown_appcontext
def shutdown_scheduler(exception=None):
    # Check if the scheduler is running before attempting to shut it down
    if scheduler.running:
        scheduler.shutdown()  # Shut down the scheduler

# Run the Flask application in debug mode if this script is executed directly
if __name__ == "__main__":
    app.run(debug=True)