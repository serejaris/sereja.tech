# Design QA — Reading Ledger

## Target and implementation

- Selected target: `/Users/ris/.codex/generated_images/019fce7f-2cc1-7d01-821d-af6324ab5440/exec-8308586e-82bc-4015-bb7b-5d6dd7457c88.png`
- Target pixels: `936 × 1680`
- Implementation URL: `http://127.0.0.1:1313/blog/best-practices-code/`
- Implementation capture: `/Users/ris/.codex/visualizations/2026/08/04/019fce7f-2cc1-7d01-821d-af6324ab5440/reading-ledger-exact-936x1680-v5.png`
- Implementation pixels and CSS viewport: `936 × 1680`
- Density normalization: source and implementation compared at the same pixel size and viewport state.
- Full-view comparison: `/Users/ris/.codex/visualizations/2026/08/04/019fce7f-2cc1-7d01-821d-af6324ab5440/reading-ledger-exact-comparison-v5.png`
- Focused bottom comparison: `/Users/ris/.codex/visualizations/2026/08/04/019fce7f-2cc1-7d01-821d-af6324ab5440/reading-ledger-related-comparison-v3.png`
- Mobile capture: `/Users/ris/.codex/visualizations/2026/08/04/019fce7f-2cc1-7d01-821d-af6324ab5440/reading-ledger-mobile-480x844-final.png`

## Review

| Area | Result | Evidence |
| --- | --- | --- |
| Layout | passed | Fixed author rail, article column, and sticky TOC match the selected three-column target at `936 × 1680`. |
| Typography | passed | Inter Tight display headings and JetBrains Mono reading text reproduce the target hierarchy and density. |
| Color and borders | passed | Graphite surfaces, warm orange accent, thin dividers, and square geometry match the target language. |
| First-screen rhythm | passed | Title, metadata, cover, opening, first heading, and comparison table align closely in the combined v5 capture. |
| Article navigation | passed | Desktop TOC has five links and active-state tracking; mobile TOC opens and exposes the same five links. |
| Heading permalinks | passed | Five visible H2 anchors resolve to their real section hashes. |
| Bottom modules | passed | Previous/next navigation, exactly three related rows, and tag links are present and visually match the focused target region. |
| Responsive behavior | passed | At a `480 × 844` CSS viewport the layout becomes one column, the right rail is hidden, body text is `14px`, and document width equals viewport width. |
| Interaction and console | passed | Copy-link feedback, TOC navigation, heading anchors, and route smoke were exercised; the article console had no errors or warnings. |
| Content integrity | passed | The complete Russian article remains intact. Its greater length moves the bottom modules below the first `1680px`; this is an intentional content constraint. |
| Assets and icons | passed | The cover is a dedicated `1200 × 300` WebP asset; interface icons come from the Phosphor icon set. |

## Comparison history

1. `v3`: the combined comparison showed narrow side rails, a loose header rhythm, and an overly tall table. Severity: P2.
2. `v4`: column proportions and header spacing were corrected; content density still ran taller than the target. Severity: P2.
3. `v5`: responsive type scaling, paragraph rhythm, heading spacing, and table density were corrected. No P0, P1, or P2 findings remain.

final result: passed
