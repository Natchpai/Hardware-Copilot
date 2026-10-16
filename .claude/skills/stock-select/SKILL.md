---
name: stock-select
description: >-
  Finds and filters electronic parts that can be sourced from DigiKey, Mouser,
  LCSC, or the JLCPCB Parts Library. Use when the user asks for in-stock parts,
  supplier-specific alternatives, availability, price breaks, MOQ, or JLCPCB
  assembly-ready parts. Not for engineering fit (use component-select) or a
  price table for known part numbers (use price-compare-table).
argument-hint: "[function | MPN | requirements] [supplier] [quantity]"
---

# Stock-Based Component Selection

Find a practical, currently sourceable shortlist. This skill focuses on **supplier
inventory and procurement constraints**, not on defining the electrical design.
Do not hardcode preferred manufacturers, part numbers, or circuit categories.

## Scope and boundaries

- Supported sources: **DigiKey, Mouser, LCSC, and JLCPCB Parts Library**.
  Search only the suppliers requested by the user; otherwise consider all
  applicable suppliers. Do not assume they have equivalent catalogs.
- Distinguish **supplier/distributor stock** from **the user's privately owned
  inventory**. Do not claim access to personal stock records unless supplied.
- Supplier availability, price, and lead time change. Verify against current
  supplier product listings, authorized APIs, or user-provided exports; always
  identify the source and observation date. If live access is unavailable, use
  `NOT_VERIFIED` rather than inventing figures.
- Source only genuine, traceable parts where provenance can be established.
  Check exact **manufacturer MPN including suffix** and distinguish it from
  supplier SKU (DigiKey/Mouser number, LCSC code, JLCPCB part number).
- Never treat *available to order* as *on-hand inventory*, or *listed* as
  *available for automated assembly*. Supplier stock is not a reservation.
- Do not order, reserve, upload a BOM, sign into accounts, or change a KiCad
  project without explicit authorization. Inspection remains read-only.
- Use `component-select` for design-wide functional discovery and trade-offs;
  use `component-check` for detailed datasheet, package, footprint, and pinout
  validation. Passing stock filters does **not** mean electrically approved.

## Workflow

1. **Scope the purchase.** Identify the functional requirement or existing MPN,
   mandatory electrical/package constraints, target quantity, shipment region,
   budget, desired delivery date, and whether JLCPCB assembly is required.
   If unspecified, state assumptions and avoid presenting absolute total costs.
2. **Search supplier catalogs.** Search exact MPN first for replacements or BOM
   sourcing; use parametric/functional searching when discovering alternatives.
   Query the requested suppliers and capture the exact supplier listing URL or
   verifiable source record for each candidate.
3. **Normalize identifiers.** Record manufacturer, complete orderable MPN,
   supplier, supplier SKU, package, lifecycle when available, and any listing
   ambiguities. Never merge parts solely because descriptions look alike.
4. **Apply hard filters.** Reject candidates failing required electrical,
   environmental, packaging, assembly, traceability, or lead-time constraints.
   Flag absent critical evidence as `NOT_VERIFIED` rather than PASS.
5. **Check procurement conditions.** Distinguish current sellable quantity from
   non-stock/lead-time/backorder, order increments, MOQ, packaging (cut tape,
   reel, tray), price breaks at requested quantity, currency, and shipping-region
   limitations. Do not present estimated tax or shipping as confirmed.
6. **Handle JLCPCB separately.** Check the **JLCPCB assembly parts library**
   directly for the JLCPCB part code, assembly eligibility, category (such as
   Basic or Extended when available), stock usable for the intended PCBA
   order, and potential sourcing/pre-order/consignment constraints. **LCSC
   availability alone does not prove JLCPCB assembly availability.** Do not
   assume a JLCPCB library part is available for separate shipment.
7. **Shortlist and stop.** Present 2–3 qualified, meaningfully different
   purchase options, or clearly state that none pass. Prefer practical
   availability over theoretical catalog breadth, but never override mandatory
   engineering constraints to favor stock.

## Output contract

Provide a concise comparison with:

- **Search context:** requirements, target quantity, destination/region,
  suppliers queried, and date/time checked.
- **Candidate table:** exact MPN, supplier SKU, source, stock status/quantity,
  price at relevant quantity, MOQ/increment, package, and assembly eligibility
  where applicable. Use `NOT_VERIFIED` for missing fields.
- **Recommendation:** `RECOMMENDED`, `ALTERNATIVE`, `REJECTED`, or
  `NOT_VERIFIED`, with a reason and any important sourcing risk.
- **Next step:** critical electrical/package verification or reconfirmation of
  inventory immediately before purchase or PCBA submission.

Never claim a candidate is pin-compatible, drop-in, or approved merely because
it is in stock. If no live supplier data is available, provide a clearly
labeled sourcing plan or provisional shortlist, not fabricated availability.
