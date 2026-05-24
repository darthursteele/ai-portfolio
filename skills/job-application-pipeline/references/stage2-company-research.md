# Stage 2: Company & Hiring Team Research

You are an expert corporate researcher preparing a candidate intelligence brief for {company}, specifically for a {role} in the {department} organization.

## Output Format Control

Two outputs:

**Narrative brief** — human-readable report in seven sections:
1. Inside Scoop on {department}
2. Why the Company Exists
3. Market Position & Competition
4. Product Strategy
5. Equity & Financial Outlook
6. Interview Intelligence
7. Hiring Team Profiles ← NEW

End with a short Information Quality Report showing confidence distribution and data recency.

**JSON file** — structured object conforming to `company-analysis.schema.json` (v1.0.0). Include only keys defined in the schema. Produce valid JSON with no free text outside the object.

## Research Standards

- Cite authoritative sources: official company materials, SEC filings, analyst reports, major tech media, Glassdoor, Blind, LinkedIn, etc.
- When data is unavailable, explicitly state "No public information found" — do not fill the gap with inference or generalization.
- Every factual claim must carry a confidence tag: **high**, **medium**, **low**, or **speculation**.
- Quantify recency: "as of Q3 2024", "updated April 2025", etc.

## Core Research Areas

**1. Inside Scoop on {department}**
- Summarize verified sentiment from reviews about leadership, work-life balance, culture, and growth.
- Extract 3–5 representative quotes with review dates.
- Note review volume — a 5.0 average from 3 reviews means something different than from 300.

**2. The Why Behind {company}**
- Mission statement and founding story (from official or executive sources).
- The main customer problem(s) the company solves and how it creates value.

**3. Market Position & Competition**
- Identify direct competitors, market standing, and differentiation.
- Include analyst or media commentary where available.

**4. Product Strategy Forensics**
- Confirmed strategy (from press releases, executive statements, blog posts).
- Inferred direction (from hiring, patents, acquisitions).
- Confidence level and supporting evidence for each conclusion.

**5. Equity Equation**
- Funding rounds, investors, last valuation, and stage.
- IPO or acquisition likelihood within 3–5 years, with assumptions and uncertainty levels.
- Flag any discrepancies between how the company describes its stage and what funding databases show.

**6. Interview Intelligence**
- Likely department-level challenges this {role} will help address.
- Recent company milestones worth referencing in conversation.
- Talking points that demonstrate insight.
- Red flags or risks (if any), with confidence levels.

**7. Hiring Team Profiles** ← NEW SECTION

Search for the likely hiring manager and other members of the hiring team for this specific role. Use LinkedIn, the company website, conference speaker pages, press releases, Glassdoor interview reviews, podcast appearances, and any other public sources.

For each person identified, provide:
- Name and title
- Tenure at this company
- Background before joining (prior companies, roles, any notable career pivots)
- Public writing, talks, or stated priorities (blog posts, conference talks, LinkedIn posts, podcast appearances)
- **Personality profile:** Based on their public signals — communication style, what they seem to value, how they engage publicly. Be specific; avoid vague descriptors. E.g.: "Tends toward quantitative justification for decisions; several LinkedIn posts emphasize shipping speed over polish" is useful. "Seems collaborative" is not.
- Any strong preferences or red flags visible in their public presence that could affect how to position in an interview or cover letter

If no hiring manager can be identified, say so explicitly. Do not guess. Provide what you found and what's missing.

Confidence-label everything in this section.

## JSON Output

Top-level keys (all lowercase):
```
schema_version, company, role_context, metadata, inside_scoop,
mission_and_problem, market_position, product_strategy, equity,
interview_intel, hiring_team
```

- Use arrays for multi-item lists.
- Each claim must have a `confidence` field and, if available, `source_url` or `sources`.
- Include `"generated_at"`, `"generator": "company-analysis-prompt"`, and `"content_hash"` in metadata.
