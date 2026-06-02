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
| 3 | Resume Gap Analysis + ATS Keyword Matching | — |
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

**Session state file:** Initialize `{company-slug}_session-state.json` at the start of Stage 2 (the hiring problem synthesis writes there after company research). Conform to `references/session-state.schema.json`. Write to it after each stage that produces output — do not batch writes to the end. Stages 5, 6, 7, 8, and 10 all read `stage2_hiring_problem` as a primary input — it is the through-line the whole application answers.

---

## Stage 1: JD Review

Read `references/stage1-jd-review.md` for the full prompt.

**Core behavior:**
- Fetch the JD URL. If the page fails to render or returns only partial content, stop immediately and tell the user: *"The page didn't render the full JD — can you paste it in directly?"* Do not proceed with incomplete content.
- Parse the JD into structured sections: role overview, key responsibilities, required qualifications, nice-to-haves, and any signals about team/culture/stage.
- Identify anything ambiguous or missing that would affect how you approach the application.
- **Flag context-dependent language:** Note any JD phrases whose meaning depends on knowing the company's actual situation — things that could signal very different hiring problems depending on context. Examples: "drive AI adoption," "build from scratch," "partner with the business," "own the roadmap." List these explicitly as *phrases to reinterpret after company research.* Do not guess at their meaning yet — that happens at the end of Stage 2.

**Output:** Present a clean JD summary to the user — not a copy-paste, a structured interpretation. Flag any gaps (e.g., compensation not listed, seniority level unclear). End with the flagged context-dependent phrases as a brief list. No gate — proceed to Stage 2 immediately.

---

## Stage 2: Company & Hiring Team Research

Read `references/stage2-company-research.md` for the full prompt and research standards.

**Core behavior:**
- Research the company per the existing standards (mission, market position, product strategy, equity, culture, interview intel).
- **Additionally:** Attempt to identify the likely hiring manager and members of the hiring team for this role. Search LinkedIn, the company website, press releases, conference talks, and any other public sources.
  - For each person identified: name, title, how long they've been at the company, background before joining, any public writing, talks, or stated priorities.
  - Assess their likely personality profile based on public signals: communication style, what they seem to value, any red flags or strong preferences visible in their public presence.
  - Confidence-label everything. If the hiring manager can't be identified, say so.
- Apply confidence labels to every claim. Tag **all** quantitative claims with recency — this includes funding figures, valuations, headcount, and industry benchmark ranges (e.g., "ARR estimate (as of ~2024–2025)"). No quantitative number or range should appear without a recency marker.

**Outputs:**
1. `{company-slug}_company-brief.md` — narrative report with seven sections: Inside Scoop, Mission, Market Position, Product Strategy, Equity, Interview Intel, Hiring Team Profiles
2. `{company-slug}_company-analysis.json` — structured JSON per `references/company-analysis.schema.json`

**Hiring Manager Profile — write to session state as `stage2_hm_profile`:**

After the narrative brief is complete, distill the hiring manager research into a structured profile for downstream use. If the hiring manager couldn't be identified, populate what can be inferred from the JD's tone, emphasis, and seniority signals, and flag it as inferred. Write this to `stage2_hm_profile` in `{company-slug}_session-state.json`:

```json
{
  "name": "Name or 'Unknown'",
  "confidence": "confirmed | inferred | unknown",
  "background": "One sentence: career path and functional origin (e.g., 'Engineering-to-PM, spent 8 years at enterprise SaaS companies')",
  "values_signals": ["List of 3–5 things they demonstrably care about, drawn from public writing, talks, LinkedIn, or JD emphasis — concrete, not generic"],
  "communication_style": "How they write and speak publicly — formal/casual, data-driven/narrative, direct/diplomatic",
  "likely_confident_if": ["2–3 specific things a candidate would say or show that would make this person lean in"],
  "likely_skeptical_if": ["2–3 specific things that would raise flags for this person — based on their background and stated values, not generic interview fears"],
  "jd_tone_signals": "What the JD's word choices, emphasis, and structure reveal about what this HM prioritizes — independent of what it literally says"
}
```

This profile is a primary input for the Hiring Manager Filter applied in Stages 5, 6, 7, 8, and 10. Confidence-label everything. If a field is truly unknowable, write `null` and note why.

**Hiring Problem Synthesis — append to the company brief as an eighth section:**

After completing the company research, return to the context-dependent JD phrases flagged in Stage 1 and resolve them with what you now know. Then synthesize a hiring problem statement: *what specific business problem is this hire meant to solve?*

Write 3–5 sentences covering:
- The **primary problem** — the core thing that breaks or stalls without this hire
- **Secondary goals** — what the hiring manager also wants but would trade away if forced to
- **Implied urgency** — signals about timeline or pressure (competitive threat, growth stage, recent org change, etc.)
- **What a bad hire looks like** — what failure mode the hiring manager is most afraid of, inferred from company context and JD emphasis

This should read as a pointed analytical conclusion, not a restatement of the JD. If company research revealed something that recontextualizes a flagged JD phrase, name it explicitly: *"'Own the roadmap end-to-end' likely signals that the previous PM was execution-only and the team lost strategic direction — not that they want someone to start a roadmap from scratch."*

Write the hiring problem statement to `stage2_hiring_problem` in `{company-slug}_session-state.json`. This is a primary input for Stages 5, 6, 7, 8, and 10 — every downstream stage should answer the question this section poses.

**⛔ STOP — Gate 2:** After presenting the narrative brief and hiring problem synthesis, add a visible separator. Use this exact format:

```
---
⛔ Pausing here before Stage 3. Does this read of the hiring problem feel right? Any corrections, insider knowledge, or recruiter intel that would change the picture?
```

Wait for the user's response. If they have corrections — a recruiter call, inside knowledge, a referral who described the real situation — incorporate them and update `stage2_hiring_problem` in session state before proceeding to Stage 3.

---

## Stage 3: Resume Gap Analysis + ATS Keyword Matching

Read `references/stage3-gap-analysis.md` for the full prompt.

**Core behavior — two parallel analyses, presented together:**

### 3A: Alignment & Gap Analysis
- Compare the resume against the JD requirements systematically.
- Produce an alignment table: top 7–10 JD requirements vs. candidate experience, with alignment strength (Strong / Partial / Gap).
- Identify gaps in three tiers:
  - **Critical gaps** — required qualifications the resume doesn't address at all
  - **Partial gaps** — requirements where the resume has adjacent experience but not a direct match
  - **Addressable gaps** — things that could be surfaced in Stage 4 Q&A if the experience exists but isn't on the resume yet
- Do NOT ask gap-filling questions here — that's Stage 4. Just identify them.

### 3B: ATS Keyword Matching
ATS (Applicant Tracking System) filters rank resumes by keyword density before a human reads them. This analysis ensures the resume uses the JD's own language where it's truthful to do so.

**Step 1 — Extract JD keyword inventory.** Pull:
- Role-specific titles and seniority language (e.g., "Principal," "Staff," "Solutions Architect")
- Technical skills, tools, platforms, and frameworks named explicitly
- Methodologies and processes called out (e.g., "agile," "discovery," "go-to-market")
- Domain terms that signal industry fluency (e.g., "omnichannel," "agentic workflows")
- Soft-skill phrases that appear more than once (repetition signals they're weighted)

**Step 2 — Map each keyword against the current resume.** For each keyword:
- **Present** — the word or a close synonym appears on the resume
- **Absent but supportable** — the candidate likely has this experience but the resume doesn't use the JD's language (high-priority rewrite target)
- **Absent, not supportable** — the experience genuinely doesn't exist (do not add)

**Step 3 — Produce the ATS keyword table.** Format:

| Keyword / Phrase | JD Weight | Resume Status | Action |
|---|---|---|---|
| [keyword] | High/Med/Low | Present / Absent-supportable / Absent-gap | Add verbatim / Rephrase / Skip |

Cap the table at the 15 highest-weighted terms. "JD Weight" = High if it appears in required qualifications or multiple times; Med if once in responsibilities; Low if only in nice-to-haves.

**Step 4 — Write ATS data to session state.** After presenting the table, write to `stage3_ats_keywords` in `{company-slug}_session-state.json`:
```json
{
  "high_priority_additions": ["keyword1", "keyword2"],
  "present_keywords": ["keyword3"],
  "absent_gaps": ["keyword4"]
}
```
Stage 8 reads this directly when rewriting bullets and the skills section — it is the source of truth for which terms to weave in.

**Output:** Present both the alignment table (3A) and the ATS keyword table (3B) in a single response. Proceed directly to Stage 4 without stopping.

---

## Stage 4: Experience Gap Questions

**⛔ STOP — Gate 4 (ongoing):** This stage is entirely conversational. Ask gap-filling questions **one at a time** — exactly one question per message, one question mark. Do not combine multiple questions into a single paragraph or sentence, even without list formatting. Do not present a bulleted or numbered list of questions. Wait for the user's answer before asking the next one.

**Core behavior:**
- Start with the highest-priority gap from Stage 3.
- For each question, explain briefly why you're asking (what it unlocks for the application).
- After each answer, either ask a follow-up or move to the next gap.
- Aim for 5–6 questions total. Prioritize questions that affect the competitiveness assessment (Stage 5) or could surface new resume bullets — those are the highest-value. Stop when those are covered, even if minor gaps remain. Don't ask about gaps that are either unaddressable (true missing experience) or already adequately covered by the resume.
- After each answer, write it immediately to `stage4_gap_answers` in `{company-slug}_session-state.json` — including the question asked, the user's answer, the gap it addresses, and any implication for resume bullets. Do not batch writes to the end of the stage; answers should persist even if the conversation is interrupted.

**Example opening:** *"Before I move to strategy, I want to fill in a few gaps. First: [most important gap from Stage 3]. [One question, one question mark.]"*

---

## Stage 5: Application Strategy

Read `references/stage5-application-strategy.md` for the full prompt.

**⛔ STOP — Gate 5:** Present the strategy analysis and wait for explicit user approval before proceeding to resume work.

**Core behavior:**
0. **Anchor to the hiring problem and hiring manager.** Read both `stage2_hiring_problem` and `stage2_hm_profile` from `{company-slug}_session-state.json` before doing anything else. Then run the Hiring Manager Filter:

   > *Hiring Manager Filter — Stage 5:* Given this HM's background, values signals, and likely skepticisms, which positioning angle would make them lean in vs. put them off? Note any mismatch between what the applicant pool analysis suggests and what this specific person is likely to respond to. Flag it if the strongest strategic angle for the pool is a weak fit for this individual.

   Every element of the strategy — pool analysis, competitiveness, positioning — should be evaluated against both the hiring problem and the HM profile.
1. **Applicant pool analysis:** Who else is likely applying? What does the typical strong candidate look like? What does the typical weak candidate look like?
2. **Competitiveness assessment:** Where does this candidate sit in that pool? Be honest. If the candidate is unlikely to get an interview, say so clearly — opportunity cost is real. Use a plain rating (e.g., top quartile / middle of the pack / long shot) with reasoning.
3. **Positioning options:** Based on the assessment, propose 2–3 distinct positioning strategies. Each strategy should have a name, a core narrative, what it emphasizes, and what it de-emphasizes. These should represent meaningfully different choices — not stylistic variations of the same strategy. For each, explicitly state how it addresses the hiring problem from Stage 2 — if a positioning angle doesn't connect to that problem, it's the wrong angle.

Present the analysis and ask: *"Which positioning direction feels right, or would you like to adjust any of these? This will shape the resume headline, summary, and cover letter."* Wait for the user's choice before continuing. Write the approved strategy to `stage5_strategy` in `{company-slug}_session-state.json`, including the competitiveness verdict and reasoning.

---

## Stage 6: Headline Brainstorm

Read `references/stage6-headline.md` for the full prompt if it exists. The rules below take precedence.

**⛔ STOP — Gate 6:** Present headline options and wait for the user to pick or request revisions.

**What a resume headline must do:**
1. Communicate the candidate's primary value — what they're best at — anchored to what the role most needs.
2. Differentiate: it should be harder to apply verbatim to a generic candidate than a generic title like "Product Manager."
3. Not fabricate. No skills, domains, or credentials the candidate doesn't have. No implied scale or scope that isn't supported by the resume.
4. Not be boastful. The tone is confident, not self-congratulatory. There's a meaningful difference between "I'm exceptional at X" and a headline that demonstrates it by how it's constructed.

**Patterns to avoid — these are banned:**
- "From [X] to [Y]" constructions. They're overused and signal nothing distinctive.
- Random keyword strings. "AI | Product | Strategy | Data | Enterprise" is not a headline — it's a tag cloud. Every word must pull its weight toward a coherent idea.
- Superlatives: "world-class," "visionary," "results-driven," "passionate."
- Generic professional titles with a modifier bolted on: "Senior Strategic Product Leader."

**How to construct candidates:**

Start with three inputs from session state: the positioning strategy approved in Stage 5, the hiring problem from `stage2_hiring_problem`, and the HM profile from `stage2_hm_profile`. Run the Hiring Manager Filter before generating any options:

> *Hiring Manager Filter — Stage 6:* Given this HM's communication style, values signals, and what would make them skeptical, what tone and framing register as credible vs. off-putting? A data-driven, operationally-minded HM will read compressed, specific language as confident; they'll read visionary or abstract framing as unsubstantiated. An HM who came up through storytelling or brand will respond to the opposite. Let the HM profile shape the register of every headline option, not just the content.

The headline should answer the hiring problem — not abstractly, but by implying that this candidate is the solution to it. If the hiring problem is "they need someone who can translate AI capabilities into revenue without needing a technical co-pilot," the headline should make that legible without stating it literally.

**Literary device toolkit for headlines** (pick a dominant device per headline, not a pile of them):

*Sound and rhythm* — Alliteration, assonance, and meter make a phrase memorable without the reader knowing why. "Physics to Product" works partly because of the hard stop of the P sounds. Use sparingly — it should feel crafted, not forced.

*Compression* — Parataxis and asyndeton strip conjunctions for speed. "Build. Ship. Learn." is three ideas in six words. Useful when the candidate's value is a sequence or process.

*Tension and contrast* — Juxtaposition, oxymoron, and paradox force the reader to resolve a contradiction, which creates recall. "Rigorous systems, fast decisions" implies someone who doesn't sacrifice one for the other. The tension does work that a straight description can't.

*Specificity as device* — A single concrete noun or number outpunches an adjective every time. Naming a real domain, tool, or outcome is more differentiating than claiming to be "results-oriented."

*Implied metaphor* — A phrase that carries a structural analogy without stating it. "Translating AI into market motion" implies a translator's precision without saying "communication skills."

*Chiasmus or reversal* — Flipping a familiar structure: "Shape tools, tools shape us" forces a re-read. Use this when the candidate's value is counterintuitive.

*Zeugma* — One verb or noun that governs two different things: "Designing products and the teams that build them." Efficient, implies breadth without listing.

*Negative space* — What's intentionally not said. A tight, specific headline implies everything it excludes. "AI infrastructure for regulated industries" says nothing about soft skills — and doesn't need to.

**For each of the 5 options, show:**
1. The headline itself.
2. The dominant literary device used.
3. One sentence of strategic logic: what it emphasizes, what it implies about the candidate, why it serves this particular application.

**After presenting:** Ask the user to pick one, request changes, or say "none — try again." Iterate without complaint. Write the approved headline to `stage6_headline` in `{company-slug}_session-state.json`.

---

## Stage 7: Professional Summary

**⛔ STOP — Gate 7:** Show draft, iterate, wait for explicit approval.

**Core behavior:**
- Before drafting, run the Hiring Manager Filter:

  > *Hiring Manager Filter — Stage 7:* Pull `stage2_hm_profile`. What word choices, sentence rhythm, and types of evidence would make this HM read the summary as credible and immediately relevant? What would make them skim past it? The summary should feel written in a register this person responds to — not generic professional prose. If their communication style is direct and data-forward, lead with a concrete claim. If they value narrative and mission alignment, the credibility statement should carry more weight.

- Write a professional summary using the three-part structure: credibility statement → approach/method → impact statement.
- Ground it in the approved positioning strategy, headline direction, the hiring problem from `stage2_hiring_problem`, and the HM profile from `stage2_hm_profile`. The summary's impact statement should land on what the hiring manager needs solved — make it feel like the candidate was written for this problem.
- Write in first person. Match JD language without sounding optimized.
- Present the draft and ask for feedback. Revise until approved. Write the approved summary to `stage7_summary` in `{company-slug}_session-state.json`.

---

## Stage 8: Full Resume Customization

Read `references/stage8-resume-customization.md` for the full prompt.

**⛔ STOP — Gate 8:** Present the complete optimized resume and wait for user approval.

**Core behavior:**
- Read `{company-slug}_session-state.json` at the start of this stage. All inputs (hiring problem, positioning strategy, headline, summary, gap answers, ATS keywords) come from there — not from conversation history.
- **Hiring problem as editorial filter:** Pull `stage2_hiring_problem`. When choosing which bullets to keep, rewrite, or cut, ask: does this bullet speak to the problem this hire is meant to solve? Bullets that don't connect — even impressive ones — should be deprioritized or cut if space is needed. Bullets that directly address the hiring problem should be prominent and specific.
- **Hiring Manager Filter — Stage 8:** Pull `stage2_hm_profile`. Before finalizing the resume, read it as this HM would: Given their background and values signals, which bullets will land as compelling evidence and which will read as noise or raise doubts? Specifically: (1) reframe any bullet whose framing conflicts with what this HM demonstrably values — the same accomplishment can be framed around speed, rigor, collaboration, or impact depending on what resonates; (2) check that the skills section ordering and category labels reflect this HM's priorities, not a generic ordering; (3) if `likely_skeptical_if` flags anything the resume currently triggers, address it — either by removing the signal or explicitly countering it elsewhere.
- **ATS integration:** Pull `stage3_ats_keywords.high_priority_additions` from `{company-slug}_session-state.json`. For each term, weave it into bullets or the skills section where it's truthful — use the JD's exact phrasing, not paraphrases. Do not manufacture usage; if a term can't be placed honestly, leave it out. After completing the resume, do a pass confirming every high-priority term is present at least once (or explicitly noted as unplaceable).
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
- Read `{company-slug}_session-state.json` at the start of this stage. The hiring problem, positioning strategy, personal story, and additional materials implications all come from there.
- **The cover letter's job is to answer the hiring problem directly.** The resume proves qualifications; the cover letter makes the argument for why this candidate solves the specific problem identified in Stage 2. If the pre-draft strategy doesn't connect the opening hook to the hiring problem, revise it until it does.
- **Hiring Manager Filter — Stage 10:** Pull `stage2_hm_profile`. Before drafting the pre-draft strategy (Step 10b), answer: What opening would make this specific person stop and read? What would make them put it down in the first two sentences? What tone — direct assertion, intellectual curiosity, operational credibility, mission resonance — matches how they communicate and what they've signaled they value? The cover letter is the one artifact that can directly address this person; use the profile to make it feel like it was written for them, not for the role abstractly.

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

**The hiring problem is the through-line.** `stage2_hiring_problem` is not a section of the company brief — it's the editorial lens for the entire application. Every positioning decision, resume edit, and cover letter paragraph should be traceable back to the problem this hire is meant to solve. If something doesn't connect, cut it or reframe it.

**Don't invent things.** Every claim must trace back to the resume, user answers from Stage 4, web research, or the JD.

**The JSON schema carries the confidence signal.** Stage 10 reads it; low-confidence claims get softened language ("based on recent signals") not direct assertion.

**Gates are the design, not friction.** They exist because the quality of the output is a direct function of the conversation. An AI that skips them is faster and worse.

**One folder, multiple files.** By the end, the user has a complete application package: company brief for interview prep, optimized resume, cover letter, and any additional materials.

---

## References

- `references/stage1-jd-review.md` — JD parsing prompt and structured output format
- `references/stage2-company-research.md` — Company + hiring team research prompt and standards
- `references/stage3-gap-analysis.md` — Gap analysis framework, alignment table, and ATS keyword matching
- `references/stage5-application-strategy.md` — Applicant pool, competitiveness, and positioning framework
- `references/stage6-headline.md` — Headline brainstorm prompt and literary device guide (SKILL.md Stage 6 rules take precedence if conflict)
- `references/stage8-resume-customization.md` — Full resume optimization prompt
- `references/stage10-cover-letter.md` — Cover letter prompt, rules, and structure
- `references/company-analysis.schema.json` — JSON schema for Stage 2 company research output
- `references/session-state.schema.json` — JSON schema for accumulating approved decisions across Stages 4–10
