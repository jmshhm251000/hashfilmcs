from pymongo import MongoClient

# Replace this with your actual connection string
CONNECTION_STRING = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority"

# Connect to MongoDB Atlas
client = MongoClient(CONNECTION_STRING)

# Choose or create a database and collection
db = client["CustomerService"]
collection = db["Complaints"]

# Insert a sample complaint
complaint = {
    "customer_name": "John Doe",
    "platform": "WhatsApp",
    "message": "I'm having an issue with my order #12345.",
    "timestamp": "2025-04-03T12:34:00",
    "files": [],  # could be URLs or filenames
    "status": "pending"
}

inserted_id = collection.insert_one(complaint).inserted_id
print(f"Inserted complaint with ID: {inserted_id}")

# Retrieve all complaints
for doc in collection.find():
    print(doc)