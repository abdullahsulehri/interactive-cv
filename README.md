# Abdullah Sulehri: interactive CV

Live site: https://abdullahsulehri.github.io/interactive-cv/

| File | What it is |
|---|---|
| `index.html` | The whole site (layout, styles, scripts) |
| `content.json` | All text and data: roles, AI projects, certificates, testimonials, links |
| `assets/` | Portrait, paper textures, brand/tool/institution logos |
| `cv/Abdullah-Sulehri-CV.pdf` | Downloadable CV |
| `DESIGN-RULES.md` | **Read before any change.** 41 design rules every edit must follow |
| `tools/` | Audit scripts that check the rules at 9 screen sizes |

**Before publishing any change:** run `python tools/audit.py` and `python tools/align.py` against the changed page and fix everything they report (rule Q1).

The contact form sends through Web3Forms; the access key in `content.json` (`settings.web3forms_key`) is public by design.
