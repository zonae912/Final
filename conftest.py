# AI Contribution: Copilot generated pytest configuration
# Reviewed and validated by team

"""
pytest configuration file for Campus Resource Hub.
Sets up Python path and test fixtures.
"""

import sys
import os

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
