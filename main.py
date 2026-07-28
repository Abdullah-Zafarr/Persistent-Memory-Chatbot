import subprocess
import sys

def main():
    print("Starting Persistent Memory Chatbot...")
    print("Make sure you are using your Python 3.14 environment.")
    cmd = [sys.executable, "-m", "streamlit", "run", "src/app.py"]
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\nChatbot stopped.")
    except Exception as e:
        print(f"Error starting Streamlit chatbot: {e}")


if __name__ == "__main__":
    main()

