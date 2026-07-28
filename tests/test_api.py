import os
import inspect
from dotenv import load_dotenv
from mem0 import MemoryClient

load_dotenv()
api_key = os.environ.get("MEM0_API_KEY") or os.environ.get("mem0_api")
client = MemoryClient(api_key=api_key)

print("get_all signature:", inspect.signature(client.get_all))
print("delete_all signature:", inspect.signature(client.delete_all))
print("delete signature:", inspect.signature(client.delete))
print("add signature:", inspect.signature(client.add))
print("search signature:", inspect.signature(client.search))
