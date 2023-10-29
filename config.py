import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Get credentials from environment variables
        # self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        # self.API_KEY = os.getenv("API_KEY")
        self.MONGO_URL=os.getenv("MONGO_URL")
