# -*- coding: utf-8 -*-
import os
import pytest

# Configure VCR for test recordings
os.environ["VCR_RECORD_MODE"] = "new_episodes"

# Update fixtures for new Wikipedia API format
