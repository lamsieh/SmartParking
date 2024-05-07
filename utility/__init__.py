import sys
import os

# Add parent directory of 'utility' module to Python path
utility_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utility'))
sys.path.append(utility_path)
