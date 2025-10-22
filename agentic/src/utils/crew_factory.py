"""
CrewAI factory for creating and managing different crew configurations.
"""

from typing import Dict, Any, List, Optional, Type
from crewai import Crew, Agent, Task, Process
from crewai_tools import SerperDevTool, FileReaderTool, FileWriterTool

from ..config.settings import Settings
from ..agents.base_agent import BaseAgent, AgentConfig
from .logging_utils import get_logger


class CrewFactory:
    """Factory for creating CrewAI crews with standardized configurations."""
    
    def __init__(self, settings: Settings):
        """
        Initialize the crew factory.
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.logger = get_logger("crew_factory")
        
        # Initialize common tools
        self.common_tools = {
            "search": SerperDevTool(),
            "file_reader": FileReaderTool(),
            "file_writer": FileWriterTool(),
        }
    
    def create_crew(
        self,
        crew_type: str,
        config_override: Optional[Dict[str, Any]] = None
    ) -> Crew:
        """
        Create a crew of the specified type.
        
        Args:
            crew_type: Type of crew to create
            config_override: Optional configuration overrides
            
        Returns:
            Configured Crew instance
        """
        self.logger.info(f"Creating crew of type: {crew_type}")
        
        config = config_override or {}
        
        if crew_type == "research":
            return self._create_research_crew(config)
        elif crew_type == "content_analysis":
            return self._create_content_analysis_crew(config)
        elif crew_type == "creative_writing":
            return self._create_creative_writing_crew(config)
        elif crew_type == "data_analysis":
            return self._create_data_analysis_crew(config)
        elif crew_type == "social_media":
            return self._create_social_media_crew(config)
        else:
            raise ValueError(f"Unknown crew type: {crew_type}")
    
    def _create_research_crew(self, config: Dict[str, Any]) -> Crew:
        """Create a research crew."""
        # Create agents
        researcher = Agent(
            role="Research Specialist",
            goal="Conduct thorough research on given topics and gather accurate information",
            backstory="""You are an experienced researcher with a keen eye for detail.
            You excel at finding reliable sources and extracting key insights from complex information.
            Your research forms the foundation for high-quality content creation.""",
            tools=[self.common_tools["search"]],
            verbose=config.get("verbose", self.settings.crew.verbose),
            allow_delegation=False
        )
        
        writer = Agent(
            role="Content Writer",
            goal="Create engaging and informative content based on research findings",
            backstory="""You are a skilled writer who transforms research into compelling narratives.
            You have a talent for making complex topics accessible and engaging for various audiences.
            Your writing is clear, well-structured, and factually accurate.""",
            tools=[self.common_tools["file_writer"]],
            verbose=config.get("verbose", self.settings.crew.verbose),
            allow_delegation=False
        )
        
        # Create tasks
        research_task = Task(
            description="""Research the topic: {topic}
            
            Focus on:
            - Key concepts and definitions
            - Recent developments and trends
            - Important statistics or data points
            - Expert opinions and perspectives
            
            Provide a comprehensive research summary with sources.""",
            agent=researcher,
            expected_output="A detailed research summary with key findings and source references"
        )
        
        writing_task = Task(
            description="""Using the research findings, write a comprehensive article about {topic}.
            
            The article should:
            - Be 800-1200 words long
            - Include an engaging introduction
            - Cover all key points from the research
            - Have a clear structure with headings
            - End with a meaningful conclusion
            
            Save the article to a file named '{topic}_article.md'""",
            agent=writer,
            expected_output="A well-written article saved to a markdown file",
            context=[research_task]
        )
        
        return Crew(
            agents=[researcher, writer],
            tasks=[research_task, writing_task],
            process=Process.sequential,
            verbose=config.get("verbose", self.settings.crew.verbose),
            memory=config.get("memory", self.settings.crew.memory_enabled)
        )
    
    def _create_content_analysis_crew(self, config: Dict[str, Any]) -> Crew:
        """Create a content analysis crew."""
        # Create agents
        analyzer = Agent(
            role="Content Analyst",
            goal="Analyze text content for themes, sentiment, and key insights",
            backstory="""You are an expert content analyst with deep expertise in natural language processing.
            You excel at identifying patterns, themes, and sentiment in written content.
            Your analyses provide valuable insights for content strategy and optimization.""",
            tools=[self.common_tools["file_reader"]],
            verbose=config.get("verbose", self.settings.crew.verbose),
            allow_delegation=False
        )
        
        data_scientist = Agent(
            role="Data Scientist",
            goal="Perform statistical analysis and extract quantitative insights",
            backstory="""You are a data scientist specializing in text analytics and metrics.
            You transform qualitative content analysis into actionable quantitative insights.
            Your statistical approach provides objective measurements and trends.""",
            tools=[],
            verbose=config.get("verbose", self.settings.crew.verbose),
            allow_delegation=False
        )
        
        report_writer = Agent(
            role="Report Writer",
            goal="Create comprehensive analysis reports with actionable recommendations",
            backstory="""You are a professional report writer who specializes in business intelligence.
            You transform complex analysis into clear, actionable business recommendations.
            Your reports drive strategic decision-making and content optimization.""",
            tools=[self.common_tools["file_writer"]],
            verbose=config.get("verbose", self.settings.crew.verbose),
            allow_delegation=False
        )
        
        # Create tasks
        analysis_task = Task(
            description="""Analyze the content in the file: {content_file}
            
            Perform comprehensive analysis including:
            - Main themes and topics identification
            - Sentiment analysis (positive, negative, neutral)
            - Key message extraction
            - Writing style assessment
            - Target audience identification
            - Content structure evaluation
            
            Provide detailed findings with specific examples from the text.""",
            agent=analyzer,
            expected_output="Detailed content analysis with themes, sentiment, and key insights"
        )
        
        statistical_task = Task(
            description="""Based on the content analysis, perform statistical evaluation:
            
            Calculate and analyze:
            - Word count and readability metrics
            - Sentence structure patterns
            - Keyword density and frequency
            - Sentiment score distribution
            - Content complexity metrics
            - Engagement potential indicators
            
            Provide quantitative metrics and statistical insights.""",
            agent=data_scientist,
            expected_output="Statistical analysis with metrics and quantitative insights",
            context=[analysis_task]
        )
        
        report_task = Task(
            description="""Create a comprehensive content analysis report based on previous findings.
            
            The report should include:
            - Executive summary of key findings
            - Detailed analysis results
            - Statistical metrics and trends
            - Content strengths and weaknesses
            - Actionable recommendations for improvement
            - Conclusion with strategic insights
            
            Save the report as '{content_file}_analysis_report.md'""",
            agent=report_writer,
            expected_output="Professional analysis report saved to markdown file",
            context=[analysis_task, statistical_task]
        )
        
        return Crew(
            agents=[analyzer, data_scientist, report_writer],
            tasks=[analysis_task, statistical_task, report_task],
            process=Process.sequential,
            verbose=config.get("verbose", self.settings.crew.verbose),
            memory=config.get("memory", self.settings.crew.memory_enabled)
        )
    
    def _create_creative_writing_crew(self, config: Dict[str, Any]) -> Crew:
        """Create a creative writing crew."""
        # Create agents
        planner = Agent(
            role="Story Planner",
            goal="Develop compelling story structures, characters, and plot outlines",
            backstory="""You are a master storyteller with expertise in narrative structure and character development.
            You create detailed outlines that serve as blueprints for engaging stories.
            Your planning ensures stories have strong arcs, memorable characters, and satisfying conclusions.""",
            tools=[],
            verbose=config.get("verbose", self.settings.crew.verbose),
            allow_delegation=False
        )
        
        writer = Agent(
            role="Creative Writer",
            goal="Transform story plans into engaging, well-written narratives",
            backstory="""You are a talented creative writer with a gift for bringing stories to life.
            You excel at dialogue, descriptive prose, and maintaining reader engagement.
            Your writing style adapts to different genres while maintaining quality and authenticity.""",
            tools=[self.common_tools["file_writer"]],
            verbose=config.get("verbose", self.settings.crew.verbose),
            allow_delegation=False
        )
        
        editor = Agent(
            role="Editor",
            goal="Refine and polish written content for maximum impact and readability",
            backstory="""You are an experienced editor with a keen eye for detail and flow.
            You enhance clarity, fix inconsistencies, and ensure the narrative maintains its intended tone.
            Your editing transforms good writing into exceptional storytelling.""",
            tools=[self.common_tools["file_writer"]],
            verbose=config.get("verbose", self.settings.crew.verbose),
            allow_delegation=False
        )
        
        # Create tasks
        planning_task = Task(
            description="""Create a detailed story plan for: {story_prompt}
            
            Develop:
            - Main character profiles with motivations and backgrounds
            - Plot structure with beginning, middle, and end
            - Key scenes and story beats
            - Setting and world-building elements
            - Conflict and resolution framework
            - Themes and underlying messages
            
            Genre: {genre}
            Target length: {target_length} words
            
            Provide a comprehensive story outline ready for writing.""",
            agent=planner,
            expected_output="Detailed story plan with characters, plot structure, and key scenes"
        )
        
        writing_task = Task(
            description="""Using the story plan, write the complete story.
            
            Requirements:
            - Follow the planned structure and character development
            - Write approximately {target_length} words
            - Maintain consistent tone and style for {genre} genre
            - Include engaging dialogue and vivid descriptions
            - Ensure proper pacing and narrative flow
            - Create compelling opening and satisfying conclusion
            
            Save the story as '{story_title}.md'""",
            agent=writer,
            expected_output="Complete story written and saved to file",
            context=[planning_task]
        )
        
        editing_task = Task(
            description="""Edit and refine the written story for publication quality.
            
            Focus on:
            - Grammar, punctuation, and spelling corrections
            - Sentence structure and flow improvements
            - Character consistency and development
            - Plot coherence and pacing
            - Dialogue naturalness and effectiveness
            - Overall readability and engagement
            
            Save the edited version as '{story_title}_final.md'""",
            agent=editor,
            expected_output="Polished, publication-ready story saved to file",
            context=[writing_task]
        )
        
        return Crew(
            agents=[planner, writer, editor],
            tasks=[planning_task, writing_task, editing_task],
            process=Process.sequential,
            verbose=config.get("verbose", self.settings.crew.verbose),
            memory=config.get("memory", self.settings.crew.memory_enabled)
        )
    
    def _create_data_analysis_crew(self, config: Dict[str, Any]) -> Crew:
        """Create a data analysis crew (placeholder implementation)."""
        # This would contain data analysis specific agents and tasks
        # Implementation depends on specific data analysis requirements
        raise NotImplementedError("Data analysis crew not yet implemented")
    
    def _create_social_media_crew(self, config: Dict[str, Any]) -> Crew:
        """Create a social media crew (placeholder implementation)."""
        # This would contain social media specific agents and tasks
        # Implementation depends on specific social media requirements
        raise NotImplementedError("Social media crew not yet implemented")
    
    def list_available_crews(self) -> List[str]:
        """
        Get list of available crew types.
        
        Returns:
            List of crew type names
        """
        return ["research", "content_analysis", "creative_writing"]
    
    def get_crew_description(self, crew_type: str) -> str:
        """
        Get description for a crew type.
        
        Args:
            crew_type: Type of crew
            
        Returns:
            Description of the crew
        """
        descriptions = {
            "research": "Research crew for information gathering and analysis",
            "content_analysis": "Content analysis crew for text evaluation and insights",
            "creative_writing": "Creative writing crew for story generation and editing",
            "data_analysis": "Data analysis crew for statistical insights (coming soon)",
            "social_media": "Social media crew for content creation (coming soon)"
        }
        
        return descriptions.get(crew_type, "Unknown crew type")