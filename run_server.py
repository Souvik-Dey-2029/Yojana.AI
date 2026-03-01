import uvicorn
import os
import sys

# Ensure the current directory is in the Python path
sys.path.append(os.getcwd())

if __name__ == "__main__":
    print("🚀 Starting Yojana.AI Server...")
    # Using the module string format for uvicorn to handle absolute imports correctly
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
