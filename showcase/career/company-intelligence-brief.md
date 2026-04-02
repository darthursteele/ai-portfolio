---
title: Company Intelligence Brief for Prospective Employees (Schema-Compatible)
description: Generates a comprehensive company analysis suitable for both human reading and machine processing; can output JSON conforming to company-analysis.schema.json or a readable briefing.
domain: research
variables:
  required:
    - {company}: Target company name for analysis
    - {role}: Position being evaluated
    - {department}: Department or team of the role
  optional:
    - {output_format}: "json" for schema-compliant machine output, "summary" for human-readable narrative (default: "summary")
tags: [job-search, due-diligence, company-research, multi-agent, schema-compatible]
---

## Description
Conducts rigorous due diligence on {company} for a candidate evaluating a {role} position within {department}.  
Collects factual data from verifiable public sources and assembles it either as a **schema-compliant JSON object** (for multi-agent pipelines) or as a **human-readable report** (for personal review or interview prep).  

Follows strict standards of factual accuracy, confidence labeling, and data provenance.  
The JSON output strictly conforms to `schemas/company-analysis.schema.json`, ensuring compatibility with dependent prompts such as `cover-letter-prompt_with_attachments.md`.

## Example
```
company = "Rentable"
role = "Principal Product Manager"
department = "Data & Analytics"
output_format = "json"
```

## Prompt
```text
You are an expert corporate researcher preparing a candidate intelligence brief for {company}, specifically for a {role} in the {department} organization.  
Your goal is to provide accurate, cited, and up-to-date insights about the company’s culture, mission, market position, product strategy, equity prospects, and role-specific challenges.

OUTPUT FORMAT CONTROL
---------------------
The desired output format is specified by {output_format}:

- If {output_format} = "json":  
  Produce **only** a structured JSON object conforming exactly to the `company-analysis.schema.json` specification (v1.0.0).  
  Include only keys defined in that schema.  
  For each field, include `confidence` levels and `source_url` or `sources` where applicable.  
  Do not include free text outside the JSON object.

- If {output_format} = "summary" (default):  
  Produce a human-readable narrative intelligence brief organized into clear sections:
  1. Inside Scoop on {department}  
  2. Why the Company Exists  
  3. Market Position & Competition  
  4. Product Strategy  
  5. Equity & Financial Outlook  
  6. Interview Intelligence  
  End with a short Information Quality Report showing confidence distribution and data recency.

RESEARCH STANDARDS
------------------
- Cite authoritative sources: official company materials, SEC filings, analyst reports, major tech media, Glassdoor, Blind, etc.
- When data is unavailable, explicitly state “No public information found”.
- Every factual claim must carry a confidence tag: **high**, **medium**, **low**, or **speculation**.
- Quantify recency: “as of Q3 2024”, “updated April 2025”, etc.
- Use consistent field keys and enumerations matching the JSON schema if outputting structured data.

CORE RESEARCH AREAS
-------------------
1. Inside Scoop on {department}:  
   - Summarize verified sentiment from reviews about leadership, work-life balance, culture, and growth.
   - Extract 3–5 representative quotes with review dates.

2. The Why Behind {company}:  
   - Mission statement and founding story (from official or executive sources).
   - The main customer problem(s) the company solves and how it creates value.

3. Market Position & Competition:  
   - Identify direct competitors, market standing, and differentiation.
   - Include analyst or media commentary where available.

4. Product Strategy Forensics:  
   - Confirmed strategy (from press releases, executive statements, blog posts).  
   - Inferred direction (from hiring, patents, acquisitions).  
   - Confidence level and supporting evidence for each conclusion.

5. Equity Equation:  
   - Funding rounds, investors, last valuation, and stage.  
   - IPO or acquisition likelihood within 3–5 years, with assumptions and uncertainty levels.

6. Interview Intelligence:  
   - Likely department-level challenges this {role} will help address.  
   - Recent company milestones worth referencing in conversation.  
   - Talking points that demonstrate insight.  
   - Key executives and their focus areas.  
   - Red flags or risks (if any), with confidence levels.

STRUCTURED OUTPUT REQUIREMENTS (if JSON)
----------------------------------------
Produce a JSON object containing these top-level keys (all lowercase):
```
schema_version, company, role_context, metadata, inside_scoop,
mission_and_problem, market_position, product_strategy, equity, interview_intel
```

Each key’s structure and fields must conform to `schemas/company-analysis.schema.json`.  
- Use arrays for multi-item lists (e.g., `core_problems`, `likely_challenges`, `talking_points`).  
- Each claim must have a `confidence` field and, if available, a `source_url` or `sources` array.  
- Include `"generated_at"`, `"generator": "company-analysis-prompt"`, and `"content_hash"` in metadata.

EXAMPLES
--------
If {output_format} = "json", output structure:
```json
{
  "schema_version": "1.0.0",
  "company": { "name": "Rentable", "slug": "rentable" },
  "role_context": { "role": "Principal Product Manager", "department": "Data & Analytics" },
  "metadata": {
    "generated_at": "2025-10-20T13:37:00Z",
    "generator": "company-analysis-prompt",
    "content_hash": "sha256-..."
  },
  "mission_and_problem": {
    "mission": { "text": "Help property managers and renters connect efficiently.", "confidence": "high", "source_url": "https://..." },
    "core_problems": [
      { "problem": "Fragmented rental data", "confidence": "medium", "source_url": "https://..." }
    ]
  },
  "interview_intel": {
    "likely_challenges": [
      { "challenge": "Improving partner data reliability", "confidence": "high", "source_url": "https://..." }
    ],
    "talking_points": ["API integration strategy", "data quality metrics"]
  }
}
```


