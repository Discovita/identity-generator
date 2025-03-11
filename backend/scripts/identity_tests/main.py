#!/usr/bin/env python3
"""
Interactive test script for the coach identity generation functionality.

This script tests the coach's ability to generate identities by simulating
a conversation focused on creating the identity "I am a talented engineer".
"""

import argparse
import sys

from .api import check_server_health
from .tester import IdentityTester

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Test coach identity generation")
    parser.add_argument(
        "--url", 
        default="http://localhost:8000", 
        help="Base URL for the coach API (default: http://localhost:8000)"
    )
    return parser.parse_args()

def main():
    """Main entry point."""
    args = parse_args()
    
    print("Identity Generation Test")
    print("=======================")
    print(f"API URL: {args.url}")
    print("This script will test the coach's ability to generate the 'talented engineer' identity.")
    print("The script will guide the conversation and check if the identity is generated.")
    print("You can continue the conversation interactively if needed.")
    
    # Check if the server is running
    if not check_server_health(args.url):
        print("❌ Server is not running. Please start the server and try again.")
        print("   Run: cd backend && uvicorn discovita.app:app --reload")
        sys.exit(1)
    
    print("✅ Server is running")
    
    # Run the test
    tester = IdentityTester(args.url)
    tester.run_test()

if __name__ == "__main__":
    main()
