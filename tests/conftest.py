#!/usr/bin/env python3
"""pytest configuration - adds src to path"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
