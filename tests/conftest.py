# -*- coding: utf-8 -*-
import os
import pytest

# Configure VCR for test recordings
os.environ["VCR_RECORD_MODE"] = "once"

# Update fixtures for new Wikipedia API format
