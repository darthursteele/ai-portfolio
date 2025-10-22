#!/usr/bin/env python3
"""
Main orchestration script for AI Portfolio CrewAI applications.

This script provides a command-line interface for running different
crew configurations and managing agent workflows.
"""

import argparse
import asyncio
import sys
import time
from pathlib import Path
from typing import Dict, Any, Optional

from src.config.settings import Settings
from src.utils.logging_utils import setup_logging, get_logger, log_crew_execution
from src.utils.crew_factory import CrewFactory
from src.utils.performance_monitor import PerformanceMonitor


class CrewOrchestrator:
    """Main orchestrator for managing CrewAI workflows."""
    
    def __init__(self, settings: Optional[Settings] = None):
        """
        Initialize the orchestrator.
        
        Args:
            settings: Application settings
        """
        self.settings = settings or Settings()
        self.logger = get_logger("orchestrator")
        self.crew_factory = CrewFactory(self.settings)
        self.performance_monitor = PerformanceMonitor()
        
        # Setup logging
        setup_logging()
        
        self.logger.info("CrewAI Orchestrator initialized")
    
    def list_available_crews(self) -> Dict[str, str]:
        """
        Get list of available crew configurations.
        
        Returns:
            Dictionary mapping crew names to descriptions
        """
        return {
            "research": "Research crew for information gathering and analysis",
            "content_analysis": "Content analysis crew for text evaluation",
            "creative_writing": "Creative writing crew for story generation",
            "data_analysis": "Data analysis crew for statistical insights",
            "social_media": "Social media crew for content creation and management"
        }
    
    def run_crew(
        self,
        crew_name: str,
        inputs: Dict[str, Any],
        config_override: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Run a specific crew with given inputs.
        
        Args:
            crew_name: Name of the crew to run
            inputs: Input parameters for the crew
            config_override: Optional configuration overrides
            
        Returns:
            Results from crew execution
        """
        self.logger.info(f"Starting crew execution: {crew_name}")
        log_crew_execution(crew_name, "started")
        
        start_time = time.time()
        
        try:
            # Create crew
            crew = self.crew_factory.create_crew(crew_name, config_override)
            
            # Start performance monitoring
            self.performance_monitor.start_monitoring(crew_name)
            
            # Execute crew
            self.logger.info(f"Executing crew {crew_name} with inputs: {list(inputs.keys())}")
            result = crew.kickoff(inputs=inputs)
            
            # Calculate execution time
            execution_time = time.time() - start_time
            
            # Log success
            metrics = {
                "execution_time": execution_time,
                "tasks_completed": len(crew.tasks),
                "agents_used": len(crew.agents)
            }
            
            log_crew_execution(crew_name, "completed", metrics)
            self.logger.info(f"Crew {crew_name} completed successfully in {execution_time:.2f}s")
            
            # Stop monitoring and get metrics
            performance_metrics = self.performance_monitor.stop_monitoring(crew_name)
            
            return {
                "result": result,
                "execution_time": execution_time,
                "metrics": metrics,
                "performance": performance_metrics,
                "status": "success"
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_details = {
                "error": str(e),
                "execution_time": execution_time,
                "error_type": type(e).__name__
            }
            
            log_crew_execution(crew_name, "failed", error_details)
            self.logger.error(f"Crew {crew_name} failed: {e}", exc_info=True)
            
            return {
                "result": None,
                "execution_time": execution_time,
                "error": str(e),
                "status": "failed"
            }
    
    async def run_crew_async(
        self,
        crew_name: str,
        inputs: Dict[str, Any],
        config_override: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Run a crew asynchronously.
        
        Args:
            crew_name: Name of the crew to run
            inputs: Input parameters for the crew
            config_override: Optional configuration overrides
            
        Returns:
            Results from crew execution
        """
        # Run in thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, 
            self.run_crew, 
            crew_name, 
            inputs, 
            config_override
        )
    
    def run_batch_crews(
        self,
        crew_configs: list[Dict[str, Any]]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Run multiple crews in sequence.
        
        Args:
            crew_configs: List of crew configurations
            
        Returns:
            Dictionary mapping crew names to results
        """
        results = {}
        
        for config in crew_configs:
            crew_name = config["name"]
            inputs = config["inputs"]
            config_override = config.get("config_override")
            
            self.logger.info(f"Running batch crew: {crew_name}")
            result = self.run_crew(crew_name, inputs, config_override)
            results[crew_name] = result
            
            # Short delay between crews
            time.sleep(1)
        
        return results
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get current system status and performance metrics.
        
        Returns:
            System status information
        """
        return {
            "orchestrator_status": "running",
            "settings": self.settings.model_dump(),
            "available_crews": list(self.list_available_crews().keys()),
            "performance_metrics": self.performance_monitor.get_global_metrics(),
            "uptime": time.time() - getattr(self, '_start_time', time.time())
        }


def main():
    """Main entry point for the orchestrator."""
    parser = argparse.ArgumentParser(description="AI Portfolio CrewAI Orchestrator")
    parser.add_argument("--crew", type=str, help="Name of the crew to run")
    parser.add_argument("--list-crews", action="store_true", help="List available crews")
    parser.add_argument("--config", type=str, help="Path to configuration file")
    parser.add_argument("--input-file", type=str, help="Path to input JSON file")
    parser.add_argument("--output-file", type=str, help="Path to output file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    parser.add_argument("--async", action="store_true", help="Run crew asynchronously")
    
    # Specific crew arguments
    parser.add_argument("--topic", type=str, help="Topic for research crew")
    parser.add_argument("--content-file", type=str, help="Content file for analysis crew")
    parser.add_argument("--story-prompt", type=str, help="Story prompt for creative writing crew")
    
    args = parser.parse_args()
    
    # Initialize orchestrator
    settings = Settings()
    if args.config:
        settings = Settings.from_file(args.config)
    
    orchestrator = CrewOrchestrator(settings)
    orchestrator._start_time = time.time()
    
    # List crews if requested
    if args.list_crews:
        crews = orchestrator.list_available_crews()
        print("Available crews:")
        for name, description in crews.items():
            print(f"  {name}: {description}")
        return
    
    # Run specific crew
    if args.crew:
        # Prepare inputs based on crew type and arguments
        inputs = {}
        
        if args.crew == "research" and args.topic:
            inputs = {"topic": args.topic}
        elif args.crew == "content_analysis" and args.content_file:
            inputs = {"content_file": args.content_file}
        elif args.crew == "creative_writing" and args.story_prompt:
            inputs = {
                "story_prompt": args.story_prompt,
                "genre": "fiction",
                "target_length": 1500,
                "story_title": "generated_story"
            }
        
        # Load inputs from file if specified
        if args.input_file:
            import json
            with open(args.input_file, 'r') as f:
                file_inputs = json.load(f)
                inputs.update(file_inputs)
        
        if not inputs:
            print(f"No inputs provided for crew '{args.crew}'. Use --help for options.")
            sys.exit(1)
        
        # Run crew
        if args.async:
            async def run_async():
                return await orchestrator.run_crew_async(args.crew, inputs)
            
            result = asyncio.run(run_async())
        else:
            result = orchestrator.run_crew(args.crew, inputs)
        
        # Output results
        if args.output_file:
            import json
            with open(args.output_file, 'w') as f:
                json.dump(result, f, indent=2, default=str)
            print(f"Results saved to {args.output_file}")
        else:
            print("Execution completed:")
            print(f"Status: {result['status']}")
            print(f"Execution time: {result['execution_time']:.2f}s")
            if result['status'] == 'success':
                print("Result: Success")
            else:
                print(f"Error: {result.get('error', 'Unknown error')}")
    
    else:
        # Interactive mode
        print("AI Portfolio CrewAI Orchestrator")
        print("Use --help for command line options")
        print("Available crews:")
        crews = orchestrator.list_available_crews()
        for name, description in crews.items():
            print(f"  {name}: {description}")


if __name__ == "__main__":
    main()