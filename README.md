# Abdullah Sulehri · CV site

A one-page CV site. All text, numbers, links, logos and images are stored in **`content.json`**. The page reads that file every time it loads, so changing the site never means touching code.

## Put it on GitHub Pages (one time)

1. Create a public repository, for example `abdullahsulehri.github.io`.
2. Upload **everything in this folder** (keep the folder structure: `assets/`, `cv/`, `index.html`, `content.json`, `.nojekyll`).
3. Go to **Settings → Pages → Build and deployment**, choose **Deploy from a branch**, branch `main`, folder `/ (root)`, and save.
4. After a minute the site is live at `https://<username>.github.io/`. A custom domain can be added later on the same Settings page.

## Edit the site

1. Open `content.json` on GitHub and click the pencil icon.
2. Change the text between the quotes. Keep every comma, bracket and quote mark.
3. Click **Commit changes**. The live site updates in about a minute; refresh the page.

If the page stops updating after an edit, the file probably has a missing comma or quote. Open the file's **History** on GitHub and restore the previous version. (The page then falls back to the copy built into `index.html`, so it never goes blank.)

**Accent words.** Wrap a word in asterisks to colour it in the accent colour: `"From blogger to *B2B lead*."`

## Where everything lives in `content.json`

| What | Where |
|---|---|
| Email, LinkedIn, booking link, CV file, accent colour | `settings` |
| Name, photo, role line, headline, status, hero numbers | `hero` |
| The 6 tiles on the first screen | `tiles` |
| What each tile opens | `panels` (`problems`, `proof`, `ai`, `testimonials`, `writing`) |
| Career strip | `career.items` |
| Certificates and education | `certificates` |
| Testimonials | `testimonials.items` |
| Brand logos | `brands.items` |
| "Why I built this" | `why` |
| Contact section | `contact` |
| Top menu | `nav` |

## How to add things

**A new job.**
1. Add an entry at the **end** of `career.items`. Items run oldest to newest.
2. Move `"now": true` to the new entry and set the old one to `false`.
3. Add the role to `panels.proof.roles` as well, at the **top** (newest first).

```json
{"years":"2027 – Now","title":"Head of Marketing","company":"Company name","headline":"One-line story","story":"Two or three sentences.","highlights":["Result one","Result two"],"now":true}
```

**A certificate from a new issuer.** Add an entry to `certificates.issuers`. If there's no logo file yet, leave `"logo":""` and the card shows the issuer's initials, or the text in `"short"`.

```json
{"issuer":"Harvard Business School Online","logo":"assets/logos/hbs.webp","short":"HBS","items":[{"title":"Course name","date":"Mar 2027","url":"https://verification-link"}]}
```

**More certificates from an existing issuer.** Add to that issuer's `items`.

**A big certificate programme.** Add an entry to `certificates.featured`. Each one is a large card with a course list.

**The certificate count updates itself.** The hero number for certificates uses `"auto":"certificates"`, so it counts everything in `certificates`. To fix the number by hand instead, replace `"auto"` with `"value": 30`.

**A brand logo.**
1. Upload the image to `assets/logos/`.
2. Add `{"name":"Brand","logo":"assets/logos/brand.webp"}` to `brands.items`.
3. If you leave `"logo":""`, the brand's name is shown instead.

**A testimonial.** Add `{"name":"","title":"","company":"","year":"","text":""}` to `testimonials.items`. All testimonials are shown.

**An article.** Add to `panels.writing.articles`.
- With `"blocks"`, the article can be read on the site.
- Without `"blocks"`, its row opens the LinkedIn link instead.

**A hero number.** Edit `hero.stats`. Four numbers fit best.

**A new photo.**
1. Upload it to `assets/`. Use a cut-out with a transparent background, full body, in portrait format.
2. Set `hero.portrait` to the new file path.

**A new CV.** Upload the PDF to `cv/` with the same file name (`Abdullah-Sulehri-CV.pdf`), or change `settings.cv_url`.

**Accent colour.** Set `settings.accent`. Visitors can also pick from `settings.accent_presets` with the Colours button.

## Layout rules (how the design absorbs new data)

- **Tiles:** 2 columns. 6 is ideal; 4 or 8 also fill evenly. A tile with `"scrolls_to"` jumps to a section instead of opening a panel.
- **Panels:** the pager, its counter and the Previous/Next buttons count the panels automatically. Each panel's headline is its tile's headline.
- **Career strip:**
  - Oldest on the left, **Now** on the right.
  - More than 6 items scroll sideways.
  - The current role opens by default.
- **Certificate and education grids:** 3 columns. If the last row is short, its last card stretches, so no card is left alone.
- **Brand logos:** the column count adjusts so the last row is never a lone logo.
- **Logos display style:** all logos are shown in one ink colour, so logos of different colours still match.
- **Empty sections:** a section with no items is hidden automatically.
- **Phone:**
  - The name stacks onto two lines.
  - Panels open full screen.
  - The phone's Back button closes the panel instead of leaving the site.

## Logo files

Logos are best as transparent PNG or WebP files, about 72 px tall. The site turns every logo into one ink colour, so the logo's own colours don't matter. Avoid logos on a solid coloured background: the whole block turns into one dark shape.
