import json
from pymongo import MongoClient

def insert_json_data(json_file_path, db_name, collection_name, batch_size=1000):
    """
    Inserts data from a JSON file into a specified MongoDB collection in batches.

    Parameters:
    - json_file_path: Path to the JSON file containing the data.
    - db_name: Name of the database.
    - collection_name: Name of the collection.
    - batch_size: Number of documents to insert per batch.
    """
    # Establish a connection to the MongoDB server
    client = MongoClient('mongodb://localhost:27017/')
    db = client[db_name]
    collection = db[collection_name]

    try:
        # Open and read the JSON file
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            # Ensure data is a list of documents
            if isinstance(data, list):
                total_documents = len(data)
                print(f"Total documents to insert: {total_documents}")

                for i in range(0, total_documents, batch_size):
                    batch = data[i:i + batch_size]
                    collection.insert_many(batch)
                    print(f"Inserted documents {i + 1} to {i + len(batch)}")
            else:
                print("The JSON file does not contain a list of documents.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    # Specify the path to your JSON file
    json_file_path = './data.json'
    # Define the database and collection names
    db_name = 'hashfilmcs'
    collection_name = 'complaints'
    # Call the function to insert data
    insert_json_data(json_file_path, db_name, collection_name)
