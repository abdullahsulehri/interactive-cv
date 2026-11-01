# Design rules: abdullahsulehri.github.io/interactive-cv

**For anyone editing this site, person or AI, in any chat or tool:** read this file before changing anything. Every change must follow these rules. A change that breaks a rule is a bug, even if it looks fine on one screen. Before publishing, run the audit (see "Quality gate") and fix everything it reports.

The site is one page (`index.html`). Text and data live in `content.json`. Images and logos live in `assets/`.

---

## 1. Fit and layout

| # | Rule |
|---|---|
| L1 | No sideways scrolling at any width from 320px to 2560px. |
| L2 | On laptops 720px tall or more, the hero (name, all 6 tiles, stats, the full figure including feet) fits the first screen. |
| L3 | Nothing sits under the top or bottom bar at rest. The page ends above the bottom bar. |
| L4 | Laptop layout starts at 900px wide; below that is the phone layout. |
| L5 | Cards in the same group are the same height. |
| L6 | Logo rows show whole rows only, with the rest behind "Show all". Card grids may end with a partial last row, aligned left, with cards at normal size. |

## 2. Text

| # | Rule |
|---|---|
| T1 | No accidental cuts. Text is shown in full, or cut at a full line with "…" plus a "Read more" control. |
| T2 | An optional line (such as a tile teaser) that can't show in full is hidden completely, never half-shown. |
| T3 | Paragraph lines are max ~75 characters wide on laptop. |
| T4 | Type scale only: 11 (labels) · 12 · 13 · 14 (body, laptop) / 15 (body, phone) · 16 · 18 · 20 · 24, plus calculated heading and stat sizes. No other sizes. |
| T5 | Long words and names wrap inside their card and never push outside it. |
| T6 | No clipped letters. Headings leave room for letters that extend above or below the line. |

## 3. Alignment (applies to every new element)

| # | Rule |
|---|---|
| A1 | Icons inside buttons, pills and circles are drawn shapes, never typed characters (+, →, ↗). Use the `.ic` element with a `data-g` name (plus, x, right, left, ext, down, up, minus); it centres the icon exactly. |
| A2 | Single-line labels in buttons, pills and chips are centred on their capital letters: `text-box: trim-both cap alphabetic`. If a label must hide overflow (for the expanding pill), use `overflow-x: clip; overflow-y: visible` so descenders (g, p, y) are never cut. |
| A3 | Every control centres its content vertically (`align-items: center`). Initials in avatar circles are centred both ways. |
| A4 | Tolerance is 1px. The audit checks icon and label centring with the real fonts loaded. |

## 4. Components

| # | Rule |
|---|---|
| C1 | Three button types only: primary (filled, 40px), secondary (outline, 40px), and the action pill (32px, icon + label). Labels are 13px. |
| C2 | Every expand control has a label, shows its open state, and has a clear way back (Hide, Back, Collapse all, ×) that returns exactly the previous state. |
| C3 | On phone, every tappable thing has at least a 44×44px tap area, even if it looks smaller. |
| C4 | Highlight rule. Laptop: hovering lights the whole card or row; only "Book a call" also lights when it reaches the middle of the screen. Phone: whatever is at the middle line lights up. Hover always wins. |
| C5 | Fixed elements (bars, panels) never cover text a visitor needs. |
| C6 | The same component has the same internal structure at every width. Nothing rearranges because one item's text is longer. |
| C7 | Each section has one action slot, at the top right of its heading (e.g. View on LinkedIn, Expand all). On phone it sits under the heading. |

## 5. Panels

| # | Rule |
|---|---|
| P1 | Panel content aims for max ~1.3 panel-heights of scrolling on a 1366×768 laptop. |
| P2 | While a panel scrolls, its header (title, Prev/Next, Close) stays visible. |
| P3 | Back and Close are labelled buttons. The phone's Back button closes the panel instead of leaving the site. |
| P4 | Sticky headers sit flush with the top edge of their scroll area, on a solid background. Nothing may show above them. |

## 6. Motion

| # | Rule |
|---|---|
| M1 | Three speeds only: 0.2s (hover, colour), 0.4s (expand, open), 1.2s (story line). |
| M2 | One easing curve: `var(--ez)`. |
| M3 | Motion off (the Motion toggle or the device's reduced-motion setting) means no movement, only instant changes. |
| M4 | Animations only move or fade things; they never resize layout under the reader. |

## 7. Colour

| # | Rule |
|---|---|
| K1 | The accent colour has three jobs: highlighted state, primary action, key numbers. Never decoration. |
| K2 | All text passes 4.5:1 contrast in all six accent colours (Blue, Teal, Terracotta, Burgundy, Plum, Ochre). |
| K3 | Logos rest in ink and turn the accent when highlighted. |
| K4 | Page backgrounds use the two paper colours only, alternating by section. No dark sections. |
| K5 | Green is used for WhatsApp only. |

## 8. Content

| # | Rule |
|---|---|
| D1 | Repeated items use one fixed format. Testimonial: name / position / company, no year. Certificate: issuer / title / course count. Education: qualification / institution / year. |
| D2 | Parallel cards get equal-length copy. AI benefit lines fit 2–3 lines; "What it does" fits max 3 lines. Exactly 2 tool tags per AI card. |
| D3 | No company-internal data, no "MOT" naming, no "chartered accountant" in education. |

## 9. Quality gate

| # | Rule |
|---|---|
| Q1 | Nothing is published until the audit passes at all 9 sizes: 360×740, 390×844, 768×1024, 1024×768, 1280×720, 1366×768, 1440×900, 1920×1080, 2560×1440. |

The audit checks: sideways scrolling, cut text, half-shown teasers, bar overflow, nav overflow, script errors, clipped letters in headings, icon and label centring (with the real fonts), avatar initials centring, and sticky-header gaps. A person still checks motion and feel in a real browser.

## 10. Source code

These keep the code clean every time a feature or content is added. `tools/lint.py` checks them automatically.

| # | Rule |
|---|---|
| S1 | One `<style>` block. No new `!important`, duplicate selectors, `setTimeout`s, inline `style=` attributes or colour literals: their counts in `tools/lint-budget.json` can go down, never up. Fix specificity or order instead of forcing. |
| S2 | Layers and corners come from tokens only: `--z-*` for z-index, `--r` / `--r-*` for border-radius. Colours come from the `:root` and theme tokens. |
| S3 | Font sizes follow T4. Named exceptions: 9.5px dot-to-pill micro label (grows inside the fixed pill, so no layout moves), 34px loader monogram, 64px testimonial quote mark. |
| S4 | Every transition and animation uses `var(--ez)` and a T-rule speed (.2s / .4s / 1.2s). Named exception: 2.4s loader pulse loop. |
| S5 | Breakpoints come from the fixed list in `tools/lint.py`. Laptop starts at `min-width:900px`; phone is `max-width:899.98px`. A new breakpoint needs a rule change first. |
| S6 | Text lives only in `content.json`. After editing it, run `python tools/sync_content.py` so the copy inside `index.html` matches. US spelling (official course titles excepted). Rules D1–D3 are checked automatically. |
| S7 | No leftover build markers, `console.log`, `TODO`; every referenced file exists; JavaScript passes a syntax check. |
| S8 | Before publishing run `python tools/check.py` (sync + lint + 9-size audit + alignment report). GitHub runs the same check on every push; a red ✗ on the commit means a rule is broken. |

## How to add content or a feature

1. Text only: edit `content.json` → `python tools/sync_content.py` → `python tools/check.py`.
2. New styles: add them inside the one `<style>` block, next to the related component, using tokens. Never add a second block or an override layer at the end.
3. New behaviour: add it next to the related code in the main script, not in a new "layer" at the end.
4. CV PDF: edit `tools/build_cv.py` → `python tools/build_cv.py` → it must stay 2 pages and the QR must scan.
5. Preview, approve, then push. If the GitHub check turns red, fix before sharing the link.

## How to undo a release

Every release is tagged (`v9`, `v10`, `v11`, …). To roll the live site back: `git checkout main && git reset --hard v10 && git push --force` (replace `v10` with the version to return to). GitHub Pages updates within a few minutes.
