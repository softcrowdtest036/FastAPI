# banjos_restaurant\app\core\database.py
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGO_URI, DATABASE_NAME

class MongoDB:
    def __init__(self):
        self.client = None
        self.database = None

    async def connect(self):
        """Initialize MongoDB connection with a connection pool."""
        if self.client is None:  # Prevent multiple connections
            try:
                self.client = AsyncIOMotorClient(
                    MONGO_URI,
                    maxPoolSize=10,
                    minPoolSize=1,
                    serverSelectionTimeoutMS=5000,  # 5 seconds
                    connectTimeoutMS=30000,  # 30 seconds
                    socketTimeoutMS=30000  # 30 seconds
                )
                # Test the connection
                await self.client.server_info()
                self.database = self.client[DATABASE_NAME]
                print("Connected to MongoDB successfully!")
            except Exception as e:
                print(f"Failed to connect to MongoDB: {e}")
                raise RuntimeError("Failed to connect to MongoDB")

    async def close(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            self.client = None
            self.database = None
            print("MongoDB connection closed.")

    def get_database(self):
        """Get the database instance after initialization."""
        if self.database is None:
            raise RuntimeError("Database connection is not initialized. Call 'await mongodb.connect()' at startup.")
        return self.database

# Create a global MongoDB instance
mongodb = MongoDB()