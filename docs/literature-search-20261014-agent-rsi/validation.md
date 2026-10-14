# Local verification — 2026-10-14, revised argument

- Jekyll build passed to `/tmp/scodive-benchmark-blog-v2` after the final bilingual prose edits and five-source follow-up.
- Preview: http://localhost:4173/what-evolves-in-self-evolving-agents/
- Post date remains October 14, 2026; it appears on the Blogs page.
- English is the default; the Chinese button changes visible content and document title. Both versions include the revised joint-optimization argument and the same 33 reference IDs.
- Each language contains seven tables, two figures and four expandable paper-guide groups. A live click opened the Chinese skill group and exposed the newly added VaG row.
- Static check: no duplicate IDs or broken local links/anchors; 33 structured source records; the audit folder is excluded from the generated site.
- Images are not wrapped in links. Mobile picture sources select the compact diagrams.
- Desktop at 1280px: body text 18.4px, no page-width overflow. The article anchor handler places the selected heading 80px below the top, clear of the site navigation.
- Mobile at 390px: body 16px, tables stay inside 343px scrolling containers (760px example, 700px comparison tables), no page-width overflow. The Chinese Pareto diagram was visually inspected and is legible.
- Illustrative arithmetic: P1/P2 scores are 87.6/87.2 at a 0.1 call penalty and 82/84 at 0.5. Chart values agree with the example table: P0 (6,80), P2 (8,88), P1 (14,89). P1 is marked as failing the authorization condition.
- Existing tracked files have no modifications. Changes are limited to the new post, its assets and this excluded review folder.
- No commit, push or deployment performed.

Current screenshots: `preview-desktop-revised.png`, `preview-mobile-revised.png`.
