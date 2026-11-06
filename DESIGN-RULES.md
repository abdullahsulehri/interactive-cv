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
| A5 | Items in one row line up part by part: when a label or title wraps in one item, its neighbours reserve the same height, so titles start on the same line. |

## 4. Components

| # | Rule |
|---|---|
| C1 | Three button types only: primary (filled, 40px), secondary (outline, 40px), and the action control (32px): a dot with an icon that opens into a labelled pill (section 11). Labels are 13px. |
| C2 | Every expand control has a label (shown when its pill opens, always read by screen readers), shows its open state (filled pill reading Hide / ×), and has a clear way back that returns exactly the previous state. |
| C3 | On phone, every tappable thing has at least a 44×44px tap area, even if it looks smaller. |
| C4 | Highlighting follows the focus system in section 11, everywhere: home page and every panel. Only one place is highlighted at a time (a grid row counts as one place); nothing stays highlighted permanently (a "current" marker uses a small label, not a highlight). |
| C5 | Fixed elements (bars, panels) never cover text a visitor needs. |
| C6 | The same component has the same internal structure at every width. Nothing rearranges because one item's text is longer. |
| C7 | Each section has one action slot, at the top right of its heading (e.g. View on LinkedIn, Expand all). On phone it sits under the heading. |
| C8 | A control whose label swaps (Expand all ↔ Collapse all, Show ↔ Hide, Show all 25 brands ↔ Show fewer) fits its current label: on a swap the pill glides to the new width (.4s), so there is never a gap after a short label and nothing jumps. |

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
| K1 | The accent colour has four jobs: focus state (section 11), highlighted/open state, primary action, key numbers. Never decoration. |
| K2 | All text passes 4.5:1 contrast (large text 3:1) in all six accent colours, in both its resting and highlighted state. `tools/contrast.py` checks this. |
| K3 | Brand and tool logos rest in grey (at least 3:1 contrast) and switch to their own brand colour when in focus. A brand colour too light for 3:1 is darkened automatically; a brand with no known colour uses the accent. |
| K4 | A certificate earned from a set of courses is shown as one unit: a tinted header with its type, exact name and its own labelled Verify button, then its courses as a numbered track. Certificates from the same issuer that are not part of the set sit apart under "Also from [issuer]". One Verify never sits below a mixed list. |
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
| S8 | Before publishing run `python tools/check.py` (sync + lint + 9-size audit + contrast in 6 accents + focus reachability + alignment report). GitHub runs the same check on every push; a red ✗ on the commit means a rule is broken. |
| S9 | Safe clean-up is part of every patch: change code where it lives (never a new layer at the end), remove what the patch makes dead, keep the S1 counts equal or lower, and prove zero unintended visual change with the before/after snapshot check before publishing. |

## 11. Focus system

One way of saying "this is in focus", everywhere. `tools/lint.py` blocks any other highlight style.

| # | Rule |
|---|---|
| F1 | Every item has exactly one dot: its action dot, or an 8px marker dot left of its title. In accordion panels a whole problem or role (title, text and its button) is one item; in the laptop list + detail layout the list row is the item and the selected row's button is its action. |
| F2 | Phone: the item nearest the middle line of the visible scroll area is in focus (page or open panel). Focus is never empty: the item stays lit until another is clearly nearer. Near the top and bottom the line slides smoothly to the first / last item, so every item can reach focus. If an area doesn't scroll, the current (else first) item stays lit until you touch another. Laptop: the item under the pointer, otherwise the line. Touch and pointer always win. |
| F3 | In focus a marker dot fills at once. An action pill opens only for the one focused item, and only once scrolling pauses (~0.15s): the pill is revealed from the dot outward (clip reveal to its pre-reserved width), the icon glides with it and the label fades in last; the reverse on close. Grid-row neighbours only fill their dots. A dot never changes size. |
| F4 | Collapsed items never open on scroll, only on tap or click. Once open, the pill stays filled and reads Hide (×); the content inside follows these same rules. |
| F5 | Items in one grid row share focus: the whole row lights together, never one item of it. Tool logos light with their row but never take focus from their skill group. |
| F6 | Logos are their own marker (K3): grey at rest, brand colour in focus. |
| F7 | Heading accent words (including the hero line) are grey until the heading reaches the middle line, stay lit while the reader is in that section, and return to readable grey when they leave it. |
| F8 | Exceptions, so nothing falls outside the rule: timeline nodes are their items' dots; the hero tiles keep their travelling dot; bars, navigation, headings, hero stats, panel controls (incl. the pinned bar), the WhatsApp button, the colour panel and the loader never take focus; form fields use the text cursor; tags are not items; contact icons stay neutral. Standalone controls (Expand / Collapse all, Full experience, Show more / Show all, View full experience, View on LinkedIn…), the main buttons and Book a time are always labelled and fill in focus. Accordion panels (Problems, Experience) have a pinned bar: what you are reading on the left (one line), the expand control on the right; Experience's expand control is Full experience, which shows every role, the turnaround case and the origin story with key skills and numbers highlighted. Motion off: same states, instantly. |

## How to add content or a feature

1. Text only: edit `content.json` → `python tools/sync_content.py` → `python tools/check.py`.
2. New styles: add them inside the one `<style>` block, next to the related component, using tokens. Never add a second block or an override layer at the end.
3. New behaviour: add it next to the related code in the main script, not in a new "layer" at the end.
4. CV PDF: edit `tools/build_cv.py` → `python tools/build_cv.py` → it must stay 2 pages and the QR must scan.
5. Preview, approve, then push. If the GitHub check turns red, fix before sharing the link.

## How to undo a release

Every release is tagged (`v9`, `v10`, `v11`, …). To roll the live site back: `git checkout main && git reset --hard v10 && git push --force` (replace `v10` with the version to return to). GitHub Pages updates within a few minutes.

## 12. Interaction contract (I1–I4)

Every item that can take focus is one of three kinds, declared once in code (`kindOf` in index.html, written to `data-kind`). Styles are written per kind, never per item, so a new item cannot miss a behaviour. `tools/hovercheck.py` enforces this on the page and inside every panel.

| # | Rule |
|---|---|
| I1 | **Kinds.** *Card*: a box of its own (tiles, skills, certificates on laptop, testimonials, contact cards, education, the form, panel cards). *Row*: a line inside a card or list (course rows, experience and problem rows, story chapters, article rows, certificates on phone). *Mark*: a brand or tool logo. |
| I2 | **Cursor response by kind, identical everywhere.** Card: lifts 2px with a soft shadow (.4s). Row: a tint appears behind it, reaching 6px past its text, nothing moves (.2s). Mark: grey to brand colour (K3). Touch screens show none of these (no hover). |
| I3 | **Focus is the same for all kinds.** Scroll, tap or hover puts one item in focus: its dot fills and its own button opens (F-rules). Hovering anywhere on an item counts, not only its button. |
| I4 | **Checked before every release.** `hovercheck.py` hovers up to 3 items of every kind and class, on the page and in each panel, and fails if any item misses its response; it also fails if fewer than 30 items carry a kind. Run with `--sabotage` to prove the check still catches a broken style. |

