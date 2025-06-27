#!/usr/bin/env python3
"""
Setup script for Notion integration to fetch [Docs] tickets.
This script helps configure the environment and credentials.
"""

import os
import subprocess
import sys
from pathlib import Path

def install_notion_client():
    """Install the notion-client package."""
    print("📦 Installing notion-client...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "notion-client"])
        print("✅ notion-client installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install notion-client")
        return False

def create_env_file():
    """Create a .env file template for storing credentials."""
    env_file = Path(".env")
    
    if env_file.exists():
        print("📄 .env file already exists")
        return
    
    env_template = """# Notion Integration Credentials
# Add your actual values here and remove the # comments

# Your Notion Integration Token (starts with 'secret_')
# Get this from: https://www.notion.so/my-integrations
# NOTION_TOKEN=secret_your_token_here

# Your Notion Database ID (32-character string)
# Get this from your database URL: https://notion.so/your-workspace/DATABASE_ID?v=...
# NOTION_DATABASE_ID=your_database_id_here
"""
    
    with open(env_file, 'w') as f:
        f.write(env_template)
    
    print(f"📄 Created .env template file: {env_file.absolute()}")
    print("   Please edit this file and add your actual Notion credentials")

def print_setup_instructions():
    """Print detailed setup instructions."""
    print("\n" + "="*80)
    print("🚀 NOTION INTEGRATION SETUP INSTRUCTIONS")
    print("="*80)
    
    print("\n1️⃣ CREATE A NOTION INTEGRATION:")
    print("   • Go to https://www.notion.so/my-integrations")
    print("   • Click 'New integration'")
    print("   • Give it a name (e.g., 'Docs Ticket Fetcher')")
    print("   • Select your workspace")
    print("   • Click 'Submit'")
    print("   • Copy the 'Internal Integration Token' (starts with 'secret_')")
    
    print("\n2️⃣ SHARE YOUR DATABASE WITH THE INTEGRATION:")
    print("   • Go to your Notion database page")
    print("   • Click the '...' menu in the top right")
    print("   • Click 'Add connections'")
    print("   • Search for and select your integration")
    print("   • Click 'Confirm'")
    
    print("\n3️⃣ GET YOUR DATABASE ID:")
    print("   • Go to your Notion database page")
    print("   • Copy the URL - it looks like:")
    print("     https://www.notion.so/your-workspace/DATABASE_ID?v=VIEW_ID")
    print("   • The DATABASE_ID is the 32-character string (with dashes)")
    
    print("\n4️⃣ SET UP ENVIRONMENT VARIABLES:")
    print("   Option A - Using .env file (recommended):")
    print("   • Edit the .env file created by this script")
    print("   • Uncomment and fill in your actual values")
    print("   • Install python-dotenv: pip install python-dotenv")
    print("   • Add this to the top of the script:")
    print("     from dotenv import load_dotenv")
    print("     load_dotenv()")
    
    print("\n   Option B - Using environment variables:")
    print("   export NOTION_TOKEN='secret_your_token_here'")
    print("   export NOTION_DATABASE_ID='your_database_id_here'")
    
    print("\n5️⃣ RUN THE SCRIPT:")
    print("   python scripts/fetch_notion_docs_tickets.py")
    
    print("\n" + "="*80)

def check_existing_credentials():
    """Check if credentials are already set up."""
    token = os.getenv('NOTION_TOKEN')
    db_id = os.getenv('NOTION_DATABASE_ID')
    
    if token and db_id:
        print("✅ Environment variables are already set!")
        print(f"   NOTION_TOKEN: {'*' * 20}{token[-10:] if len(token) > 10 else '*' * len(token)}")
        print(f"   NOTION_DATABASE_ID: {db_id}")
        return True
    else:
        print("⚠️  Environment variables not found")
        if token:
            print(f"   ✅ NOTION_TOKEN is set")
        else:
            print(f"   ❌ NOTION_TOKEN is not set")
            
        if db_id:
            print(f"   ✅ NOTION_DATABASE_ID is set")
        else:
            print(f"   ❌ NOTION_DATABASE_ID is not set")
        return False

def test_notion_connection():
    """Test the Notion connection with current credentials."""
    try:
        from notion_client import Client
        
        token = os.getenv('NOTION_TOKEN')
        db_id = os.getenv('NOTION_DATABASE_ID')
        
        if not token or not db_id:
            print("❌ Cannot test connection - credentials not set")
            return False
        
        print("🔗 Testing Notion connection...")
        client = Client(auth=token)
        
        # Test basic connection
        response = client.databases.retrieve(database_id=db_id)
        
        print("✅ Connection successful!")
        print(f"   Database: {response.get('title', [{}])[0].get('plain_text', 'Unknown')}")
        return True
        
    except ImportError:
        print("❌ notion-client not installed")
        return False
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        return False

def main():
    """Main setup function."""
    print("🔧 Setting up Notion integration for fetching [Docs] tickets...\n")
    
    # Check current credentials
    credentials_exist = check_existing_credentials()
    
    # Install dependencies
    if not install_notion_client():
        return
    
    # Create .env file
    create_env_file()
    
    # Test connection if credentials exist
    if credentials_exist:
        test_notion_connection()
    
    # Print setup instructions
    print_setup_instructions()
    
    if not credentials_exist:
        print("\n🔔 NEXT STEPS:")
        print("1. Follow the setup instructions above")
        print("2. Edit the .env file with your credentials")
        print("3. Run this script again to test the connection")
        print("4. Then run: python scripts/fetch_notion_docs_tickets.py")

if __name__ == "__main__":
    main() 