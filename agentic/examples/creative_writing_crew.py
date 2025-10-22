#!/usr/bin/env python3
"""
Creative Writing Crew Example

A creative writing team featuring:
- Story planner for plot development
- Creative writer for content creation
- Editor for refinement and polish
"""

import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import FileWriterTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize tools
file_writer = FileWriterTool()

# Define agents
story_planner = Agent(
    role='Story Planner',
    goal='Develop compelling story structures, characters, and plot outlines',
    backstory="""You are a master storyteller with expertise in narrative structure and character development.
    You create detailed outlines that serve as blueprints for engaging stories.
    Your planning ensures stories have strong arcs, memorable characters, and satisfying conclusions.""",
    tools=[],
    verbose=True,
    allow_delegation=False
)

creative_writer = Agent(
    role='Creative Writer',
    goal='Transform story plans into engaging, well-written narratives',
    backstory="""You are a talented creative writer with a gift for bringing stories to life.
    You excel at dialogue, descriptive prose, and maintaining reader engagement.
    Your writing style adapts to different genres while maintaining quality and authenticity.""",
    tools=[file_writer],
    verbose=True,
    allow_delegation=False
)

editor = Agent(
    role='Editor',
    goal='Refine and polish written content for maximum impact and readability',
    backstory="""You are an experienced editor with a keen eye for detail and flow.
    You enhance clarity, fix inconsistencies, and ensure the narrative maintains its intended tone.
    Your editing transforms good writing into exceptional storytelling.""",
    tools=[file_writer],
    verbose=True,
    allow_delegation=False
)

# Define tasks
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
    agent=story_planner,
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
    agent=creative_writer,
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

# Create and run the crew
def run_writing_crew(story_prompt: str, genre: str = "fiction", target_length: int = 1500, story_title: str = "generated_story"):
    """Run the creative writing crew."""
    
    crew = Crew(
        agents=[story_planner, creative_writer, editor],
        tasks=[planning_task, writing_task, editing_task],
        process=Process.sequential,
        verbose=True
    )
    
    inputs = {
        'story_prompt': story_prompt,
        'genre': genre,
        'target_length': target_length,
        'story_title': story_title
    }
    
    result = crew.kickoff(inputs=inputs)
    return result

if __name__ == "__main__":
    # Example usage
    story_prompt = "A time traveler discovers they can only travel to moments of great historical significance, but each trip erases one of their own memories."
    genre = "science fiction"
    target_length = 2000
    story_title = "memory_traveler"
    
    print(f"Starting creative writing crew...")
    print(f"Prompt: {story_prompt}")
    print(f"Genre: {genre}")
    print(f"Target length: {target_length} words")
    
    result = run_writing_crew(story_prompt, genre, target_length, story_title)
    print("\n" + "="*50)
    print("CREATIVE WRITING COMPLETED")
    print("="*50)
    print(result)