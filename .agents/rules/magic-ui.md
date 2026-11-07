# Magic UI & 21st MCP — UI Component Standards

When the user asks to build, update, or design user interfaces, web applications, landing pages, dashboards, or frontend elements (pricing tables, navbars, hero blocks, cards, modals, interactive animations):

## 1. UI Component Search & Reuse First
- Do NOT write boilerplate, unstyled, or mundane UI components from scratch.
- Query 21st / Magic MCP (`search` tool or CLI `21st search "<query>"`) to find production-grade React + Tailwind + shadcn-compatible components.
- Inspect and retrieve component code via `get_component` (or CLI `21st get <id>`), and adapt styling/tokens to match the current project.

## 2. Brand & Technology Logos
- When inserting company, cloud, database, or tool logos (e.g., React, Stripe, GitHub, Supabase, Google, OpenAI, Tailwind), use `search_logo` or CLI `21st logo "<brand>"`.
- It returns clean, high-precision SVG JSX components with light/dark mode support. Never approximate logos by hand.

## 3. Custom Generation & Refinement
- When custom layouts or specialized designs are needed, check `get_usage` and use `generate` (or CLI `21st generate "<prompt>"`) to synthesize tailored UI variants with 21st AI.
- Iterate with `iterate_generation` to incorporate user feedback.
