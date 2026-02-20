#!/usr/bin/env python3
"""
ShikshyaHub Setup Script
Run this to initialize the database and start the server
"""
import subprocess
import sys
import os

def install_requirements():
    print("📦 Installing requirements...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--break-system-packages',
                    'flask', 'qrcode', 'pillow'], check=True, capture_output=True)
    print("✅ Requirements installed!")

def initialize_db():
    print("🗄️  Initializing database...")
    sys.path.insert(0, os.path.dirname(__file__))
    from app import init_db
    init_db()
    print("✅ Database initialized!")
    print("\n🔐 Demo Credentials:")
    print("   Admin:   admin@shikshyahub.edu / Admin@123")
    print("   Teacher: teacher@shikshyahub.edu / Teacher@123")
    print("   Student: student@shikshyahub.edu / Student@123")

if __name__ == '__main__':
    install_requirements()
    initialize_db()
    print("\n🚀 Starting ShikshyaHub...")
    print("   Open http://localhost:5000 in your browser")
    os.system(f'{sys.executable} app.py')
