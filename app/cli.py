#!/usr/bin/env python3
"""CLI commands for the FastAPI Todo application."""

import subprocess
import sys
import signal


def run_dev():
    """Run development server with auto-reload"""
    cmd = [
        "uvicorn",
        "app.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
    ]

    try:
        # Run uvicorn directly without subprocess to handle signals properly
        import uvicorn
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Development server stopped")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)


def run_start():
    """Run production server"""
    try:
        import uvicorn
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=False
        )
    except KeyboardInterrupt:
        print("\n🛑 Production server stopped")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "dev":
            run_dev()
        elif command == "start":
            run_start()
        else:
            print(f"Unknown command: {command}")
            sys.exit(1)
    else:
        print("Usage: python -m app.cli [dev|start]")
        sys.exit(1)
