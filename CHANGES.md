# Dataset Changes

## v3: Generated Context Fields

### What Changed

| Field | Location | Type | Distribution |
|-------|----------|------|-------------|
| `quantity` | `add_to_cart` context | int | Poisson(lambda=1.5), clamped [1, 5] |
| `discount_pct` | `purchase` context (recall) | decimal | Uniform(0.0, 0.15), round=2 |

**Before:** Every cart add was implicitly "1 item." Purchase decisions had no discount data. Basket analysis questions in the exercise header were unanswerable.

**After:** Each `add_to_cart` decision samples a quantity independently. Each `purchase` decision generates a discount percentage at recall time. The purchase context now contains four fields merged from two sources:

| Field | Source | Set When |
|-------|--------|----------|
| `price` | `entity.price` (stored in cart role) | Cart add |
| `quantity` | `generate` Poisson (stored in cart role) | Cart add |
| `payment_method` | `literal: credit_card` | Purchase recall |
| `discount_pct` | `generate` Uniform | Purchase recall |

### Data Profile

| Metric | v2 | v3 |
|--------|----|----|
| Unique customers | ~8,955 | ~9,007 |
| SCD-2 customer rows | ~13,999 | ~12,846 |
| Total decisions | ~200K | ~294K |

Quantity distribution (Poisson, lambda=1.5, clamped [1, 5]):

| qty | count | pct |
|-----|-------|-----|
| 1 | 40,127 | 55.8% |
| 2 | 18,002 | 25.0% |
| 3 | 9,006 | 12.5% |
| 4 | 3,422 | 4.8% |
| 5 | 1,342 | 1.9% |

Discount distribution: Uniform [0.00, 0.15], avg 0.074.

### Impact on Exercises

**Basket analysis (Exercise 8) is now answerable:**
- Average items per cart: `SUM(quantity)` grouped by `session_id`
- Average order value: `SUM(price * quantity * (1 - discount_pct))` per session
- Cart size vs conversion: compare `quantity` sums for sessions with/without purchase

**Revenue analysis gains depth:** Students can compute net revenue (`price * quantity * (1 - discount_pct)`), analyze discount distribution by segment/tier, and identify whether VIPs get larger discounts (they don't — discount is independent of actor properties, which is itself a finding).

**Existing exercises unaffected.** The new fields are additive context — no schema or behavioral changes.

---

## v2: Three-Year Simulation

### What Changed

| Setting | Before | After |
|---------|--------|-------|
| `start_date` | 2024-01-01 | 2022-03-01 |
| `end_date` | 2024-12-31 | 2024-12-31 |
| `initial` | 500 | removed (0) |
| `arrivals.rate` | 25/day | 5/day |
| Pinned VIP customers | 3 (Alexandra Chen, Marcus Johnson, Sofia Rodriguez) | removed |

### Why

**Day-1 spike eliminated.** 500 initial actors all entering the journey on Jan 1 created a 20x activity spike — the busiest day in the dataset was a simulation artifact, not a business event. Setting `initial: 0` and simulating from March 2022 builds the customer base organically through arrivals.

**Complete history invariant.** All actor state now derives from simulated events. No fabricated mid-process state. SCD-2 chains are intact from first arrival through final activity. See `docs/architecture/simulation.md` (Design Decisions: Why No Mid-Process State).

**Pinned VIPs removed.** With `total_purchases: 0`, pinned VIPs had no advantage over generated ones. The 0.5% VIP tier produces ~49 VIPs organically. ~33% convert to repeat purchasers (16 active VIPs with 10-13 purchases each). The other ~67% bounce on their first visit and never return — re-entry requires a prior purchase. Frame this as a VIP signup program with ~1/3 conversion.

**Arrival rate reduced (25 → 5)** to keep CSV file sizes manageable for GitHub hosting (~17 MB total). All analytical patterns remain clear at this volume.

### Event Restructuring

Baseline seasonal events now fire every year. Year-3-only events create disruptions students can discover.

**Baseline (all years):**
- `weekend_surge` — Sat/Sun 1.4x arrivals (unchanged, already recurring)
- `holiday_season` — Nov 15, 45-day bell curve 2.0x (unchanged, already seasonal)
- `summer_slowdown` — Jun 15, 60-day bell curve 0.75x (unchanged, already seasonal)
- `back_to_school` — Aug 1, 45-day ramp-up 1.5x (unchanged, already seasonal)
- `post_holiday_slump` — Jan 2-31 ramp-down 0.6x (was one_time → now seasonal)
- `black_friday` — Nov 29 arrivals 4.0x (was one_time → now seasonal)
- `cyber_monday` — Dec 2 arrivals 3.0x (was one_time → now seasonal)
- `market_growth` — 2% monthly exponential (extended from 2024-only to full simulation)

**Year 3 only (2024):**
- `spring_flash_sale` — Mar 15-17, doubles add_to_cart rate (unchanged)
- `checkout_outage_march` + `march_recovery` — Mar 15-16 (unchanged)
- `checkout_outage_august` + `august_recovery` — Aug 22-23 (unchanged)
- `black_friday_incident` — Nov 29 infrastructure degraded (unchanged)
- `vip_holiday_retention` — Dec 1-31 re-entry boost (was seasonal → now one_time)

### Impact on Exercises

**Exercise 3 ("busiest day"):** No longer Jan 1 artifact. Busiest day is now a real business event (Cyber Monday or holiday peak). The exercise shifts from "spot the simulation artifact" to "explain why this day was biggest."

**Exercise 6/17 (Black Friday):** Students can now compare Black Friday across 3 years — 2022 and 2023 show normal 4x spikes, 2024 is flat due to the infrastructure outage. The contrast is data-driven, not assumption-driven.

**Exercise 11 (VIPs):** ~49 generated VIPs replace the 3 pinned ones. 16 are active repeat purchasers. Students discover VIPs through queries, not pre-knowledge.

**All other exercises:** Work as-is. Business questions are date-agnostic.

### Dataset Profile

| Metric | Before | After |
|--------|--------|-------|
| Unique customers | ~12,986 | ~8,955 |
| SCD-2 customer rows | ~17,219 | ~13,999 |
| Total decisions | ~139K | ~200K |
| Fact table rows (after export) | ~139K | ~168K |
| VIPs | 77 (3 pinned) | 49 (all generated) |
| CSV total size | ~11 MB | ~17 MB |
| Simulation time | ~15s | ~23s |
| Time span | 1 year | 2 years 10 months |
