"""
Application settings and configuration management.
"""

import os
import json
from typing import Any, Dict, Optional, List
from pathlib import Path
from pydantic import BaseModel, Field, validator
from pydantic_settings import BaseSettings

from .environments import Environment, get_environment, get_environment_config


class LLMConfig(BaseModel):
    """LLM provider configuration."""
    
    provider: str = Field(..., description="LLM provider name")
    api_key: Optional[str] = Field(default=None, description="API key for the provider")
    model: str = Field(..., description="Model name")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Temperature setting")
    max_tokens: Optional[int] = Field(default=None, description="Maximum tokens")
    timeout: int = Field(default=60, description="Request timeout in seconds")
    
    @validator('provider')
    def validate_provider(cls, v):
        """Validate LLM provider."""
        allowed_providers = ["openai", "anthropic", "google", "azure"]
        if v.lower() not in allowed_providers:
            raise ValueError(f"Provider must be one of: {allowed_providers}")
        return v.lower()


class DatabaseConfig(BaseModel):
    """Database configuration."""
    
    type: str = Field(default="chromadb", description="Database type")
    host: str = Field(default="localhost", description="Database host")
    port: int = Field(default=8000, description="Database port")
    database: str = Field(default="ai_portfolio", description="Database name")
    username: Optional[str] = Field(default=None, description="Database username")
    password: Optional[str] = Field(default=None, description="Database password")
    persist_directory: Optional[str] = Field(default="./chroma_db", description="Persistence directory")
    
    @validator('type')
    def validate_db_type(cls, v):
        """Validate database type."""
        allowed_types = ["chromadb", "postgres", "redis", "sqlite"]
        if v.lower() not in allowed_types:
            raise ValueError(f"Database type must be one of: {allowed_types}")
        return v.lower()


class CrewConfig(BaseModel):
    """CrewAI configuration."""
    
    max_concurrent_crews: int = Field(default=3, description="Maximum concurrent crew executions")
    default_timeout: int = Field(default=300, description="Default timeout for crew execution")
    memory_enabled: bool = Field(default=True, description="Enable crew memory")
    verbose: bool = Field(default=True, description="Enable verbose logging")
    telemetry_opt_out: bool = Field(default=True, description="Opt out of telemetry")


class Settings(BaseSettings):
    """Main application settings."""
    
    # Environment
    environment: Environment = Field(default_factory=get_environment)
    debug: bool = Field(default=False, description="Debug mode")
    
    # LLM Configuration
    default_llm: LLMConfig = Field(
        default_factory=lambda: LLMConfig(
            provider="openai",
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7
        )
    )
    
    # Alternative LLM providers
    anthropic_llm: Optional[LLMConfig] = Field(
        default_factory=lambda: LLMConfig(
            provider="anthropic",
            model="claude-3-haiku-20240307",
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            temperature=0.7
        ) if os.getenv("ANTHROPIC_API_KEY") else None
    )
    
    google_llm: Optional[LLMConfig] = Field(
        default_factory=lambda: LLMConfig(
            provider="google",
            model="gemini-pro",
            api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7
        ) if os.getenv("GOOGLE_API_KEY") else None
    )
    
    # Database configuration
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    
    # CrewAI configuration
    crew: CrewConfig = Field(default_factory=CrewConfig)
    
    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: Optional[str] = Field(default="logs/ai_portfolio.log", description="Log file path")
    
    # Performance
    cache_enabled: bool = Field(default=True, description="Enable caching")
    cache_ttl: int = Field(default=3600, description="Cache TTL in seconds")
    max_workers: int = Field(default=4, description="Maximum worker threads")
    
    # Security
    api_rate_limit: int = Field(default=100, description="API rate limit per minute")
    max_file_size: int = Field(default=10485760, description="Maximum file size (10MB)")
    allowed_file_types: List[str] = Field(
        default=["txt", "md", "json", "csv", "pdf"],
        description="Allowed file types for upload"
    )
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        validate_assignment = True
    
    def __init__(self, **kwargs):
        """Initialize settings with environment-specific defaults."""
        super().__init__(**kwargs)
        
        # Apply environment-specific configuration
        env_config = get_environment_config()
        
        # Update settings based on environment
        if hasattr(self, 'log_level'):
            self.log_level = env_config.get('log_level', self.log_level)
        
        if hasattr(self, 'debug'):
            self.debug = env_config.get('debug', self.debug)
        
        if hasattr(self, 'cache_enabled'):
            self.cache_enabled = env_config.get('cache_enabled', self.cache_enabled)
        
        if hasattr(self, 'cache_ttl'):
            self.cache_ttl = env_config.get('cache_ttl', self.cache_ttl)
        
        if hasattr(self, 'max_workers'):
            self.max_workers = env_config.get('max_concurrent_tasks', self.max_workers)
        
        # Set CrewAI telemetry
        if env_config.get('telemetry_enabled', True) is False:
            os.environ['CREWAI_TELEMETRY_OPT_OUT'] = 'true'
    
    @classmethod
    def from_file(cls, config_path: str) -> "Settings":
        """
        Load settings from a configuration file.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            Settings instance
        """
        config_file = Path(config_path)
        
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        if config_file.suffix.lower() == '.json':
            with open(config_file, 'r') as f:
                config_data = json.load(f)
        else:
            raise ValueError("Only JSON configuration files are supported")
        
        return cls(**config_data)
    
    def to_file(self, config_path: str) -> None:
        """
        Save settings to a configuration file.
        
        Args:
            config_path: Path to save configuration
        """
        config_file = Path(config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_file, 'w') as f:
            json.dump(self.model_dump(), f, indent=2, default=str)
    
    def get_llm_config(self, provider: Optional[str] = None) -> LLMConfig:
        """
        Get LLM configuration for specified provider.
        
        Args:
            provider: LLM provider name (defaults to default_llm)
            
        Returns:
            LLM configuration
        """
        if provider is None:
            return self.default_llm
        
        provider = provider.lower()
        
        if provider == "anthropic" and self.anthropic_llm:
            return self.anthropic_llm
        elif provider == "google" and self.google_llm:
            return self.google_llm
        elif provider == "openai":
            return self.default_llm
        else:
            raise ValueError(f"Unknown or unconfigured LLM provider: {provider}")
    
    def validate_api_keys(self) -> Dict[str, bool]:
        """
        Validate that required API keys are available.
        
        Returns:
            Dictionary showing which API keys are available
        """
        return {
            "openai": bool(self.default_llm.api_key),
            "anthropic": bool(self.anthropic_llm and self.anthropic_llm.api_key),
            "google": bool(self.google_llm and self.google_llm.api_key),
        }
    
    def get_database_url(self) -> str:
        """
        Get database connection URL.
        
        Returns:
            Database connection URL
        """
        if self.database.type == "chromadb":
            return f"http://{self.database.host}:{self.database.port}"
        elif self.database.type == "postgres":
            auth = ""
            if self.database.username and self.database.password:
                auth = f"{self.database.username}:{self.database.password}@"
            return f"postgresql://{auth}{self.database.host}:{self.database.port}/{self.database.database}"
        elif self.database.type == "redis":
            return f"redis://{self.database.host}:{self.database.port}"
        elif self.database.type == "sqlite":
            return f"sqlite:///{self.database.database}.db"
        else:
            raise ValueError(f"Unsupported database type: {self.database.type}")
    
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == Environment.DEVELOPMENT
    
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == Environment.PRODUCTION