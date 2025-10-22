"""
Validation utilities for AI Portfolio project.
"""

import re
import json
from typing import Any, Dict, List, Optional, Union, Callable
from pathlib import Path
from datetime import datetime

from ..config.settings import Settings
from .logging_utils import get_logger


class ValidationError(Exception):
    """Custom validation error."""
    pass


class ValidationUtils:
    """Utility class for data validation."""
    
    def __init__(self, settings: Optional[Settings] = None):
        """
        Initialize validation utilities.
        
        Args:
            settings: Application settings
        """
        self.settings = settings or Settings()
        self.logger = get_logger("validation_utils")
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email address format.
        
        Args:
            email: Email address to validate
            
        Returns:
            True if email is valid
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate URL format.
        
        Args:
            url: URL to validate
            
        Returns:
            True if URL is valid
        """
        pattern = r'^https?://(?:[-\w.])+(?::[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$'
        return bool(re.match(pattern, url))
    
    @staticmethod
    def validate_api_key_format(api_key: str, provider: str) -> bool:
        """
        Validate API key format for different providers.
        
        Args:
            api_key: API key to validate
            provider: LLM provider name
            
        Returns:
            True if API key format is valid
        """
        if not api_key or not isinstance(api_key, str):
            return False
        
        provider = provider.lower()
        
        if provider == "openai":
            # OpenAI keys start with 'sk-' and are 51 characters long
            return api_key.startswith("sk-") and len(api_key) == 51
        
        elif provider == "anthropic":
            # Anthropic keys start with 'sk-ant-'
            return api_key.startswith("sk-ant-") and len(api_key) > 20
        
        elif provider == "google":
            # Google API keys are typically 39 characters long
            return len(api_key) == 39 and api_key.isalnum()
        
        else:
            # Generic validation: at least 20 characters, alphanumeric + some special chars
            return len(api_key) >= 20 and re.match(r'^[a-zA-Z0-9_-]+$', api_key)
    
    @staticmethod
    def validate_json_structure(
        data: Union[str, Dict[str, Any]],
        required_fields: List[str],
        optional_fields: Optional[List[str]] = None
    ) -> bool:
        """
        Validate JSON structure against required and optional fields.
        
        Args:
            data: JSON data (string or dict)
            required_fields: List of required field names
            optional_fields: List of optional field names
            
        Returns:
            True if structure is valid
        """
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                return False
        
        if not isinstance(data, dict):
            return False
        
        # Check required fields
        for field in required_fields:
            if field not in data:
                return False
        
        # Check that no unexpected fields are present
        if optional_fields:
            allowed_fields = set(required_fields + optional_fields)
            for field in data:
                if field not in allowed_fields:
                    return False
        
        return True
    
    def validate_file_content(self, filepath: Union[str, Path], max_size: Optional[int] = None) -> bool:
        """
        Validate file content and size.
        
        Args:
            filepath: Path to file
            max_size: Maximum file size in bytes
            
        Returns:
            True if file is valid
        """
        file_path = Path(filepath)
        
        if not file_path.exists():
            return False
        
        if not file_path.is_file():
            return False
        
        # Check file size
        file_size = file_path.stat().st_size
        max_allowed = max_size or self.settings.max_file_size
        
        if file_size > max_allowed:
            return False
        
        # Check file type
        extension = file_path.suffix.lower().lstrip('.')
        if extension not in self.settings.allowed_file_types:
            return False
        
        return True
    
    @staticmethod
    def validate_crew_config(config: Dict[str, Any]) -> List[str]:
        """
        Validate CrewAI crew configuration.
        
        Args:
            config: Crew configuration dictionary
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Required fields
        required_fields = ["agents", "tasks"]
        for field in required_fields:
            if field not in config:
                errors.append(f"Missing required field: {field}")
        
        # Validate agents
        if "agents" in config:
            agents = config["agents"]
            if not isinstance(agents, list) or len(agents) == 0:
                errors.append("Agents must be a non-empty list")
            else:
                for i, agent in enumerate(agents):
                    if not isinstance(agent, dict):
                        errors.append(f"Agent {i} must be a dictionary")
                        continue
                    
                    # Check required agent fields
                    required_agent_fields = ["role", "goal", "backstory"]
                    for field in required_agent_fields:
                        if field not in agent or not agent[field].strip():
                            errors.append(f"Agent {i} missing or empty field: {field}")
        
        # Validate tasks
        if "tasks" in config:
            tasks = config["tasks"]
            if not isinstance(tasks, list) or len(tasks) == 0:
                errors.append("Tasks must be a non-empty list")
            else:
                for i, task in enumerate(tasks):
                    if not isinstance(task, dict):
                        errors.append(f"Task {i} must be a dictionary")
                        continue
                    
                    # Check required task fields
                    required_task_fields = ["description", "expected_output"]
                    for field in required_task_fields:
                        if field not in task or not task[field].strip():
                            errors.append(f"Task {i} missing or empty field: {field}")
        
        return errors
    
    @staticmethod
    def validate_agent_config(config: Dict[str, Any]) -> List[str]:
        """
        Validate agent configuration.
        
        Args:
            config: Agent configuration dictionary
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Required fields
        required_fields = ["role", "goal", "backstory"]
        for field in required_fields:
            if field not in config:
                errors.append(f"Missing required field: {field}")
            elif not isinstance(config[field], str) or not config[field].strip():
                errors.append(f"Field '{field}' must be a non-empty string")
        
        # Optional boolean fields
        boolean_fields = ["verbose", "allow_delegation", "memory"]
        for field in boolean_fields:
            if field in config and not isinstance(config[field], bool):
                errors.append(f"Field '{field}' must be a boolean")
        
        # Optional integer fields
        integer_fields = ["max_iter", "max_execution_time"]
        for field in integer_fields:
            if field in config:
                if not isinstance(config[field], int) or config[field] <= 0:
                    errors.append(f"Field '{field}' must be a positive integer")
        
        return errors
    
    @staticmethod
    def validate_task_config(config: Dict[str, Any]) -> List[str]:
        """
        Validate task configuration.
        
        Args:
            config: Task configuration dictionary
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Required fields
        required_fields = ["description", "expected_output"]
        for field in required_fields:
            if field not in config:
                errors.append(f"Missing required field: {field}")
            elif not isinstance(config[field], str) or not config[field].strip():
                errors.append(f"Field '{field}' must be a non-empty string")
        
        # Optional fields validation
        if "agent" in config and config["agent"] is not None:
            if not hasattr(config["agent"], "role"):
                errors.append("Agent must have a 'role' attribute")
        
        if "context" in config:
            if not isinstance(config["context"], list):
                errors.append("Context must be a list of tasks")
        
        return errors
    
    def validate_settings(self, settings: Dict[str, Any]) -> List[str]:
        """
        Validate application settings.
        
        Args:
            settings: Settings dictionary
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Validate LLM configurations
        if "default_llm" in settings:
            llm_config = settings["default_llm"]
            if not isinstance(llm_config, dict):
                errors.append("default_llm must be a dictionary")
            else:
                # Check required LLM fields
                required_llm_fields = ["provider", "model"]
                for field in required_llm_fields:
                    if field not in llm_config or not llm_config[field]:
                        errors.append(f"LLM config missing field: {field}")
                
                # Validate API key if present
                if "api_key" in llm_config and llm_config["api_key"]:
                    provider = llm_config.get("provider", "")
                    if not self.validate_api_key_format(llm_config["api_key"], provider):
                        errors.append(f"Invalid API key format for provider: {provider}")
        
        # Validate database configuration
        if "database" in settings:
            db_config = settings["database"]
            if not isinstance(db_config, dict):
                errors.append("database must be a dictionary")
            else:
                # Check database type
                if "type" in db_config:
                    allowed_types = ["chromadb", "postgres", "redis", "sqlite"]
                    if db_config["type"] not in allowed_types:
                        errors.append(f"Database type must be one of: {allowed_types}")
        
        # Validate numeric fields
        numeric_fields = {
            "cache_ttl": (1, 86400),  # 1 second to 1 day
            "max_workers": (1, 50),   # 1 to 50 workers
            "api_rate_limit": (1, 10000),  # 1 to 10000 requests per minute
            "max_file_size": (1024, 1073741824)  # 1KB to 1GB
        }
        
        for field, (min_val, max_val) in numeric_fields.items():
            if field in settings:
                value = settings[field]
                if not isinstance(value, int) or not (min_val <= value <= max_val):
                    errors.append(f"Field '{field}' must be an integer between {min_val} and {max_val}")
        
        return errors
    
    @staticmethod
    def sanitize_input(text: str, max_length: Optional[int] = None) -> str:
        """
        Sanitize user input by removing/escaping potentially harmful content.
        
        Args:
            text: Input text to sanitize
            max_length: Maximum allowed length
            
        Returns:
            Sanitized text
        """
        if not isinstance(text, str):
            return ""
        
        # Remove control characters except newline and tab
        sanitized = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)
        
        # Limit length if specified
        if max_length and len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        # Trim whitespace
        sanitized = sanitized.strip()
        
        return sanitized
    
    @staticmethod
    def validate_with_schema(
        data: Dict[str, Any],
        schema: Dict[str, Any]
    ) -> List[str]:
        """
        Validate data against a simple schema.
        
        Args:
            data: Data to validate
            schema: Schema dictionary with field definitions
            
        Returns:
            List of validation errors
        """
        errors = []
        
        # Check required fields
        required_fields = schema.get("required", [])
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        # Check field types and constraints
        field_definitions = schema.get("fields", {})
        for field_name, definition in field_definitions.items():
            if field_name not in data:
                continue
            
            value = data[field_name]
            field_type = definition.get("type")
            
            # Type validation
            if field_type == "string" and not isinstance(value, str):
                errors.append(f"Field '{field_name}' must be a string")
            elif field_type == "integer" and not isinstance(value, int):
                errors.append(f"Field '{field_name}' must be an integer")
            elif field_type == "boolean" and not isinstance(value, bool):
                errors.append(f"Field '{field_name}' must be a boolean")
            elif field_type == "list" and not isinstance(value, list):
                errors.append(f"Field '{field_name}' must be a list")
            
            # Length constraints
            if "min_length" in definition:
                if hasattr(value, "__len__") and len(value) < definition["min_length"]:
                    errors.append(f"Field '{field_name}' must have at least {definition['min_length']} characters/items")
            
            if "max_length" in definition:
                if hasattr(value, "__len__") and len(value) > definition["max_length"]:
                    errors.append(f"Field '{field_name}' must have at most {definition['max_length']} characters/items")
            
            # Value constraints
            if "min_value" in definition:
                if isinstance(value, (int, float)) and value < definition["min_value"]:
                    errors.append(f"Field '{field_name}' must be at least {definition['min_value']}")
            
            if "max_value" in definition:
                if isinstance(value, (int, float)) and value > definition["max_value"]:
                    errors.append(f"Field '{field_name}' must be at most {definition['max_value']}")
            
            # Choices validation
            if "choices" in definition:
                if value not in definition["choices"]:
                    errors.append(f"Field '{field_name}' must be one of: {definition['choices']}")
        
        return errors