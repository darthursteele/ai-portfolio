# Prompt Showcase

A curated selection of production-grade prompts from my personal library — organized for readability, reuse, and potential extraction into a standalone public repo.

Each prompt here was selected because it demonstrates one or more of: structured output design, multi-agent pipeline thinking, evidence-only / anti-hallucination discipline, rubric-based evaluation, or meaningful real-world utility.

---

## What's Here

| Category | Prompts | What They Show |
|----------|---------|----------------|
| [Market Research](#market-research) | 2 | Standardized scoring, TAM/SAM analysis, JSON schema output |
| [Career](#career) | 3 | Multi-agent orchestration, ATS optimization, confidence-labeled research |
| [Marketing](#marketing) | 2 | Image-gen model adaptation, brand strategy evaluation rubric |
| [AI Behavior](#ai-behavior) | 3 | Persona engineering, meta-prompting, Socratic coaching |
| [Safety Inspection](#safety-inspection) | 1 | Anti-hallucination rules, structured JSON output, code citations |
| [Personal Tools](#personal-tools) | 2 | Psychological frameworks, covert communication scripting |

---

## Market Research

### [`app-viability-assessment.md`](./market-research/app-viability-assessment.md)
A standardized framework for evaluating mobile app ideas across market appeal, revenue potential, and competitive positioning — all with numerical scores for cross-idea comparison. Built to answer: *"Is this worth building?"* in a repeatable, comparable way.

**Why it's notable:** The scoring rubric (100-point scale, 4 sub-dimensions) lets you compare completely different app ideas on the same axis. The TAM/SAM breakdown and path-to-$100M section push beyond surface-level analysis.

### [`competitive-market-analysis.md`](./market-research/competitive-market-analysis.md)
An investment-analyst-style market position report template — adaptable to any company and strategic focus. Works equally well for pre-interview research, due diligence, or just understanding a space.

**Why it's notable:** The variable design (`STRATEGIC_FOCUS`) means the same prompt structure handles *"dominating the SMB segment"* and *"positioning for acquisition"* — very different questions with the same analytical skeleton.

---

## Career

### [`company-intelligence-brief.md`](./career/company-intelligence-brief.md)
Deep pre-interview research prompt with dual output modes: human-readable briefing *or* structured JSON conforming to a shared schema. Designed to feed downstream prompts (like the cover letter generator) as part of a multi-agent pipeline.

**Why it's notable:** This is the anchor of a three-prompt job-search pipeline. It outputs machine-readable JSON with confidence labels (`high`, `medium`, `low`, `speculation`) on every factual claim — a pattern borrowed from intelligence analysis.

### [`cover-letter-generator.md`](./career/cover-letter-generator.md)
A cover letter generator that accepts file attachments (résumé + JD) and an optional structured JSON file from the company-intelligence-brief. Performs a competitiveness assessment and positioning strategy *before* writing a single word of the letter.

**Why it's notable:** The pre-draft analysis step — ranking candidate competitiveness, flagging risks a hiring manager might raise, then asking for approval before drafting — mirrors how a good human writer actually thinks. It also integrates with the company-analysis schema for grounded, specific personalization.

### [`expert-resume-optimization.md`](./career/expert-resume-optimization.md)
A comprehensive resume optimizer that frames candidates as solutions to a hiring manager's business problem, not just a list of past jobs. Includes ATS keyword analysis, gap identification, headline brainstorming with literary devices, and a specific structure for the professional summary.

**Why it's notable:** The business-problem framing is genuinely different from typical resume prompts. The requirement to frame every bullet in terms of business impact (80%+ quantified) and align the entire document to a single professional brand narrative shows strategic coherence, not just polish.

---

## Marketing

### [`couture-photo-director.md`](./marketing/couture-photo-director.md)
An AI agent spec for generating photography prompts for luxury fashion marketing campaigns. Accepts reference images of garments and produces a full shot list — hero, detail, lifestyle, e-commerce — each with complete camera specs, lighting design, and styling direction.

The model-adaptive version goes further: it tailors prompt syntax and structure to the specific image generation model being used (Midjourney v6, DALL-E 3, Stable Diffusion XL, Ideogram v2), with budget-tier and timeline-feasibility layers baked in.

**Why it's notable:** This is a genuinely complex multi-variable agent spec. The model-specific optimization section alone — with different syntax conventions, quality modifier strategies, and negative prompt guidance per platform — represents meaningful prompt engineering depth.

### [`brand-foundations-evaluation.md`](./marketing/brand-foundations-evaluation.md)
A rubric-based evaluation prompt for brand strategy documents. Scores across five criteria (purpose, audience definition, positioning, values, internal coherence) on a 1–3 scale with explicit rubric anchors — so the model can't hedge.

**Why it's notable:** The rubric design forces directness: each score anchor describes what "strong" looks like in language specific enough to distinguish it from "adequate." The closing question — *"Could a strategist build a complete brand voice from this document alone?"* — gives a hard yes/no to an otherwise fuzzy deliverable.

---

## AI Behavior

### [`humanize-writing.md`](./ai-behavior/humanize-writing.md)
A system prompt for producing writing that reads as authentically human — covering voice, sentence structure, word choice, rhythm, and a comprehensive list of AI vocabulary clichés to avoid. Essentially a style guide baked into a prompt.

**Why it's notable:** The negative constraints are unusually specific. Rather than just saying "sound human," this catalogs the exact sentence-opening patterns, transition formulas, explanatory templates, and vocabulary clichés that give AI writing away — and prohibits each one by name.

### [`objective-skeptical-partner.md`](./ai-behavior/objective-skeptical-partner.md)
A short but highly effective behavior amendment: turns the model into a hypothesis-testing partner that interrogates assumptions, offers alternatives, and prioritizes truth over agreeableness. One of the best examples of how much you can shift AI behavior with very few words.

**Why it's notable:** Economy of expression. This is fewer than 100 words and completely changes the character of a conversation. It's the opposite of a complex multi-page spec — and equally valid as a prompt engineering technique.

### [`business-coach.md`](./ai-behavior/business-coach.md)
A comprehensive persona prompt for an experienced business mentor — with explicit decision-making frameworks, coaching methodology (Socratic questioning, pattern recognition, resource allocation focus), escalation triggers, and success metrics. Designed to persist across multiple sessions.

**Why it's notable:** The escalation trigger section is unusually thoughtful: instead of just defining a persona, it specifies *when that persona should change register* — becoming more direct and urgent when specific warning signs appear. That's meta-behavior, not just character definition.

---

## Safety Inspection

### [`shower-inspection-ca.md`](./safety-inspection/shower-inspection-ca.md)
An evidence-only analysis prompt for residential shower construction photos — checking workmanship defects and California code violations. Enforces strict anti-hallucination rules, ties every finding to specific code citations, and outputs structured JSON with risk ratings.

**Why it's notable:** The anti-hallucination protocol is the standout feature. Seven explicit rules governing what the model can and cannot infer from visual evidence — including *"prefer silence over guesswork when confidence < threshold"* — make this one of the more disciplined high-stakes prompts in the collection. The conflict resolution section (photo evidence beats project context) is also smart design.

---

## Personal Tools

### [`conversation-psychoanalysis.md`](./personal-tools/conversation-psychoanalysis.md)
A suite of psychological analysis prompts — one generic version plus three context-specific variants (workplace, family, romantic/friendship) — for analyzing two-person conversations using Big Five personality theory, cognitive bias frameworks, attachment theory, and DSM-5-informed pattern recognition.

**Why it's notable:** The context variants show disciplined prompt design: same underlying analytical structure, but with domain-appropriate frameworks and different emphasis (e.g., organizational psychology for workplace, family systems theory for family dynamics). The instruction to "be willing to identify manipulative behaviors without seeking false balance" is an interesting explicit permission that changes output quality meaningfully.

### [`covert-checkin.md`](./personal-tools/covert-checkin.md)
A safety-focused prompt for generating coded communication scripts — designed for situations where a friend may be in danger but unable to speak freely. Creates plausible-deniability cover stories and coded escalation phrases from any reference domain.

**Why it's notable:** Context and mission matter here, not just technique. This is a personal safety tool — the domain variable (`[DOMAIN]`) lets you anchor the code in something culturally relevant to the relationship, which makes the resulting scripts actually usable.

---

## Schemas

### [`company-analysis.schema.json`](./schemas/company-analysis.schema.json)
The JSON schema that links `company-intelligence-brief.md` to `cover-letter-generator.md` — enabling structured output from one prompt to serve as verified, machine-readable input to the next. The confidence-labeling pattern (`"high" | "medium" | "low" | "speculation"`) runs throughout.

---

## On Converting These to Skills

Several of these prompts are natural candidates for packaging as Cowork skills — essentially giving them a trigger description, a SKILL.md wrapper, and surfacing them as one-click agents rather than copy-paste templates.

The best candidates:

| Prompt | Skill name idea | Why it works as a skill |
|--------|----------------|------------------------|
| `app-viability-assessment` | `app-viability` | Clear trigger ("evaluate my app idea"), parameterized, structured output |
| `company-intelligence-brief` → `cover-letter-generator` | `job-search-pipeline` | Three-stage pipeline (research → analyze → write) with handoffs |
| `expert-resume-optimization` | `resume-optimizer` | File-attachment workflow, iterative back-and-forth |
| `couture-photo-director` | `fashion-photo-director` | Image analysis + structured output, niche but powerful |
| `shower-inspection-ca` | `shower-inspector` | Photo upload workflow, JSON output, code compliance |
| `conversation-psychoanalysis` | `conversation-analyst` | Text-paste workflow, context variant selection |

---

## Repo Structure (Proposed)

```
/showcase
  README.md                          ← this file
  /market-research
    app-viability-assessment.md
    competitive-market-analysis.md
  /career
    company-intelligence-brief.md
    cover-letter-generator.md
    expert-resume-optimization.md
  /marketing
    couture-photo-director.md
    brand-foundations-evaluation.md
  /ai-behavior
    humanize-writing.md
    objective-skeptical-partner.md
    business-coach.md
  /safety-inspection
    shower-inspection-ca.md
  /personal-tools
    conversation-psychoanalysis.md
    covert-checkin.md
  /schemas
    company-analysis.schema.json
```
