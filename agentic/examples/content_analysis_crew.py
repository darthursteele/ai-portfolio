#!/usr/bin/env python3
"""
Content Analysis Crew Example

A specialized CrewAI implementation for content analysis featuring:
- Content analyzer for extracting insights
- Data scientist for statistical analysis
- Report generator for comprehensive reporting
"""

import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import FileReaderTool, FileWriterTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize tools
file_reader = FileReaderTool()
file_writer = FileWriterTool()

# Define agents
content_analyzer = Agent(
    role='Content Analyst',
    goal='Analyze text content for themes, sentiment, and key insights',
    backstory="""You are an expert content analyst with deep expertise in natural language processing.
    You excel at identifying patterns, themes, and sentiment in written content.
    Your analyses provide valuable insights for content strategy and optimization.""",
    tools=[file_reader],
    verbose=True,
    allow_delegation=False
)

data_scientist = Agent(
    role='Data Scientist',
    goal='Perform statistical analysis and extract quantitative insights',
    backstory="""You are a data scientist specializing in text analytics and metrics.
    You transform qualitative content analysis into actionable quantitative insights.
    Your statistical approach provides objective measurements and trends.""",
    tools=[],
    verbose=True,
    allow_delegation=False
)

report_generator = Agent(
    role='Report Writer',
    goal='Create comprehensive analysis reports with actionable recommendations',
    backstory="""You are a professional report writer who specializes in business intelligence.
    You transform complex analysis into clear, actionable business recommendations.
    Your reports drive strategic decision-making and content optimization.""",
    tools=[file_writer],
    verbose=True,
    allow_delegation=False
)

# Define tasks
content_analysis_task = Task(
    description="""Analyze the content in the file: {content_file}
    
    Perform comprehensive analysis including:
    - Main themes and topics identification
    - Sentiment analysis (positive, negative, neutral)
    - Key message extraction
    - Writing style assessment
    - Target audience identification
    - Content structure evaluation
    
    Provide detailed findings with specific examples from the text.""",
    agent=content_analyzer,
    expected_output="Detailed content analysis with themes, sentiment, and key insights"
)

statistical_analysis_task = Task(
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
    context=[content_analysis_task]
)

report_generation_task = Task(
    description="""Create a comprehensive content analysis report based on previous findings.
    
    The report should include:
    - Executive summary of key findings
    - Detailed analysis results
    - Statistical metrics and trends
    - Content strengths and weaknesses
    - Actionable recommendations for improvement
    - Conclusion with strategic insights
    
    Save the report as '{content_file}_analysis_report.md'""",
    agent=report_generator,
    expected_output="Professional analysis report saved to markdown file",
    context=[content_analysis_task, statistical_analysis_task]
)

# Create and run the crew
def run_analysis_crew(content_file: str):
    """Run the content analysis crew for a given file."""
    
    crew = Crew(
        agents=[content_analyzer, data_scientist, report_generator],
        tasks=[content_analysis_task, statistical_analysis_task, report_generation_task],
        process=Process.sequential,
        verbose=True
    )
    
    result = crew.kickoff(inputs={'content_file': content_file})
    return result

if __name__ == "__main__":
    # Example usage
    content_file = "sample_content.txt"
    print(f"Starting content analysis crew for file: {content_file}")
    
    result = run_analysis_crew(content_file)
    print("\n" + "="*50)
    print("CONTENT ANALYSIS COMPLETED")
    print("="*50)
    print(result)