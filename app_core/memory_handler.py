# ═══ IMPORTS ═══
import os
from dotenv import load_dotenv
from mem0 import MemoryClient, Memory

# ═══ MEMORY HANDLER CLASS — Wraps Mem0 for storing & retrieving user memories ═══
class MemoryHandler:

    # ── CONSTRUCTOR: Decides between Cloud (Mem0 Platform) or Local (SQLite) storage ──
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Look for MEM0_API_KEY or mem0_api in .env/environment
        self.api_key = os.environ.get("MEM0_API_KEY") or os.environ.get("mem0_api")
        
        # Decide if using Mem0 Platform Client or Local open-source Memory
        if self.api_key and self.api_key.startswith("m0-"):
            print("Initializing Mem0 Platform Client...")
            self.client = MemoryClient(api_key=self.api_key)
            self.use_platform = True
        else:
            print("Initializing Mem0 Local Client (Open Source)...")
            # Local client uses SQLite/Qdrant under the hood
            # By default it stores files locally in ~/.mem0/
            self.client = Memory()
            self.use_platform = False

    # ── ADD MEMORY: Sends text to Mem0 which auto-extracts facts about the user ──
    def add_memory(self, text: str, user_id: str = "default_user", metadata: dict = None) -> bool:
        """
        Extract and store persistent memories from the interaction text.
        """
        try:
            if not text.strip():
                return False
            
            # Both OSS and Platform clients accept user_id in add()
            self.client.add(text, user_id=user_id, metadata=metadata)
            return True
        except Exception as e:
            print(f"Error adding memory: {e}")
            return False

    # ── GET MEMORIES: Semantic search — finds relevant past memories for a query ──
    def get_memories(self, query: str, user_id: str = "default_user") -> list[str]:
        """
        Retrieve relevant memories matching the query context.
        Returns a list of clean memory facts as strings.
        """
        try:
            if not query.strip():
                return []
                
            if self.use_platform:
                # Platform API requires filters dictionary for search
                results = self.client.search(query, filters={"user_id": user_id})
                memories = []
                # Handle results depending on list or dictionary structure
                # The response structure from search usually contains a list of matches
                raw_list = []
                if isinstance(results, dict) and "results" in results:
                    raw_list = results["results"]
                elif isinstance(results, list):
                    raw_list = results
                
                for item in raw_list:
                    if isinstance(item, dict) and "memory" in item:
                        memories.append(item["memory"])
                    elif hasattr(item, "memory"):
                        memories.append(item.memory)
                return memories
            else:
                # Local client search returns details
                results = self.client.search(query, user_id=user_id)
                memories = []
                for item in results:
                    if isinstance(item, dict) and "memory" in item:
                        memories.append(item["memory"])
                    elif hasattr(item, "memory"):
                        memories.append(item.memory)
                return memories
        except Exception as e:
            print(f"Error retrieving memories: {e}")
            return []

    # ── GET ALL MEMORIES: Returns every stored fact for a user ──
    def get_all_memories(self, user_id: str = "default_user") -> list[dict]:
        """
        Retrieves all currently stored facts about the user.
        Format returned: list of dicts containing 'id' and 'memory'.
        """
        try:
            if self.use_platform:
                # Platform API requires filters dictionary for get_all
                results = self.client.get_all(filters={"user_id": user_id})
                raw_list = []
                if isinstance(results, dict):
                    raw_list = results.get("results") or results.get("memories") or []
                elif isinstance(results, list):
                    raw_list = results
                
                memories = []
                for item in raw_list:
                    if isinstance(item, dict):
                        memories.append({
                            "id": item.get("id"),
                            "memory": item.get("memory")
                        })
                return memories
            else:
                # Local open source client lists memories
                results = self.client.get_all(user_id=user_id)
                memories = []
                if isinstance(results, list):
                    for item in results:
                        if isinstance(item, dict):
                            memories.append({
                                "id": item.get("id"),
                                "memory": item.get("memory")
                            })
                return memories
        except Exception as e:
            print(f"Error listing all memories: {e}")
            return []

    # ── DELETE MEMORY: Removes one specific memory by its ID ──
    def delete_memory(self, memory_id: str) -> bool:
        """
        Deletes a specific memory by its ID.
        """
        try:
            self.client.delete(memory_id)
            return True
        except Exception as e:
            print(f"Error deleting memory {memory_id}: {e}")
            return False

    # ── CLEAR ALL: Wipes every memory for a given user ──
    def clear_all(self, user_id: str = "default_user") -> bool:
        """
        Deletes all memories for a specific user.
        """
        try:
            # delete_all takes user_id directly on Platform client
            self.client.delete_all(user_id=user_id)
            return True
        except Exception as e:
            print(f"Error clearing memory for user {user_id}: {e}")
            return False
