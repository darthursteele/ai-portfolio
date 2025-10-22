"""
Environment configuration management.
"""

import os
from enum import Enum
from typing import Dict, Any, Optional


class Environment(str, Enum):
    """Environment types."""
    
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


def get_environment() -> Environment:
    """
    Get the current environment from environment variables.
    
    Returns:
        Current environment (defaults to DEVELOPMENT)
    """
    env_name = os.getenv("ENVIRONMENT", "development").lower()
    
    try:
        return Environment(env_name)
    except ValueError:
        return Environment.DEVELOPMENT


class EnvironmentConfig:
    """Environment-specific configuration."""
    
    def __init__(self, environment: Environment):
        """
        Initialize environment configuration.
        
        Args:
            environment: Target environment
        """
        self.environment = environment
        self._config = self._load_environment_config()
    
    def _load_environment_config(self) -> Dict[str, Any]:
        """Load configuration for the current environment."""
        base_config = {
            "log_level": "INFO",
            "debug": False,
            "telemetry_enabled": True,
            "cache_enabled": True,
            "max_concurrent_tasks": 5,
            "timeout_seconds": 300,
            "retry_attempts": 3,
        }
        
        if self.environment == Environment.DEVELOPMENT:
            return {
                **base_config,
                "log_level": "DEBUG",
                "debug": True,
                "telemetry_enabled": False,
                "hot_reload": True,
                "cache_ttl": 60,  # 1 minute
                "max_concurrent_tasks": 3,
            }
        
        elif self.environment == Environment.TESTING:
            return {
                **base_config,
                "log_level": "WARNING",
                "debug": False,
                "telemetry_enabled": False,
                "cache_enabled": False,
                "timeout_seconds": 30,
                "max_concurrent_tasks": 2,
                "retry_attempts": 1,
            }
        
        elif self.environment == Environment.STAGING:
            return {
                **base_config,
                "log_level": "INFO",
                "debug": False,
                "telemetry_enabled": True,
                "cache_ttl": 300,  # 5 minutes
                "max_concurrent_tasks": 8,
                "timeout_seconds": 600,
            }
        
        elif self.environment == Environment.PRODUCTION:
            return {
                **base_config,
                "log_level": "WARNING",
                "debug": False,
                "telemetry_enabled": True,
                "cache_ttl": 3600,  # 1 hour
                "max_concurrent_tasks": 10,
                "timeout_seconds": 900,
                "retry_attempts": 5,
                "monitoring_enabled": True,
                "performance_tracking": True,
            }
        
        return base_config
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self._config.get(key, default)
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get all configuration values.
        
        Returns:
            Complete configuration dictionary
        """
        return self._config.copy()
    
    def update(self, updates: Dict[str, Any]) -> None:
        """
        Update configuration values.
        
        Args:
            updates: Dictionary of updates to apply
        """
        self._config.update(updates)
    
    @property
    def is_development(self) -> bool:
        """Check if environment is development."""
        return self.environment == Environment.DEVELOPMENT
    
    @property
    def is_testing(self) -> bool:
        """Check if environment is testing."""
        return self.environment == Environment.TESTING
    
    @property
    def is_staging(self) -> bool:
        """Check if environment is staging."""
        return self.environment == Environment.STAGING
    
    @property
    def is_production(self) -> bool:
        """Check if environment is production."""
        return self.environment == Environment.PRODUCTION


# Global environment configuration instance
_environment_config: Optional[EnvironmentConfig] = None


def get_environment_config() -> EnvironmentConfig:
    """
    Get the global environment configuration instance.
    
    Returns:
        Environment configuration instance
    """
    global _environment_config
    
    if _environment_config is None:
        current_env = get_environment()
        _environment_config = EnvironmentConfig(current_env)
    
    return _environment_config


def reset_environment_config() -> None:
    """Reset the global environment configuration (mainly for testing)."""
    global _environment_config
    _environment_config = None