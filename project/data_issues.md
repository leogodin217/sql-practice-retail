# Data Issues

1. **No multi-session non-buyers.** Every customer with 2+ sessions has at least one purchase (494/494). All 8,411 non-buyers have exactly 1 session. Real e-commerce data would have repeat visitors who never convert.

2. **Discounts are uniformly random.** `discount_pct` is U(0, 0.15) and independent of segment, tier, product, and basket size. There is no targeted discounting -- every customer gets the same distribution. This limits exercises that try to analyze discount strategy effectiveness.

3. **Cart size doesn't predict conversion.** `quantity` on `add_to_cart` is sampled independently from the purchase decision, producing flat ~9% conversion across all cart sizes. Real data would likely show some relationship.

4. **All customers are active.** The `active` column in `dim_customer` is `true` for all 13,294 rows. No customer has ever been deactivated.

5. **No product SCD history.** `dim_product` has `valid_from`/`valid_to` columns but all 203 rows are current (no historical versions). Product prices and margins never change.

6. **Duplicate product names across SKUs.** 48 product names map to multiple SKU IDs (e.g., "Classic Soundbar" is both SKU_00057 and SKU_00083). Co-occurrence queries grouping by name silently merge distinct SKUs.
