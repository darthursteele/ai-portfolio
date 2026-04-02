---
name: job-search-pipeline
description: >
  Three-stage job application pipeline: researches the target company, optimizes the resume, and writes the cover letter — with structured JSON handoffs between stages. Use this skill any time the user mentions applying to a job, writing a cover letter, optimizing their resume for a specific role, or doing pre-interview company research. Trigger on phrases like "I want to apply to [company]", "help me with my application for [role]", "I have a job posting I want to apply to", "can you write me a cover letter for [company]", "help me prep for applying to [company]", or "I need to optimize my resume for this role". Even if the user only asks for one stage (e.g. "just write the cover letter"), invoke this skill — it will ask which stages they want to run.
---

## What This Skill Does

This is a three-stage sequential pipeline for job applications, designed around a core principle: good applications require good intelligence, and good intelligence should flow between stages rather than getting re-entered manually.

**Stage 1 — Company Research**: Conducts deep due diligence on the target company using web search. Outputs both a human-readable brief and a structured JSON file with confidence labels on every factual claim. The JSON becomes the structured input for Stage 2.

**Stage 2 — Cover Letter**: Reads the resume, job description, and Stage 1 JSON. Performs a competitiveness assessment and positioning analysis *before* writing anything. Gets your approval on the positioning strategy, then drafts the letter grounded in specific company intelligence.

**Stage 3 — Resume Optimization**: Frames your experience as a solution to the hiring manager's business problem. Produces an alignment analysis, ATS keyword priorities, gap assessment, and a fully optimized resume with 80%+ quantified bullets.

The JSON schema (`references/company-analysis.schema.json`) is the backbone that links Stage 1 to Stage 2 — confidence labels travel with each claim, so the cover letter only uses information the research actually verified.

---

## Upfront Inputs

Before starting, ask the user for:

1. **Target company** and **role title** (required for all stages)
2. **Department/team** (optional but improves Stage 1 research depth — e.g., "Data & Analytics", "Product")
3. **Which stages to run**: all three, or specific ones. Default to all three if not specified.
4. **Resume file**: needed for Stages 2 and 3. Ask them to attach it or give the path.
5. **Job description file**: needed for Stages 2 and 3. Ask them to attach it or paste it.
6. **Personalization notes** (optional): tone preferences, specific themes to emphasize, things to avoid.

Keep this conversational — one message to collect, not six separate questions. Something like: *"I'll run the full three-stage pipeline. To get started: what's the company name, the role you're applying for, and the department or team if you know it? And go ahead and attach your resume and the job description — I'll use those for the cover letter and resume stages."*

If they only need specific stages, skip the inputs you don't need. But check: if they ask for just a cover letter without a company research file, offer to run Stage 1 first — the letter will be significantly better with it.

---

## Naming Convention

At the start of every run, establish a base name for output files:
```
{company-slug}_{role-slug}/
  {company-slug}_company-brief.md
  {company-slug}_company-analysis.json
  {company-slug}_cover-letter.md
  {company-slug}_resume-optimized.md
```

Example: `rentable_principal-pm/rentable_company-brief.md`

Save all outputs to a single folder in the workspace. Tell the user the folder name at the start so they know where to find things.

---

## Stage 1: Company Intelligence Research

Read `references/stage1-company-research.md` for the full prompt and research standards.

**Core behavior:**
- Run web searches to gather information from official sources, analyst reports, Glassdoor/Blind, SEC filings, tech media.
- Apply confidence labels (`high / medium / low / speculation`) to every factual claim.
- Tag every quantitative claim with a recency marker ("as of Q3 2024").
- If a piece of information simply isn't publicly available, say so — don't fill the gap with guesswork.

**Outputs:**
1. `{company-slug}_company-brief.md` — human-readable narrative report with six sections (inside scoop, mission, market position, product strategy, equity, interview intel)
2. `{company-slug}_company-analysis.json` — structured JSON conforming to `references/company-analysis.schema.json`

**After Stage 1:**
Show the user the narrative brief and tell them the JSON file has been saved. Ask: *"Does this look right? Any corrections or gaps before I move to the cover letter?"* Incorporate feedback, then proceed to Stages 2 and 3.

---

## Stage 2: Cover Letter

Read `references/stage2-cover-letter.md` for the full prompt and output standards.

**Core behavior:**
- Load the company-analysis JSON from Stage 1 (or from a user-provided file if skipping Stage 1).
- Only reference company facts where confidence ≥ "medium". Lower-confidence claims can appear as "based on recent company signals" without presenting them as certain.
- The pre-draft analysis step is not optional — it's the part that actually makes the letter good.

**Pre-draft analysis (do this before writing a single word of the letter):**
1. Competitiveness assessment: where does this candidate rank against typical applicants for this role?
2. Key strengths for this specific JD, and most likely hiring manager concerns.
3. Recommended positioning strategy and narrative frame.

Show this analysis to the user. Ask: *"Does this positioning feel right? Anything you'd adjust before I draft the letter?"* Get a green light before writing.

**Output:**
`{company-slug}_cover-letter.md` — one-page letter in clear, credible, engaging prose. No résumé bullet repetition. 100% factually supported.

---

## Stage 3: Resume Optimization

Read `references/stage3-resume-optimizer.md` for the full prompt and analysis framework.

**Core behavior:**
- Frame the entire optimization around the business problem the hiring manager is trying to solve — not just skills matching.
- Ask gap-filling questions before writing the optimized resume. The resume optimizer needs to surface experience the user may have left off their current resume.

**Analysis first:**
1. Alignment table: top 7 JD requirements vs. candidate's experience, keyword frequency, alignment strength.
2. Gap assessment and gap-filling questions.
3. ATS keyword priorities.
4. Headline brainstorm (5 alternatives using literary devices: rule of three, juxtaposition, paradox).

Show the analysis and ask the gap-filling questions. Wait for responses before producing the final document.

**Output:**
`{company-slug}_resume-optimized.md` — full optimized resume: adjusted headline, revised professional summary (3-part structure: credibility + approach + impact), restructured skills section, enhanced experience bullets (≥80% quantified).

---

## Handoff Notes

A few things that matter for quality across all three stages:

**Don't invent things.** None of the three stages should produce claims not grounded in either web research, the attached resume, or the job description. If a gap needs filling, ask rather than guess.

**The JSON schema carries the confidence signal.** When Stage 2 reads the company-analysis JSON, it reads the confidence field on every claim and adjusts its language accordingly. Don't strip that signal.

**The pre-draft approval steps aren't friction — they're the design.** Both Stage 2 (positioning approval) and Stage 3 (gap-filling questions) have intentional human checkpoints. Don't skip them for speed. They're why the outputs are better than template-generated letters.

**One folder, multiple files.** By the end of the pipeline, the user should have a complete application package in one place: the research brief they can use for interview prep, the tailored cover letter, and the optimized resume.

---

## References

- `references/stage1-company-research.md` — Full company research prompt with research standards and JSON output spec
- `references/stage2-cover-letter.md` — Full cover letter prompt with rules of engagement and output format
- `references/stage3-resume-optimizer.md` — Full resume optimization prompt with analysis framework
- `references/company-analysis.schema.json` — JSON schema for Stage 1 → Stage 2 handoff
