# Skills

This directory will contain prompts packaged as deployable Cowork skills — essentially giving each one a trigger description, a SKILL.md wrapper, and surfacing it as a one-click agent rather than a copy-paste template.

The difference between a prompt and a skill: a skill knows when to run, asks the right clarifying questions, and returns a structured output without the user having to think about configuration.

## Conversion Roadmap

| Priority | Skill name | Source prompts | What it does |
|----------|-----------|---------------|--------------|
| 1 | `job-search-pipeline` | `career/company-intelligence-brief` → `career/cover-letter-generator` → `career/expert-resume-optimization` | Three-stage pipeline: research the company → assess your competitiveness → write the cover letter. JSON handoffs between stages mean each step builds on the last. |
| 2 | `app-viability` | `market-research/app-viability-assessment` | Evaluates a mobile app idea against a 100-point rubric across four dimensions. Clear trigger condition, structured output, easy to compare ideas against each other. |
| 3 | `shower-inspector` | `safety-inspection/shower-inspection-ca` | Photo upload → JSON defect report with CA code citations. Demonstrates responsible AI design: seven explicit anti-hallucination rules, per-photo confidence thresholds. |
| 4 | `conversation-analyst` | `personal-tools/conversation-psychoanalysis` | Paste a conversation → get a psychological analysis using Big Five, cognitive bias frameworks, and attachment theory. Context variant selection (workplace / family / romantic). |
| 5 | `fashion-photo-director` | `marketing/couture-photo-director` | Image of a garment → full shot list with camera specs, lighting design, and styling direction. Model-adaptive (Midjourney, DALL-E 3, SDXL, Ideogram). Most technically complex — save for last. |

## What a Skill Looks Like

Each skill directory will contain a `SKILL.md` file with:
- A short trigger description (what the user says to invoke it)
- Clarifying questions asked before execution
- The prompt body
- Expected output format
- Any required file attachments or inputs

Skills are the natural next step after prompt engineering: once a prompt is reliable and well-scoped, packaging it as a skill removes friction and makes it genuinely reusable.
