---
name: job-application-pipeline
description: >
  Ten-stage collaborative job application pipeline. Researches the JD, company, and hiring team; runs interactive gap analysis and strategy discussion; then builds resume and cover letter through back-and-forth with the user. Use any time the user mentions applying to a job, writing a cover letter, optimizing their resume for a specific role, or doing pre-interview company research. Trigger on phrases like "I want to apply to [company]", "help me with my application for [role]", "I have a job posting I want to apply to", "can you write me a cover letter", "help me prep for applying to [company]", or "I need to optimize my resume for this role".
---

## What This Skill Does

A sequential, collaborative pipeline for job applications. Every stage either produces intelligence that feeds the next, or requires explicit user input before proceeding. **No stage is skipped. No gate is bypassed.** The quality of the final application package depends on the conversation that builds it.

---

## MANDATORY GATE RULE

> **This pipeline runs one stage at a time. After every stage that has a ⛔ STOP marker, Claude must pause, present outputs, and wait for explicit user confirmation before continuing. Do not proceed to the next stage without it. Not for speed. Not for convenience. Not even if the user's original message seems to authorize the full pipeline.**

---

## Pipeline Overview

| # | Stage | Gate? |
|---|---|---|
| 1 | JD Review | — |
| 2 | Company & Hiring Team Research | ⛔ User confirms research before proceeding |
| 3 | Resume Gap Analysis | — |
| 4 | Experience Gap Questions | ⛔ Conversational Q&A — one question at a time |
| 5 | Application Strategy Discussion | ⛔ User approves positioning before proceeding |
| 6 | Headline Brainstorm | ⛔ User picks/refines headline |
| 7 | Professional Summary | ⛔ User approves summary |
| 8 | Full Resume Customization | ⛔ User approves all changes |
| 9 | Additional Application Materials | ⛔ Ask before writing cover letter |
| 10 | Cover Letter | ⛔ Iterate until user approves |

---

## Upfront Inputs

Before starting Stage 1, confirm you have:

1. **Job description** — URL or pasted text. If a URL is given, fetch it. If the page is JavaScript-gated and doesn't render, say so explicitly and ask the user to paste the text directly. Do not proceed with partial JD content.
2. **Resume** — attached file or project file path.

Keep this to one message: *"To get started I need the job description (URL or paste it in) and your resume if you haven't already attached it."*

---

## Naming Convention

At the start of every run, create:
```
{company-slug}_{role-slug}/
  {company-slug}_company-brief.md
  {company-slug}_company-analysis.json
  {company-slug}_session-state.json        ← accumulates approved decisions across stages
  {company-slug}_resume-optimized.md
  {company-slug}_cover-letter.md
  {company-slug}_additional-materials.md   ← if needed
```

Tell the user the folder name upfront.

**Session state file:** Initialize `{company-slug}_session-state.json` at the start of Stage 4, conforming to `references/session-state.schema.json`. Write to it after each gate — do not wait until the end of the pipeline. Downstream stages (6, 7, 8, 10) read from this file rather than scraping conversation history. This matters in long conversations where earlier answers may no longer be in the active context window.

---

## Stage 1: JD Review

Read `references/stage1-jd-review.md` for the full prompt.

**Core behavior:**
- Fetch the JD URL. If the page fails to render or returns only partial content, stop immediately and tell the user: *"The page didn't render the full JD — can you paste it in directly?"* Do not proceed with incomplete content.
- Parse the JD into structured sections: role overview, key responsibilities, required qualifications, nice-to-haves, and any signals about team/culture/stage.
- Identify anything ambiguous or missing that would affect how you approach the application.

**Output:** Present a clean JD summary to the user — not a copy-paste, a structured interpretation. Flag any gaps (e.g., compensation not listed, seniority level unclear). No gate — proceed to Stage 2 immediately after presenting, since the user doesn't need to approve a JD summary.

---

## Stage 2: Company & Hiring Team Research

Read `references/stage2-company-research.md` for the full prompt and research standards.

**Core behavior:**
- Research the company per the existing standards (mission, market position, product strategy, equity, culture, interview intel).
- **Additionally:** Attempt to identify the likely hiring manager and members of the hiring team for this role. Search LinkedIn, the company website, press releases, conference talks, and any other public sources.
  - For each person identified: name, title, how long they've been at the company, background before joining, any public writing, talks, or stated priorities.
  - Assess their likely personality profile based on public signals: communication style, what they seem to value, any red flags or strong preferences visible in their public presence.
  - Confidence-label everything. If the hiring manager can't be identified, say so.
- Apply confidence labels to every claim. Tag quantitative claims with recency.

**Outputs:**
1. `{company-slug}_company-brief.md` — narrative report with seven sections: Inside Scoop, Mission, Market Position, Product Strategy, Equity, Interview Intel, Hiring Team Profiles
2. `{company-slug}_company-analysis.json` — structured JSON per `references/company-analysis.schema.json`

**⛔ STOP — Gate 2:** After presenting the narrative brief, add a visible separator before the gate question so it doesn't get lost at the end of a long output. Use this exact format:

```
---
⛔ Pausing here before Stage 3. Does this look right? Any corrections or insider knowledge I should factor in before moving to the resume gap analysis?
```

Wait for the user's response. Incorporate any corrections, then proceed to Stage 3.

---

## Stage 3: Resume Gap Analysis

Read `references/stage3-gap-analysis.md` for the full prompt.

**Core behavior:**
- Compare the resume against the JD requirements systematically.
- Produce: alignment table (top 7–10 JD requirements vs. candidate experience, alignment strength), identified gaps, ATS keyword priorities.
- Do NOT ask gap-filling questions here — that's Stage 4. Just identify the gaps.

**Output:** Present the alignment table and gap list to the user. Proceed directly to Stage 4 without stopping — the user will engage during the Q&A.

---

## Stage 4: Experience Gap Questions

**⛔ STOP — Gate 4 (ongoing):** This stage is entirely conversational. Ask gap-filling questions **one at a time**, as if in a live conversation. Do not present a bulleted list of questions. Wait for the user's answer before asking the next one.

**Core behavior:**
- Start with the highest-priority gap from Stage 3.
- For each question, explain briefly why you're asking (what it unlocks for the application).
- After each answer, either ask a follow-up or move to the next gap.
- Aim for 5–6 questions total. Prioritize questions that affect the competitiveness assessment (Stage 5) or could surface new resume bullets — those are the highest-value. Stop when those are covered, even if minor gaps remain. Don't ask about gaps that are either unaddressable (true missing experience) or already adequately covered by the resume.
- After each answer, write it immediately to `stage4_gap_answers` in `{company-slug}_session-state.json` — including the question asked, the user's answer, the gap it addresses, and any implication for resume bullets. Do not batch writes to the end of the stage; answers should persist even if the conversation is interrupted.

**Example opening:** *"Before I move to strategy, I want to fill in a few gaps. First: [most important gap from Stage 3]. [One question.]"*

---

## Stage 5: Application Strategy

Read `references/stage5-application-strategy.md` for the full prompt.

**⛔ STOP — Gate 5:** Present the strategy analysis and wait for explicit user approval before proceeding to resume work.

**Core behavior:**
1. **Applicant pool analysis:** Who else is likely applying? What does the typical strong candidate look like? What does the typical weak candidate look like?
2. **Competitiveness assessment:** Where does this candidate sit in that pool? Be honest. If the candidate is unlikely to get an interview, say so clearly — opportunity cost is real. Use a plain rating (e.g., top quartile / middle of the pack / long shot) with reasoning.
3. **Positioning options:** Based on the assessment, propose 2–3 distinct positioning strategies. Each strategy should have a name, a core narrative, what it emphasizes, and what it de-emphasizes. These should represent meaningfully different choices — not stylistic variations of the same strategy.

Present the analysis and ask: *"Which positioning direction feels right, or would you like to adjust any of these? This will shape the resume headline, summary, and cover letter."* Wait for the user's choice before continuing. Write the approved strategy to `stage5_strategy` in `{company-slug}_session-state.json`, including the competitiveness verdict and reasoning.

---

## Stage 6: Headline Brainstorm

Read `references/stage6-headline.md` for the full prompt.

**⛔ STOP — Gate 6:** Present headline options and wait for the user to pick or request revisions.

**Core behavior:**
- Using the approved positioning strategy from Stage 5, generate 5 headline alternatives using literary devices: rule of three, juxtaposition, paradox, specificity, contrast.
- For each: show the headline and one sentence explaining the strategic logic.
- Ask the user to pick one, request changes, or say "none of these — let's try again."
- Iterate until the user approves. Write the approved headline to `stage6_headline` in `{company-slug}_session-state.json`.

---

## Stage 7: Professional Summary

**⛔ STOP — Gate 7:** Show draft, iterate, wait for explicit approval.

**Core behavior:**
- Write a professional summary using the three-part structure: credibility statement → approach/method → impact statement.
- Ground it in the approved positioning strategy and headline direction.
- Write in first person. Match JD language without sounding optimized.
- Present the draft and ask for feedback. Revise until approved. Write the approved summary to `stage7_summary` in `{company-slug}_session-state.json`.

---

## Stage 8: Full Resume Customization

Read `references/stage8-resume-customization.md` for the full prompt.

**⛔ STOP — Gate 8:** Present the complete optimized resume and wait for user approval.

**Core behavior:**
- Read `{company-slug}_session-state.json` at the start of this stage. All inputs (positioning strategy, headline, summary, gap answers) come from there — not from conversation history.
- Update the skills section: category headers matching job priorities, only skills the candidate actually has, ordered by relevance.
- Update each experience role: add context sentence, rewrite bullets for relevance, ≥80% of bullets quantified. No fabrication. Surface the answers from Stage 4.
- Save the complete resume as `{company-slug}_resume-optimized.md`.
- Present it and ask: *"How does this look? Any bullets you want changed, anything that doesn't sound like you?"* Revise until approved.

---

## Stage 9: Additional Application Materials

**⛔ STOP — Gate 9:** Ask before starting cover letter work.

**Core behavior:**
Ask: *"Before I start the cover letter — are there any other application requirements? Things like: essays on specific topics, short-answer questions, portfolio or work sample links, or anything else the application form asks for."*

- If yes: help the user complete those materials first, save to `{company-slug}_additional-materials.md`. Write a summary of what was produced and its cover letter implications to `stage9_additional_materials` in `{company-slug}_session-state.json`.
- If no: write `{"has_additional_requirements": false}` to `stage9_additional_materials` in `{company-slug}_session-state.json` and proceed to Stage 10.

---

## Stage 10: Cover Letter

Read `references/stage10-cover-letter.md` for the full prompt and output standards.

**⛔ STOP — Gate 10 (multiple points):**
1. Ask for a personal story or anecdote before drafting.
2. Show the pre-draft strategy and wait for approval.
3. Show the draft and iterate until approved.

**Core behavior:**
- Read `{company-slug}_session-state.json` at the start of this stage. The positioning strategy, personal story, and additional materials implications all come from there.

**Step 10a — Personal story:** Ask the user: *"Is there a specific story, moment, or personal connection to this company's mission that you'd want in the cover letter? Something that doesn't appear in the resume."* Write the answer (or `{"provided": false}` if none) to `stage10_personal_story` in `{company-slug}_session-state.json` before drafting anything.

**Step 10b — Pre-draft strategy:** Before writing, present:
- Opening hook approach (one sentence on what angle you'll lead with)
- Body structure (what each paragraph will accomplish)
- Closing approach
Ask: *"Does this structure feel right?"* Get a green light.

**Step 10c — Draft and iterate:** Write the letter. Present it. Ask for feedback. Revise until approved. Save final to `{company-slug}_cover-letter.md`.

**Standards:**
- Maximum one page.
- No résumé bullet repetition — interpret significance, don't repeat stats.
- 100% factually supported.
- Only use company-analysis JSON facts where confidence ≥ medium.
- Integrate any additional materials content from Stage 9 without contradiction.

---

## Handoff Notes

**Don't invent things.** Every claim must trace back to the resume, user answers from Stage 4, web research, or the JD.

**The JSON schema carries the confidence signal.** Stage 10 reads it; low-confidence claims get softened language ("based on recent signals") not direct assertion.

**Gates are the design, not friction.** They exist because the quality of the output is a direct function of the conversation. An AI that skips them is faster and worse.

**One folder, multiple files.** By the end, the user has a complete application package: company brief for interview prep, optimized resume, cover letter, and any additional materials.

---

## References

- `references/stage1-jd-review.md` — JD parsing prompt and structured output format
- `references/stage2-company-research.md` — Company + hiring team research prompt and standards
- `references/stage3-gap-analysis.md` — Gap analysis framework and alignment table format
- `references/stage5-application-strategy.md` — Applicant pool, competitiveness, and positioning framework
- `references/stage6-headline.md` — Headline brainstorm prompt and literary device guide
- `references/stage8-resume-customization.md` — Full resume optimization prompt
- `references/stage10-cover-letter.md` — Cover letter prompt, rules, and structure
- `references/company-analysis.schema.json` — JSON schema for Stage 2 company research output
- `references/session-state.schema.json` — JSON schema for accumulating approved decisions across Stages 4–10
