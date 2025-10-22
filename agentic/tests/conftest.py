"""
Pytest configuration and fixtures for AI Portfolio tests.
"""

import pytest
import os
from unittest.mock import Mock, patch
from typing import Generator


@pytest.fixture
def mock_env_vars() -> Generator[dict, None, None]:
    """Mock environment variables for testing."""
    env_vars = {
        "OPENAI_API_KEY": "test-openai-key",
        "ANTHROPIC_API_KEY": "test-anthropic-key",
        "GOOGLE_API_KEY": "test-google-key",
        "CREWAI_TELEMETRY_OPT_OUT": "true",
    }
    
    with patch.dict(os.environ, env_vars):
        yield env_vars


@pytest.fixture
def mock_crewai_tools():
    """Mock CrewAI tools to avoid external dependencies in tests."""
    with patch("crewai_tools.SerperDevTool") as mock_serper, \
         patch("crewai_tools.FileReaderTool") as mock_reader, \
         patch("crewai_tools.FileWriterTool") as mock_writer:
        
        mock_serper.return_value = Mock()
        mock_reader.return_value = Mock()
        mock_writer.return_value = Mock()
        
        yield {
            "serper": mock_serper,
            "reader": mock_reader, 
            "writer": mock_writer
        }


@pytest.fixture
def sample_content():
    """Sample content for testing content analysis."""
    return """
    Artificial Intelligence has revolutionized the way we approach problem-solving.
    Machine learning algorithms can now process vast amounts of data to identify patterns
    that would be impossible for humans to detect manually. This technology has applications
    in healthcare, finance, transportation, and many other industries.
    
    The future of AI looks promising, with developments in natural language processing,
    computer vision, and robotics advancing rapidly. However, we must also consider
    the ethical implications and ensure responsible development.
    """


@pytest.fixture
def temp_file(tmp_path):
    """Create a temporary file for testing."""
    def _create_temp_file(content: str, filename: str = "test_file.txt"):
        file_path = tmp_path / filename
        file_path.write_text(content)
        return str(file_path)
    
    return _create_temp_file


# Markers for different test types
pytestmark = [
    pytest.mark.filterwarnings("ignore::DeprecationWarning"),
    pytest.mark.filterwarnings("ignore::PendingDeprecationWarning"),
]