#!/usr/bin/env python3
"""
Simple Research Crew Example

A basic CrewAI implementation demonstrating:
- Research agent for gathering information
- Writer agent for creating content
- Sequential task execution
"""

import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, FileWriterTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize tools
search_tool = SerperDevTool()
file_writer = FileWriterTool()

# Define agents
researcher = Agent(
    role='Research Specialist',
    goal='Conduct thorough research on given topics and gather accurate information',
    backstory="""You are an experienced researcher with a keen eye for detail.
    You excel at finding reliable sources and extracting key insights from complex information.
    Your research forms the foundation for high-quality content creation.""",
    tools=[search_tool],
    verbose=True,
    allow_delegation=False
)

writer = Agent(
    role='Content Writer',
    goal='Create engaging and informative content based on research findings',
    backstory="""You are a skilled writer who transforms research into compelling narratives.
    You have a talent for making complex topics accessible and engaging for various audiences.
    Your writing is clear, well-structured, and factually accurate.""",
    tools=[file_writer],
    verbose=True,
    allow_delegation=False
)

# Define tasks
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

# Create and run the crew
def run_research_crew(topic: str):
    """Run the research crew for a given topic."""
    
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        process=Process.sequential,
        verbose=True
    )
    
    result = crew.kickoff(inputs={'topic': topic})
    return result

if __name__ == "__main__":
    # Example usage
    topic = "Artificial Intelligence in Healthcare"
    print(f"Starting research crew for topic: {topic}")
    
    result = run_research_crew(topic)
    print("\n" + "="*50)
    print("CREW EXECUTION COMPLETED")
    print("="*50)
    print(result)