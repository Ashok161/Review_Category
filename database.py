# Import necessary modules from SQLAlchemy for database interaction
from sqlalchemy import create_engine, Column, String, Integer, Date  # Import SQLAlchemy components for defining models and creating an engine
from sqlalchemy.ext.declarative import declarative_base  # Import declarative_base for model definition
from sqlalchemy.orm import sessionmaker  # Import sessionmaker to create session objects

# PostgreSQL Database URL (replace with your actual credentials)
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Arjun%40123@localhost/ashok"  # Define the database connection URL

# Create the PostgreSQL engine using the provided database URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)  # Create an engine that connects to the PostgreSQL database
Base = declarative_base()  # Create a base class for declarative model definitions
Session = sessionmaker(bind=engine)  # Create a session factory bound to the engine
session = Session()  # Create a new session instance

# Define the Review model class which maps to the 'reviews' table in the database
class Review(Base):
    __tablename__ = 'reviews'  # Specify the name of the table in the database
    id = Column(Integer, primary_key=True, index=True)  # Define an 'id' column as primary key with indexing
    text = Column(String)  # Define a 'text' column to store review content as a string
    date = Column(Date)  # Define a 'date' column to store review date
    category = Column(String)  # Define a 'category' column to store review category as a string

# Create all tables in the database defined by the Base's subclasses (in this case, just the Review table)
Base.metadata.create_all(engine)  # This creates the 'reviews' table if it doesn't exist

# Function to save a review to the database
def save_review_to_db(review_data):
    # Create an instance of Review using data from review_data dictionary
    review = Review(text=review_data['text'], date=review_data['date'], category=review_data['category'])
    session.add(review)  # Add the review instance to the current session
    session.commit()  # Commit the current session to save changes to the database
    print(f"Review saved to database: {review_data}")  # Print confirmation that the review has been saved