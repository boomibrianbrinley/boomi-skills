# Boomi Reporting — PDF Scorecard Reference

A working Python script lives at `scripts/generate_scorecard.py`. Read this guide
first to understand the design decisions, then adapt the script for the data at hand.

---

## Key Rules (Learned the Hard Way)

### 1. Never use Paragraph `backColor` for badges
ReportLab's `backColor` on a `ParagraphStyle` does not clip to the cell boundary —
it bleeds into surrounding cells. Always use `TableStyle BACKGROUND` on the cell itself.

```python
# WRONG — bleeds outside the cell
badge_style = ParagraphStyle('badge', backColor=colors.HexColor("#D1FAE5"), ...)

# RIGHT — clips cleanly
table.setStyle(TableStyle([
    ('BACKGROUND', (0, row_index), (0, row_index), colors.HexColor("#D1FAE5")),
]))
```

### 2. Never nest Tables for colored badges
Nested Tables (a Table inside a Table cell) cause unpredictable background rendering.
Use a single flat Table where each row's badge color is applied directly via TableStyle
at the row-specific cell coordinate.

### 3. Section headers — use a two-column Table, not LINEBEFORE
`LINEBEFORE` in TableStyle drifts vertically and doesn't align with text.
Use a narrow col 0 (4–8pt wide) with a solid `BACKGROUND` coral fill instead.

```python
def section_header(text):
    t = Table([[Paragraph('', plain), Paragraph(text, sec_head)]], colWidths=[8, content_width])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), CORAL),   # solid coral left accent
        ('LINEBELOW',  (0,0), (-1,-1), 0.5, GRAY_200),
    ]))
    return t
```

---

## Layout Structure

```
┌─────────────────────────────────────────────────────────┐
│  NAVY HEADER BANNER                    DATA CLASSIFICATION│
│  Title (Poppins Bold 22, white)        CONFIDENTIAL badge │
│  Account ID (Poppins 10, light)        (amber bg, flat)  │
│  Reporting period (Poppins 9, muted)                     │
│  ─────────────────── coral underline ─────────────────── │
├──────────┬──────────┬──────────┬────────────────────────┤
│ METRIC   │ METRIC   │ METRIC   │ METRIC                 │
│ CARD     │ CARD     │ CARD     │ CARD                   │
│ (coral   │ (green   │ (purple  │ (blue accent)          │
│  accent) │  accent) │  accent) │                        │
├──────────┴──────────┴──────────┴────────────────────────┤
│ ▌ EXECUTIVE SUMMARY                                      │
│   Narrative prose...                                     │
│                                                          │
│ ▌ EXECUTION SUMMARY                                      │
│   Navy header table with coral underline                 │
│   Alternating white/gray rows                            │
│                                                          │
│ ▌ ACTIVITY HIGHLIGHTS                                    │
│   Flat table: [badge col] [gap col] [content col]        │
│   Per-row cell BACKGROUND for badge colors               │
│                                                          │
│ ▌ COMPONENTS TRANSFERRED (if applicable)                 │
│   Navy header table, alternating rows                    │
├─────────────────────────────────────────────────────────┤
│ Footer: date · source · account ID                       │
└─────────────────────────────────────────────────────────┘
```

---

## Boomi Colors

```python
CORAL      = colors.HexColor("#FF7C69")   # primary accent, metric cards, section headers
PURPLE     = colors.HexColor("#A93FA5")   # secondary accent
NAVY       = colors.HexColor("#273E59")   # header banner, table headers, body text
WHITE      = colors.white
GRAY_50    = colors.HexColor("#F9FAFB")   # alternating table rows
GRAY_200   = colors.HexColor("#E5E7EB")   # borders, dividers
GRAY_600   = colors.HexColor("#4B5563")   # muted text, labels
GREEN      = colors.HexColor("#04C788")   # success metric accent
BLUE       = colors.HexColor("#009EE2")   # info metric accent
WARN_BG    = colors.HexColor("#FEF3C7")   # confidential badge bg
WARN_FG    = colors.HexColor("#92400E")   # confidential badge text
```

---

## Typography

Fonts: Poppins Regular, SemiBold, Bold (downloaded from Google Fonts TTF)

```python
# Download once, cache locally
urls = {
    "Poppins":          "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Regular.ttf",
    "Poppins-SemiBold": "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-SemiBold.ttf",
    "Poppins-Bold":     "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Bold.ttf",
}
```

| Style | Font | Size | Color | Use |
|---|---|---|---|---|
| Doc title | Poppins-Bold | 22 | White | Header banner |
| Account sub | Poppins | 10 | #CBD5E1 | Header banner |
| Metric value | Poppins-Bold | 28 | Navy | KPI cards |
| Metric label | Poppins | 8 | Gray-600 | KPI cards |
| Section head | Poppins-SemiBold | 8 | Gray-600 | Section dividers |
| Body | Poppins | 9 | Navy | Narrative text |
| Body bold | Poppins-SemiBold | 9 | Navy | Sub-headings |
| Table header | Poppins-SemiBold | 8 | White | Navy table headers |
| Badge | Poppins-SemiBold | 8 | (varies) | Activity highlights |
| Footer | Poppins | 8 | Gray-600 | Page footer |

---

## Activity Highlights — Flat Table Pattern

This is the correct pattern. Do not deviate from it.

```python
BADGE_W = 1.0 * inch
GAP_W   = 0.15 * inch
CONT_W  = page_width - BADGE_W - GAP_W

rows = []
styles = [
    ('TOPPADDING',    (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('LEFTPADDING',   (0,0), (-1,-1), 6),
    ('RIGHTPADDING',  (0,0), (-1,-1), 6),
    ('LEFTPADDING',   (1,0), (1,-1),  0),  # gap col has no padding
    ('RIGHTPADDING',  (1,0), (1,-1),  0),
    ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ('VALIGN',        (2,0), (2,-1),  'TOP'),
]

for i, (label, bg, fg, title, desc) in enumerate(highlights):
    lbl_style = ParagraphStyle(f'lbl_{i}', fontName='Poppins-SemiBold',
                                fontSize=8, textColor=fg, alignment=1)
    rows.append([Paragraph(label, lbl_style), '', [Paragraph(title, ...), Paragraph(desc, ...)]])
    styles.append(('BACKGROUND', (0,i), (0,i), bg))      # ← color per row
    styles.append(('LINEBELOW',  (0,i), (-1,i), 0.5, GRAY_200))

table = Table(rows, colWidths=[BADGE_W, GAP_W, CONT_W])
table.setStyle(TableStyle(styles))
```

---

## Classification Badge — Flat Table Pattern

```python
# In header: single Table, 2 columns [left content | right classification]
# Apply yellow background DIRECTLY to the cell — no nested Table

header = Table([
    [Paragraph(title, title_style),    Paragraph("DATA CLASSIFICATION", label_style)],
    [Paragraph(account, sub_style),    Paragraph("CONFIDENTIAL", conf_style)],
    [Paragraph(period, date_style),    Paragraph("")],
], colWidths=[left_width, right_width])

header.setStyle(TableStyle([
    ('BACKGROUND',  (0,0), (-1,-1), NAVY),              # whole banner = navy
    ('BACKGROUND',  (1,1), (1,1),   WARN_BG),           # just the CONFIDENTIAL cell = amber
    ('ALIGN',       (1,0), (1,-1),  'RIGHT'),
    ('LINEBELOW',   (0,2), (-1,2),  3, CORAL),
    ...
]))
```

---

## File Naming Convention

```
boomi_[report-type]_YYYYMMDD.pdf
```

Examples:
- `boomi_weekly_scorecard_20260329.pdf`
- `boomi_execution_report_20260329.pdf`
- `boomi_executive_summary_20260329.pdf`
