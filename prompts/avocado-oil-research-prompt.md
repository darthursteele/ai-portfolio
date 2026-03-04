---
title: Online Avocado Oil Price Research
description: Comprehensive research prompt for finding the lowest cost-per-unit pure cold-pressed avocado oil with shipping included
domain: "shopping research"
variables:
  required:
    minimum_size: "Minimum container size in ounces"
    product_specs: "Specific product requirements (purity, processing method, grade)"
  optional:
    retailer_list: "List of retailers to check | default: Amazon, Walmart, Costco, manufacturer sites"
    max_results: "Maximum number of options to compare | default: 5"
    vendor_memberships: "Vendors the user has paid memberships with (e.g., Costco, Sam's Club, Thrive Market) | default: none"
tags:
  - shopping
  - price-comparison
  - food-products
  - research
  - citations
---

## Description
This prompt instructs an AI to conduct thorough price research for avocado oil purchases, with emphasis on verifiable information, confidence levels, and proper citations. It requires explicit statements about data reliability and prevents assumptions about pricing or availability. Use when you need accurate, current pricing data with full transparency about information sources.

## Example

```
minimum_size = "32 oz"
product_specs = "100% pure, cold-pressed, food grade"
retailer_list = "Amazon, Walmart, Costco, Whole Foods, Thrive Market, Chosen Foods, BetterBody Foods"
max_results = "5"
vendor_memberships = "Costco" # leave blank or omit if none
```


## Prompt
```text
Find me the least expensive per unit volume option for purchasing {product_specs} avocado oil online, with these specific requirements:

**Essential Criteria:**
- Must meet ALL specifications: {product_specs}
- Minimum purchase size: {minimum_size}
- Include shipping costs in the per-ounce calculation
- Must be available for online purchase and delivery
- Only include products with visible, verifiable pricing at time of research; do NOT present any product for which pricing cannot be obtained
- Exclude products that are available only through paid memberships unless the vendor is listed in {vendor_memberships}

**Research Tasks:**

1. Check these retailers: {retailer_list}

2. For each option found, provide:
   - Brand name and product verification (certifications like Non-GMO, USDA Organic, third-party testing)
   - Exact container size(s) available
   - Base price as displayed on vendor site
   - Shipping cost (exact amount or free shipping threshold)
   - Final cost per fluid ounce INCLUDING shipping
   - Direct URL link to the product page on vendor's website
   - Bulk discount or subscription savings if available
   - Date/time you accessed this information

3. Quality verification:
   - Note any reviews mentioning rancidity, packaging issues, or authenticity concerns
   - Include overall rating and number of reviews if available

**Critical Instructions:**

- DO NOT make assumptions about prices, availability, or shipping costs
- Do not include any product lacking current, visible pricing
- Do not include membership-only products unless that membership is explicitly listed in {vendor_memberships}; otherwise flag and exclude them
- Do not include any product that does not meet all of the specified product specs
- For EVERY piece of information, indicate confidence level:
  * HIGH confidence: Price visible on vendor website with screenshot/direct observation
  * MEDIUM confidence: Price from third-party aggregators or recent cached pages
  * LOW confidence: Information older than 7 days or indirect sources
  * NO DATA: Information could not be verified

- Citations required for ALL data:
  * Format: [Source: exact website URL, date accessed MM/DD/YYYY]
  * Place citation immediately after each price or claim
  * If information comes from reviews, note "per customer reviews on [site]"

- Shipping cost handling:
  * If exact shipping unavailable, state "Shipping cost could not be determined" and exclude the product if total price cannot be computed
  * Provide shipping calculator link if available
  * Note free shipping thresholds explicitly

- Access restrictions:
  * Note if membership required (e.g., "Requires Costco membership $60/year") and exclude even if included in {vendor_memberships}
  * Indicate if login needed to see prices
  * Flag any geographic restrictions

**Output Format:**

1. **Summary Table**
   | Brand | Size | Base Price | Shipping | Total $/oz | Confidence | Direct Link | Notes |
   |-------|------|------------|----------|------------|------------|-------------|-------|
   [Include top {max_results} options sorted by total $/oz]

2. **Top Recommendation**
   - Selected option and rationale
   - Confidence level in recommendation
   - Key assumptions (if any)
   - Access requirements or restrictions
   - Alternative if primary requires membership/special access

3. **Data Gaps**
   List any products considered but excluded due to missing price or membership restriction:
   - Product name
   - What information is missing or which membership is required
   - Why it couldn't be included

4. **Important Disclaimers**
   - Note if prices may vary by location
   - Mention any seasonal pricing patterns observed
   - Flag any time-sensitive promotions

Remember: It's better to explicitly state "could not determine" than to estimate or assume any information.
```
