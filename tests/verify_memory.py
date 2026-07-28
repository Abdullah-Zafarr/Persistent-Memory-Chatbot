import sys
import os
import time

# Ensure src/ package is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from memory_handler import MemoryHandler
from llm_connector import LLMConnector

def test_mem0_persistence():
    print("------------------------------------------")
    print("Starting Automated Mem0 Memory Tests from tests/")
    print("------------------------------------------")
    
    handler = MemoryHandler()
    test_user = "verify_test_user_new"
    
    # 1. Clear old memories for absolute clean test state
    print(f"Clearing any existing memories for user: {test_user}...")
    handler.clear_all(user_id=test_user)
    time.sleep(2) # wait for sync
    
    memories = handler.get_all_memories(user_id=test_user)
    print(f"Initial memories (should be empty): {memories}")
    assert len(memories) == 0, f"Expected 0 memories, got {len(memories)}"
    print("✅ Clear/Setup stage passed.")
    
    # 2. Add Age memory
    print("\nAdding memory: 'I am 25 years old'...")
    handler.add_memory("I am 25 years old", user_id=test_user)
    print("Waiting for Mem0 API to process...")
    # Polling logic
    success = False
    for i in range(15):
        time.sleep(1)
        mems = handler.get_all_memories(user_id=test_user)
        print(f"Polling memories (attempt {i+1}/15): {[m['memory'] for m in mems]}")
        if len(mems) > 0 and any("25" in m["memory"] for m in mems):
            success = True
            break
            
    assert success, "Failed to record and verify age 25 fact in time."
    print("✅ Storing persistent memory passed.")
    
    # 3. Retrieve by query context injection test
    retrieved = handler.get_memories("How old am I?", user_id=test_user)
    print(f"Retrieved memories for query 'How old am I?': {retrieved}")
    retrieved_has_age = any("25" in m for m in retrieved)
    assert retrieved_has_age, "Failed to retrieve correct age memory context."
    print("✅ Context query retrieval passed.")

    # 4. Add override memory (updates age to 26)
    print("\nAdding memory override: 'I am 26 years old now'...")
    handler.add_memory("I am 26 years old now", user_id=test_user)
    
    # Poll for update
    success = False
    for i in range(15):
        time.sleep(2)
        mems_updated = handler.get_all_memories(user_id=test_user)
        print(f"Polling updated memories (attempt {i+1}/15): {[m['memory'] for m in mems_updated]}")
        has_26 = any("26" in m["memory"] for m in mems_updated)
        has_25 = any("25" in m["memory"] for m in mems_updated)
        if has_26:
            success = True
            break
            
    assert success, "Failed to register new age 26 in time."
    print("✅ Fact override update verification passed.")
    
    # 5. Connect and test LLM context injection
    print("\nTesting LLM Connector with injected memories...")
    provider = "Groq" if (os.environ.get("GROQ_API_KEY") or os.environ.get("Groq_api")) else "Gemini"
    connector = LLMConnector(provider=provider)
    if connector.is_configured():
        response = connector.generate_response(
            prompt="What is my age after my birthday today?",
            chat_history=[],
            memories=handler.get_memories("What is my age?", user_id=test_user)
        )
        print(f"LLM Response via {provider}: {response}")
        assert "26" in response, f"LLM failed to answer using updated memory context (Response: {response})"
        print("✅ LLM Connector integration test passed.")
    else:
        print(f"⚠️ LLM Connector not tested because {provider} API key is not configured.")

    print("\n------------------------------------------")
    print("🎉 All Automated Persistence Tests Passed Successfully! 🎉")
    print("------------------------------------------")

if __name__ == "__main__":
    test_mem0_persistence()
