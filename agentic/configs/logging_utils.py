"""
Logging utilities for AI Portfolio project.
"""

import logging
import logging.config
import os
import yaml
from pathlib import Path
from typing import Optional


def setup_logging(
    config_path: Optional[str] = None,
    default_level: int = logging.INFO,
    env_key: str = "LOG_CFG"
) -> None:
    """
    Setup logging configuration.
    
    Args:
        config_path: Path to logging configuration file
        default_level: Default logging level if config file not found
        env_key: Environment variable name for config path override
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Determine config path
    if config_path is None:
        config_path = os.getenv(env_key, None)
    
    if config_path is None:
        # Use default config path relative to this file
        config_path = Path(__file__).parent / "logging.yaml"
    
    config_path = Path(config_path)
    
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        # Fallback to basic configuration
        logging.basicConfig(
            level=default_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        logging.warning(f"Logging config file not found at {config_path}. Using basic configuration.")


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def log_agent_action(agent_name: str, action: str, details: Optional[dict] = None) -> None:
    """
    Log agent actions with structured data.
    
    Args:
        agent_name: Name of the agent
        action: Action being performed
        details: Additional details about the action
    """
    logger = get_logger("agentic.agents")
    
    log_data = {
        "agent": agent_name,
        "action": action,
        "details": details or {}
    }
    
    logger.info("Agent action", extra=log_data)


def log_crew_execution(crew_name: str, status: str, metrics: Optional[dict] = None) -> None:
    """
    Log crew execution status and metrics.
    
    Args:
        crew_name: Name of the crew
        status: Execution status (started, completed, failed, etc.)
        metrics: Execution metrics (duration, tasks completed, etc.)
    """
    logger = get_logger("agentic.crews")
    
    log_data = {
        "crew": crew_name,
        "status": status,
        "metrics": metrics or {}
    }
    
    if status == "failed":
        logger.error("Crew execution", extra=log_data)
    else:
        logger.info("Crew execution", extra=log_data)


def log_task_progress(task_name: str, progress: float, details: Optional[str] = None) -> None:
    """
    Log task progress.
    
    Args:
        task_name: Name of the task
        progress: Progress percentage (0.0 to 1.0)
        details: Additional progress details
    """
    logger = get_logger("agentic.tasks")
    
    log_data = {
        "task": task_name,
        "progress": progress,
        "details": details
    }
    
    logger.debug("Task progress", extra=log_data)


# Initialize logging when module is imported
setup_logging()