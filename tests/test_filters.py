import os
from dotenv import load_dotenv
from mem0 import MemoryClient

load_dotenv()
api_key = os.environ.get("MEM0_API_KEY") or os.environ.get("mem0_api")
client = MemoryClient(api_key=api_key)

user_id = "test_user_filter"

print("--- Testing Add ---")
try:
    res = client.add("I like green tea", user_id=user_id)
    print("Add Response:", res)
except Exception as e:
    print("Add failed:", e)

print("\n--- Testing Search ---")
try:
    res = client.search("What tea do I like?", filters={"user_id": user_id})
    print("Search Response:", res)
except Exception as e:
    print("Search failed:", e)

print("\n--- Testing Get All (with filters={'user_id': ...}) ---")
try:
    res = client.get_all(filters={"user_id": user_id})
    print("Get All (filters) Response:", res)
except Exception as e:
    print("Get All (filters) failed:", e)

print("\n--- Testing Delete All (with user_id directly) ---")
try:
    res = client.delete_all(user_id=user_id)
    print("Delete All (user_id) Response:", res)
except Exception as e:
    print("Delete All (user_id) failed:", e)
