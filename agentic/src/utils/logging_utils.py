"""
Enhanced logging utilities for AI Portfolio project.
"""

import logging
import logging.config
import os
import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime


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
        # Use default config path
        config_path = Path("agentic/configs/logging.yaml")
    
    config_path = Path(config_path)
    
    if config_path.exists() and config_path.suffix.lower() == '.yaml':
        import yaml
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        # Fallback to basic configuration
        logging.basicConfig(
            level=default_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(logs_dir / "ai_portfolio.log")
            ]
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


def log_agent_action(agent_name: str, action: str, details: Optional[Dict[str, Any]] = None) -> None:
    """
    Log agent actions with structured data.
    
    Args:
        agent_name: Name of the agent
        action: Action being performed
        details: Additional details about the action
    """
    logger = get_logger("agentic.agents")
    
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "agent": agent_name,
        "action": action,
        "details": details or {}
    }
    
    logger.info(f"Agent {agent_name} - {action}", extra=log_data)


def log_crew_execution(crew_name: str, status: str, metrics: Optional[Dict[str, Any]] = None) -> None:
    """
    Log crew execution status and metrics.
    
    Args:
        crew_name: Name of the crew
        status: Execution status (started, completed, failed, etc.)
        metrics: Execution metrics (duration, tasks completed, etc.)
    """
    logger = get_logger("agentic.crews")
    
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "crew": crew_name,
        "status": status,
        "metrics": metrics or {}
    }
    
    if status == "failed":
        logger.error(f"Crew {crew_name} - {status}", extra=log_data)
    else:
        logger.info(f"Crew {crew_name} - {status}", extra=log_data)


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
        "timestamp": datetime.now().isoformat(),
        "task": task_name,
        "progress": progress,
        "details": details
    }
    
    logger.debug(f"Task {task_name} - {progress:.1%}", extra=log_data)


def log_performance_metrics(component: str, metrics: Dict[str, Any]) -> None:
    """
    Log performance metrics.
    
    Args:
        component: Component name (agent, crew, task, etc.)
        metrics: Performance metrics dictionary
    """
    logger = get_logger("performance")
    
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "component": component,
        "metrics": metrics
    }
    
    logger.info(f"Performance metrics for {component}", extra=log_data)


class StructuredLogger:
    """Structured logger for better log analysis."""
    
    def __init__(self, name: str):
        """
        Initialize structured logger.
        
        Args:
            name: Logger name
        """
        self.logger = get_logger(name)
        self.name = name
    
    def log_event(
        self,
        event_type: str,
        message: str,
        level: int = logging.INFO,
        **kwargs
    ) -> None:
        """
        Log a structured event.
        
        Args:
            event_type: Type of event
            message: Log message
            level: Log level
            **kwargs: Additional structured data
        """
        extra_data = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "logger_name": self.name,
            **kwargs
        }
        
        self.logger.log(level, message, extra=extra_data)
    
    def log_agent_event(self, agent_name: str, event: str, **kwargs) -> None:
        """Log an agent-specific event."""
        self.log_event("agent", f"Agent {agent_name}: {event}", agent=agent_name, **kwargs)
    
    def log_crew_event(self, crew_name: str, event: str, **kwargs) -> None:
        """Log a crew-specific event."""
        self.log_event("crew", f"Crew {crew_name}: {event}", crew=crew_name, **kwargs)
    
    def log_task_event(self, task_name: str, event: str, **kwargs) -> None:
        """Log a task-specific event."""
        self.log_event("task", f"Task {task_name}: {event}", task=task_name, **kwargs)
    
    def log_error(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> None:
        """
        Log an error with context.
        
        Args:
            error: Exception that occurred
            context: Additional context about the error
        """
        self.log_event(
            "error",
            f"Error occurred: {str(error)}",
            level=logging.ERROR,
            error_type=type(error).__name__,
            error_message=str(error),
            context=context or {}
        )


# Global structured logger instance
def get_structured_logger(name: str) -> StructuredLogger:
    """
    Get a structured logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        StructuredLogger instance
    """
    return StructuredLogger(name)