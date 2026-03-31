---
name: boomi-branding
description: >
  Apply Boomi brand guidelines when creating HTML pages, architecture diagrams,
  technical documentation, presentations, or any visual content for Boomi projects.
  Use this skill whenever the user asks to create, style, or brand anything for Boomi —
  including web pages, dashboards, diagrams, reports, slide decks, or component libraries.
  Also trigger when the user mentions Boomi colors, Boomi fonts, Boomi logos, or wants
  output that "looks like Boomi" or follows "Boomi branding". When in doubt, use this
  skill — it ensures correct colors, typography, logos, and accessibility compliance.
---

# Boomi Branding Skill

This skill ensures all Boomi-branded output follows official brand guidelines. Before
creating any HTML, diagram, presentation, or document for Boomi, consult this skill.

## Quick Reference

| Element         | Value                                      |
|-----------------|--------------------------------------------|
| Primary font    | Poppins (Google Fonts)                     |
| Primary color   | Coral `#FF7C69`                            |
| Secondary color | Purple `#A93FA5`                           |
| Text/headers    | Navy `#273E59`                             |
| Background      | White `#FFFFFF` / Light gray `#F9FAFB`     |
| Gradient        | `#FF7C69` → `#A93FA5` (135deg)             |
| Icon library    | Phosphor Icons (CDN)                       |
| Border radius   | `9999px` for pills; `0.5rem` for cards     |
| Badge padding   | 1:3 ratio (e.g. `0.375rem 1.125rem`)       |

---

## When to Read Reference Files

- **Full color palette, gradients, contrast ratios**: → `references/colors.md`
- **Logo variants, CSS embed classes, placement rules**: → `references/logos.md`
- **Typography, spacing, shadows, component CSS**: → `references/components.md`
- **Full HTML page template (copy-paste ready)**: → `references/html-template.md`
- **Architecture diagram guidelines & Mermaid config**: → `references/diagrams.md`
- **Phosphor Icons CDN + usage patterns**: → `references/icons.md`

For a complete HTML page, read `references/html-template.md` and `references/components.md`.
For a diagram, read `references/diagrams.md` and `references/colors.md`.
For logo placement questions, read `references/logos.md`.

---

## Core Rules (Always Apply)

### Colors
- **Primary brand communications**: Use ONLY coral, purple, navy, white, black
- **Internal/technical docs**: May also use secondary palette (periwinkle, blue, green)
- **Never** use green `#04C788` or blue `#009EE2` as text color on white — insufficient contrast
- **Body text**: Always navy `#273E59` on white `#FFFFFF` (14.21:1 contrast)
- **Gradient**: Coral-to-purple (`linear-gradient(135deg, #FF7C69 0%, #A93FA5 100%)`)

### Typography
- Import Poppins from Google Fonts: `https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap`
- Headings: Bold (700) or SemiBold (600), navy
- Body: Regular (400), navy, 16px base
- Code: JetBrains Mono or Fira Code

### Badges & Pills (Critical)
- `border-radius: 9999px` — always
- Padding ratio **1:3** vertical:horizontal (e.g. `0.375rem 1.125rem`)
- `display: inline-flex; align-items: center;`
- `min-height: 2rem` to prevent collapse

### Logo Usage
- Light backgrounds → 2-color wordmark (navy + coral dot) or 1-color navy
- Dark backgrounds → reversed (white) versions
- Never rotate, recolor, stretch, or add effects
- Minimum digital width: 70px (wordmark), 35px (mark)

---

## CSS Variable Starter Block

Always include this `:root` block in every HTML output:

```css
:root {
  /* Primary */
  --boomi-coral: #FF7C69;
  --boomi-purple: #A93FA5;
  --boomi-navy: #273E59;
  --boomi-white: #FFFFFF;
  --boomi-black: #000000;

  /* Secondary (use sparingly) */
  --boomi-periwinkle: #4E47E7;
  --boomi-blue: #009EE2;
  --boomi-green: #04C788;
  --boomi-purple-alt: #A6327D;

  /* Neutrals */
  --gray-50: #F9FAFB;
  --gray-100: #F3F4F6;
  --gray-200: #E5E7EB;
  --gray-300: #D1D5DB;
  --gray-600: #4B5563;
  --gray-800: #1F2937;

  /* Typography */
  --font-sans: "Poppins", -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: "JetBrains Mono", "Fira Code", monospace;

  /* Spacing */
  --space-1: 0.25rem; --space-2: 0.5rem;
  --space-3: 0.75rem; --space-4: 1rem;
  --space-6: 1.5rem;  --space-8: 2rem;
  --space-12: 3rem;   --space-16: 4rem;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
}
```

---

## Section Header Icons

Do NOT place Phosphor Icons inline inside `<h2>` or `<h3>` tags. Icon + text
inside a heading element will misalign. Instead, use the coral left-border
accent (already defined on `h2`) as the sole visual indicator — no icons needed.

If icons are desired on headings, they must be placed in a flex wrapper OUTSIDE
the heading tag:
```html
<!-- ✅ Correct: flex wrapper outside the heading -->
<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.875rem;">
  <i class="ph ph-list-checks" style="color:var(--boomi-coral);font-size:1.1rem;flex-shrink:0;"></i>
  <h2 style="margin:0;padding:0;border:none;">Section Title</h2>
</div>

<!-- ❌ Wrong: icon inside the heading tag -->
<h2><i class="ph ph-list-checks"></i> Section Title</h2>
```

---

## Phosphor Icons (Quick Start)

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.2/src/regular/style.css" />

<!-- Usage -->
<i class="ph ph-database" style="color: var(--boomi-blue); font-size: 24px;"></i>
<i class="ph ph-check-circle" style="color: var(--boomi-green);"></i>
<i class="ph ph-warning" style="color: var(--boomi-coral);"></i>
```

For full icon patterns → `references/icons.md`

---

## Approved Color Combinations (Summary)

| Background     | Text      | Contrast | Use For             |
|----------------|-----------|----------|---------------------|
| Navy `#273E59` | White     | 14.21:1  | Body copy, headers  |
| White `#FFF`   | Navy      | 14.21:1  | Body copy, headers  |
| Navy `#273E59` | Coral     | 5.6:1    | Large text only     |
| Purple `#A93FA5`| White    | 6.25:1   | Large text, badges  |
| Periwinkle     | White     | 5.97:1   | Large text, badges  |
| Blue `#009EE2` | White     | 3.74:1   | Graphics only       |
| Green `#04C788`| White     | 2.28:1   | ✗ Never use         |
