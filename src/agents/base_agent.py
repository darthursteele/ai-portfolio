"""
Base Agent class for CrewAI agents with common functionality.
"""

import logging
from typing import Any, Dict, List, Optional, Union
from abc import ABC, abstractmethod
from crewai import Agent
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from ..config.settings import Settings
from ..utils.logging_utils import get_logger, log_agent_action


class AgentConfig(BaseModel):
    """Configuration model for agents."""
    
    role: str = Field(..., description="The role of the agent")
    goal: str = Field(..., description="The goal of the agent")
    backstory: str = Field(..., description="The backstory of the agent")
    verbose: bool = Field(default=True, description="Whether to enable verbose logging")
    allow_delegation: bool = Field(default=False, description="Whether to allow delegation")
    max_iter: int = Field(default=5, description="Maximum iterations for agent execution")
    memory: bool = Field(default=True, description="Whether to enable memory")
    max_execution_time: Optional[int] = Field(default=None, description="Maximum execution time in seconds")
    system_template: Optional[str] = Field(default=None, description="Custom system template")
    prompt_template: Optional[str] = Field(default=None, description="Custom prompt template")


class BaseAgent(ABC):
    """
    Base class for all CrewAI agents with common functionality.
    
    This class provides:
    - Standardized configuration management
    - Logging integration
    - Error handling
    - Performance monitoring
    - Tool management
    """
    
    def __init__(
        self,
        config: Union[AgentConfig, Dict[str, Any]],
        tools: Optional[List[BaseTool]] = None,
        settings: Optional[Settings] = None
    ):
        """
        Initialize the base agent.
        
        Args:
            config: Agent configuration (AgentConfig or dict)
            tools: List of tools available to the agent
            settings: Application settings
        """
        # Convert dict to AgentConfig if needed
        if isinstance(config, dict):
            config = AgentConfig(**config)
        
        self.config = config
        self.tools = tools or []
        self.settings = settings or Settings()
        self.logger = get_logger(f"agents.{self.__class__.__name__}")
        
        # Initialize CrewAI agent
        self._agent = self._create_crewai_agent()
        
        # Performance tracking
        self.execution_count = 0
        self.total_execution_time = 0.0
        
        self.logger.info(f"Initialized {self.__class__.__name__} agent with role: {config.role}")
    
    def _create_crewai_agent(self) -> Agent:
        """Create the underlying CrewAI agent."""
        agent_kwargs = {
            "role": self.config.role,
            "goal": self.config.goal,
            "backstory": self.config.backstory,
            "tools": self.tools,
            "verbose": self.config.verbose,
            "allow_delegation": self.config.allow_delegation,
            "max_iter": self.config.max_iter,
            "memory": self.config.memory,
        }
        
        # Add optional parameters if they exist
        if self.config.max_execution_time:
            agent_kwargs["max_execution_time"] = self.config.max_execution_time
        if self.config.system_template:
            agent_kwargs["system_template"] = self.config.system_template
        if self.config.prompt_template:
            agent_kwargs["prompt_template"] = self.config.prompt_template
        
        return Agent(**agent_kwargs)
    
    @property
    def agent(self) -> Agent:
        """Get the underlying CrewAI agent."""
        return self._agent
    
    @property
    def name(self) -> str:
        """Get the agent name (class name)."""
        return self.__class__.__name__
    
    @property
    def role(self) -> str:
        """Get the agent role."""
        return self.config.role
    
    def add_tool(self, tool: BaseTool) -> None:
        """
        Add a tool to the agent.
        
        Args:
            tool: Tool to add
        """
        self.tools.append(tool)
        self._agent.tools = self.tools
        self.logger.info(f"Added tool {tool.__class__.__name__} to agent {self.name}")
    
    def remove_tool(self, tool_name: str) -> bool:
        """
        Remove a tool from the agent by name.
        
        Args:
            tool_name: Name of the tool to remove
            
        Returns:
            True if tool was removed, False if not found
        """
        for i, tool in enumerate(self.tools):
            if tool.__class__.__name__ == tool_name:
                removed_tool = self.tools.pop(i)
                self._agent.tools = self.tools
                self.logger.info(f"Removed tool {removed_tool.__class__.__name__} from agent {self.name}")
                return True
        return False
    
    def get_tool(self, tool_name: str) -> Optional[BaseTool]:
        """
        Get a tool by name.
        
        Args:
            tool_name: Name of the tool to get
            
        Returns:
            Tool instance if found, None otherwise
        """
        for tool in self.tools:
            if tool.__class__.__name__ == tool_name:
                return tool
        return None
    
    def log_action(self, action: str, details: Optional[Dict[str, Any]] = None) -> None:
        """
        Log an agent action.
        
        Args:
            action: Action being performed
            details: Additional details about the action
        """
        log_agent_action(self.name, action, details)
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """
        Get performance metrics for the agent.
        
        Returns:
            Dictionary containing performance metrics
        """
        avg_execution_time = (
            self.total_execution_time / self.execution_count 
            if self.execution_count > 0 else 0
        )
        
        return {
            "execution_count": self.execution_count,
            "total_execution_time": self.total_execution_time,
            "average_execution_time": avg_execution_time,
            "tools_count": len(self.tools),
            "agent_name": self.name,
            "agent_role": self.role
        }
    
    @abstractmethod
    def get_specialized_config(self) -> Dict[str, Any]:
        """
        Get specialized configuration for this agent type.
        
        Returns:
            Dictionary containing agent-specific configuration
        """
        pass
    
    def validate_config(self) -> bool:
        """
        Validate the agent configuration.
        
        Returns:
            True if configuration is valid
            
        Raises:
            ValueError: If configuration is invalid
        """
        if not self.config.role.strip():
            raise ValueError("Agent role cannot be empty")
        
        if not self.config.goal.strip():
            raise ValueError("Agent goal cannot be empty")
        
        if not self.config.backstory.strip():
            raise ValueError("Agent backstory cannot be empty")
        
        if self.config.max_iter <= 0:
            raise ValueError("max_iter must be greater than 0")
        
        return True
    
    def reset_performance_metrics(self) -> None:
        """Reset performance tracking metrics."""
        self.execution_count = 0
        self.total_execution_time = 0.0
        self.logger.info(f"Reset performance metrics for agent {self.name}")
    
    def __str__(self) -> str:
        """String representation of the agent."""
        return f"{self.__class__.__name__}(role='{self.config.role}', tools={len(self.tools)})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the agent."""
        return (
            f"{self.__class__.__name__}("
            f"role='{self.config.role}', "
            f"goal='{self.config.goal[:50]}...', "
            f"tools={len(self.tools)}, "
            f"executions={self.execution_count}"
            f")"
        )