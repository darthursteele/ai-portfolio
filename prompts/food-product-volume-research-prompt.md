---
title: Online Food Product Price Research (Volume-Based)
description: Comprehensive research prompt for finding the lowest cost-per-unit volume food products with shipping included
domain: shopping research
variables:
  required:
    - {product_name}: Name of the food product (e.g., olive oil, maple syrup, honey)
    - {minimum_volume}: Minimum container size with units (e.g., 32 oz, 1 liter, 500 ml)
    - {product_specs}: Specific product requirements (e.g., organic, cold-pressed, grade A, etc.)
  optional:
    - {retailer_list}: List of retailers to check | default: Amazon, Walmart, Costco, Whole Foods, manufacturer sites
    - {max_results}: Maximum number of options to compare | default: 5
    - {volume_unit}: Preferred unit for price comparison | default: per fluid ounce
tags: [shopping, price-comparison, food-products, research, citations, bulk-buying]
---

## Description
This prompt instructs an AI to conduct thorough price research for volume-based food product purchases (oils, syrups, vinegars, sauces, etc.), with emphasis on verifiable information, confidence levels, and proper citations. It requires explicit statements about data reliability and prevents assumptions about pricing or availability. Use when you need accurate, current pricing data for any liquid or volume-measured food product with full transparency about information sources.

## Example
```
product_name = "extra virgin olive oil"
minimum_volume = "1 liter"
product_specs = "first cold-pressed, organic certified, single origin"
retailer_list = "Amazon, Costco, Whole Foods, Trader Joe's, California Olive Ranch, Colavita"
volume_unit = "per fluid ounce"
max_results = "5"
```

## Prompt
```text
Find me the least expensive per unit volume option for purchasing {product_name} online, with these specific requirements:

**Essential Criteria:**
- Product: {product_name}
- Must meet ALL specifications: {product_specs}
- Minimum purchase size: {minimum_volume}
- Include shipping costs in the {volume_unit} calculation
- Must be food grade and safe for consumption
- Must be available for online purchase and delivery

**Research Tasks:**

1. Check these retailers: {retailer_list}

2. For each option found, provide:
   - Brand name and product verification (certifications like USDA Organic, Non-GMO, quality grades, third-party testing)
   - Exact container size(s) available (in fl oz, liters, gallons, or ml)
   - Base price as displayed on vendor site
   - Shipping cost (exact amount or free shipping threshold)
   - Final cost {volume_unit} INCLUDING shipping
   - Direct URL link to the product page on vendor's website
   - Bulk discount or subscription savings if available
   - Expiration date or shelf life if listed
   - Date/time you accessed this information

3. Quality verification:
   - Note any reviews mentioning quality issues (rancidity, contamination, off-flavors, separation)
   - Packaging concerns (leaking, damaged containers, poor seals)
   - Authenticity or dilution concerns
   - Include overall rating and number of reviews if available

**Critical Instructions:**

- DO NOT make assumptions about prices, availability, or shipping costs
- For EVERY piece of information, indicate confidence level:
  * HIGH confidence: Price visible on vendor website with screenshot/direct observation
  * MEDIUM confidence: Price from third-party aggregators or recent cached pages
  * LOW confidence: Information older than 7 days or indirect sources
  * NO DATA: Information could not be verified

- Citations required for ALL data:
  * Format: [Source: exact website URL, date accessed MM/DD/YYYY HH:MM timezone]
  * Place citation immediately after each price or claim
  * If information comes from reviews, note "per customer reviews on [site]"

- Shipping cost handling:
  * If exact shipping unavailable, state "Shipping cost could not be determined"
  * Provide shipping calculator link if available
  * Note free shipping thresholds explicitly
  * Include any temperature-controlled shipping requirements/costs for perishables

- Access restrictions:
  * Note if membership required (e.g., "Requires Costco membership $60/year")
  * Indicate if login needed to see prices
  * Flag any geographic restrictions or delivery limitations
  * Note if product requires age verification

**Output Format:**

1. **Summary Table**
   | Brand | Product Name | Size | Base Price | Shipping | Total ${volume_unit} | Confidence | Direct Link | Certifications |
   |-------|--------------|------|------------|----------|-------------------|------------|-------------|----------------|
   [Include top {max_results} options sorted by total ${volume_unit}]

2. **Top Recommendation**
   - Selected option and rationale
   - Confidence level in recommendation
   - Key assumptions (if any)
   - Access requirements or restrictions
   - Alternative if primary requires membership/special access
   - Storage recommendations if provided by vendor

3. **Data Gaps**
   List any products where complete information unavailable:
   - Product/Brand name
   - What information is missing
   - Why it couldn't be obtained

4. **Important Disclaimers**
   - Note if prices may vary by location
   - Mention any seasonal pricing patterns observed
   - Flag any time-sensitive promotions
   - Temperature/shipping restrictions for perishable items
   - Bulk purchase considerations (storage life vs. volume savings)

5. **Unit Conversion Reference**
   Provide conversions if products listed in different units:
   - 1 gallon = 128 fl oz = 3.785 liters
   - 1 liter = 33.814 fl oz
   - 1 ml = 0.033814 fl oz
   - Show calculations for any unit conversions performed

Remember: It's better to explicitly state "could not determine" than to estimate or assume any information. Always show the math for unit price calculations.
```
