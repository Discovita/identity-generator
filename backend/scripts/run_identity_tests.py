#!/usr/bin/env python3
"""
Wrapper script to run the identity generation test.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from identity_tests.main import main

if __name__ == "__main__":
    main()
