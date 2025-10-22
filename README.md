# AI Portfolio

A collection of AI applications, agentic systems, and prompt engineering work by [@darthursteele](https://github.com/darthursteele).

## Repository Structure

- **`agentic/`** - Complete CrewAI development framework with agents, crews, and utilities
- **`prompts/`** - Curated prompts for various AI tasks and use cases  
- **`experiments/`** - Research experiments and proof-of-concept projects

## Getting Started

### CrewAI Framework
The `agentic/` directory contains a professional CrewAI development environment:

```bash
cd agentic
python main.py --list-crews  # See available crews
python main.py --crew research --topic "AI in Healthcare"  # Run research crew
make help  # See all available commands
```

### Development Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Development setup with Docker
docker-compose up -d

# Run tests
cd agentic && make test
```

## About

This portfolio showcases various AI implementations, from practical applications to experimental research in artificial intelligence and machine learning. The main focus is on CrewAI-based autonomous agent systems with professional development tooling.