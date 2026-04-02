---
title: Mobile App Idea Viability Assessment
description: Systematically evaluate the market viability of a mobile app concept with standardized scoring criteria for comparative analysis across multiple ideas
domain: product-strategy
variables:
  required:
    - {app_concept}: Brief description of the mobile app idea and core functionality
    - {target_market}: Primary target audience or user segment
    - {geographic_scope}: Market region for analysis (e.g., "North America", "global", "Europe")
  optional:
    - {monetization_model}: Preferred revenue approach if known | default "analyze optimal options"
    - {platform_preference}: Target platform preference | default "iOS and Android"
    - {competitive_benchmark}: Specific competitor to benchmark against | default "category leaders"
tags: [app-viability, market-assessment, revenue-potential, competitive-analysis, product-validation]
---

## Description
This prompt provides a standardized framework for evaluating mobile app ideas, focusing exclusively on market viability, revenue potential, and competitive positioning. Each assessment generates consistent scoring metrics that enable direct comparison across multiple app concepts, helping prioritize which ideas warrant further development.

## Example
```
app_concept = "AI-powered meal planning app that generates shopping lists and reduces food waste"
target_market = "busy professionals aged 25-45 with household incomes above $50k"
geographic_scope = "North America"
monetization_model = "freemium with premium recipe collections"
platform_preference = "iOS first, then Android"
```

## Prompt
```text
Conduct a comprehensive viability assessment for the following mobile app concept: {app_concept}

Target audience: {target_market}
Geographic scope: {geographic_scope}
Platform focus: {platform_preference}
Monetization approach: {monetization_model}

Structure your analysis using the standardized format below, including numerical scores for comparative analysis:

## Executive Summary
**Viability Score: [X/100]**
- One-paragraph summary of overall market opportunity and key findings
- Primary recommendation: Proceed/Proceed with modifications/Do not pursue

## Market Appeal Assessment

**Market Size & Opportunity**
- Total Addressable Market (TAM) size and growth rate
- Serviceable Addressable Market (SAM) for {target_market}
- Market maturity stage (emerging/growth/mature/declining)

**User Demand Indicators**
- Evidence of existing demand or pain points in the market
- Search volume trends and keyword analysis for related terms
- Social media discussions, forums, or communities around the problem space
- Adjacent market growth indicating potential demand

**Market Appeal Score: [X/25]**
Rate based on: Market size (5 pts), Growth potential (5 pts), User demand strength (5 pts), Market timing (5 pts), Target segment attractiveness (5 pts)

## Revenue Potential Analysis

**Monetization Viability**
- Optimal revenue model(s) for this concept and target market
- Average revenue per user (ARPU) benchmarks from similar apps
- Customer lifetime value (LTV) estimates based on user behavior patterns
- Multiple revenue stream opportunities

**Market Pricing Analysis**
- Pricing tolerance in this category and target segment
- Freemium vs. paid model success rates for similar concepts
- In-app purchase potential and typical conversion rates
- Subscription model viability and churn expectations

**Revenue Scale Potential**
- Path to $1M, $10M, and $100M+ annual revenue
- Time-to-revenue projections and growth trajectory
- Market share required to achieve significant revenue milestones

**Revenue Potential Score: [X/35]**
Rate based on: Monetization model fit (10 pts), ARPU potential (10 pts), Revenue scalability (10 pts), Multiple revenue streams (5 pts)

## Competitive Landscape Assessment

**Direct Competition Analysis**
- Identify 3-5 direct competitors and their market positions
- Competitive strengths and weaknesses relevant to your concept
- Market share distribution among existing players
- Barriers to entry and competitive moats

**Differentiation Opportunity**
- Clear gaps in current market offerings
- Unique value proposition potential vs. existing solutions
- Defensibility of proposed differentiation
- First-mover advantage opportunities

**Competitive Positioning**
- Realistic market share potential within 2-3 years
- Required investment to compete effectively
- Risk of incumbent response or market saturation

**Competitive Score: [X/25]**
Rate based on: Market gaps (10 pts), Differentiation strength (5 pts), Competitive intensity (5 pts), Defensibility (5 pts)

## Risk & Opportunity Factors

**Market Risks**
- Platform dependency risks (App Store policies, algorithm changes)
- Market saturation potential
- Economic sensitivity of target market
- Regulatory or compliance considerations

**Strategic Opportunities**
- Partnership or integration possibilities
- Adjacent market expansion potential
- Platform or technology trend alignment
- Viral or network effect potential

**Risk-Adjusted Score: [X/15]**
Rate based on: Risk mitigation (5 pts), Strategic opportunities (5 pts), Market resilience (5 pts)

## Comparative Analysis Metrics

Present key metrics in standardized format for cross-idea comparison:

| Metric | Score | Benchmark |
|--------|-------|-----------|
| Overall Viability | [X/100] | 70+ recommended for pursuit |
| Market Appeal | [X/25] | Attractiveness of target market |
| Revenue Potential | [X/35] | Scale and monetization strength |
| Competitive Position | [X/25] | Differentiation and market gaps |
| Risk-Adjusted Opportunity | [X/15] | Strategic value vs. risks |
| Estimated TAM | $[X]B | Total addressable market size |
| 3-Year Revenue Potential | $[X]M | Realistic revenue projection |
| Time to Market Viability | [X] months | Estimated time to meaningful traction |

## Strategic Recommendation

**Priority Level: [High/Medium/Low]**
- Specific rationale for recommendation
- Key success factors if pursuing this concept
- Suggested modifications to improve viability score
- Next steps for validation or market entry

**Investment Thesis**
- Why this app concept could succeed in the current market
- Critical assumptions that must prove true for success
- Comparable success stories in similar categories

Base all analysis on current market data from the past three years and cite sources where possible. Focus exclusively on market viability—assume implementation is feasible and concentrate on commercial potential.
```