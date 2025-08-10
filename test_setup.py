import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app

if __name__ == "__main__":
    print("✅ FastAPI app imported successfully!")
    print("🚀 Project structure is working correctly!")
    print("\nAvailable routes:")
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            methods = ', '.join(route.methods)
            print(f"  {methods} {route.path}")

    print("\n🎉 Project setup validation completed!")
    print("\nTo run the server:")
    print("  python run.py")
    print("\nTo view API docs:")
    print("  http://localhost:8000/docs")
