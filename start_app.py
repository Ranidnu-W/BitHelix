#!/usr/bin/env python3
"""
Startup script for the DNA Storage application.

This script provides a convenient way to start the DNA Storage application,
including dependency checking, installation, and launching both backend and frontend.
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import fastapi
        import uvicorn
        print("✅ FastAPI dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def install_dependencies():
    """Install Python dependencies."""
    print("Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def start_backend():
    """Start the FastAPI backend server."""
    print("🚀 Starting DNA Storage API backend...")
    print("📍 Backend will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    
    try:
        # Start the FastAPI server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "api_server:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")

def check_frontend():
    """Check if frontend dependencies are installed."""
    frontend_dir = Path("DNA-storage-frontend_MK1")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    package_json = frontend_dir / "package.json"
    if not package_json.exists():
        print("❌ Frontend package.json not found")
        return False
    
    node_modules = frontend_dir / "node_modules"
    if not node_modules.exists():
        print("⚠️  Frontend dependencies not installed")
        return False
    
    print("✅ Frontend dependencies found")
    return True

def install_frontend_dependencies():
    """Install frontend dependencies."""
    frontend_dir = Path("DNA-storage-frontend_MK1")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    print("Installing frontend dependencies...")
    try:
        subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
        print("✅ Frontend dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install frontend dependencies")
        return False
    except FileNotFoundError:
        print("❌ Node.js/npm not found. Please install Node.js first.")
        return False

def start_frontend():
    """Start the frontend development server."""
    frontend_dir = Path("DNA-storage-frontend_MK1")
    
    print("🌐 Starting frontend development server...")
    print("📍 Frontend will be available at: http://localhost:3000")
    
    try:
        subprocess.run(["npm", "run", "dev"], cwd=frontend_dir)
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped")
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")

def main():
    """Main startup function."""
    print("🧬 DNA Storage Application")
    print("=" * 50)
    
    # Check and install Python dependencies
    if not check_dependencies():
        print("\nInstalling Python dependencies...")
        if not install_dependencies():
            return
    
    # Check and install frontend dependencies
    if not check_frontend():
        print("\nInstalling frontend dependencies...")
        if not install_frontend_dependencies():
            print("⚠️  Frontend dependencies not installed. You can still run the backend.")
    
    print("\n🎯 Starting the application...")
    print("=" * 50)
    
    # Start backend in a separate process
    backend_process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "api_server:app", 
        "--host", "0.0.0.0", 
        "--port", "8000",
        "--reload"
    ])
    
    try:
        # Wait a moment for backend to start
        time.sleep(3)
        
        # Open browser to backend docs
        print("📚 Opening API documentation...")
        webbrowser.open("http://localhost:8000/docs")
        
        print("\n✅ Backend is running!")
        print("📍 API: http://localhost:8000")
        print("📚 Docs: http://localhost:8000/docs")
        
        print("\n🌐 To start the frontend:")
        print("1. Open a new terminal")
        print("2. Navigate to: DNA-storage-frontend_MK1")
        print("3. Run: npm run dev")
        print("4. Open: http://localhost:3000")
        
        print("\n🔄 Backend is running. Press Ctrl+C to stop.")
        
        # Keep the backend running
        backend_process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping backend...")
        backend_process.terminate()
        backend_process.wait()
        print("✅ Backend stopped")

if __name__ == "__main__":
    main() 