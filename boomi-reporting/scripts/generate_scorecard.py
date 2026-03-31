from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import urllib.request, os, math

OUTPUT = "/mnt/user-data/outputs/boomi_weekly_scorecard_20260329.pdf"

# ── Download Poppins fonts ────────────────────────────────────────────────────
FONT_DIR = "/home/claude/fonts"
os.makedirs(FONT_DIR, exist_ok=True)

fonts = {
    "Poppins":       "https://fonts.gstatic.com/s/poppins/v21/pxiEyp8kv8JHgFVrJJfecg.woff2",
    "Poppins-Bold":  "https://fonts.gstatic.com/s/poppins/v21/pxiByp8kv8JHgFVrLCz7Z1xlFQ.woff2",
    "Poppins-SemiBold": "https://fonts.gstatic.com/s/poppins/v21/pxiByp8kv8JHgFVrLEj6Z1xlFQ.woff2",
}

# Use ttf versions instead (woff2 not supported by reportlab)
ttf_fonts = {
    "Poppins":          ("https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Regular.ttf",    f"{FONT_DIR}/Poppins-Regular.ttf"),
    "Poppins-SemiBold": ("https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-SemiBold.ttf",  f"{FONT_DIR}/Poppins-SemiBold.ttf"),
    "Poppins-Bold":     ("https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Bold.ttf",      f"{FONT_DIR}/Poppins-Bold.ttf"),
}

for name, (url, path) in ttf_fonts.items():
    if not os.path.exists(path):
        print(f"Downloading {name}...")
        urllib.request.urlretrieve(url, path)
    pdfmetrics.registerFont(TTFont(name, path))

# ── Boomi Colors ──────────────────────────────────────────────────────────────
CORAL       = colors.HexColor("#FF7C69")
PURPLE      = colors.HexColor("#A93FA5")
NAVY        = colors.HexColor("#273E59")
WHITE       = colors.white
GRAY_50     = colors.HexColor("#F9FAFB")
GRAY_100    = colors.HexColor("#F3F4F6")
GRAY_200    = colors.HexColor("#E5E7EB")
GRAY_300    = colors.HexColor("#D1D5DB")
GRAY_600    = colors.HexColor("#4B5563")
GREEN       = colors.HexColor("#04C788")
BLUE        = colors.HexColor("#009EE2")
GREEN_DARK  = colors.HexColor("#027A52")
BLUE_DARK   = colors.HexColor("#006FA0")
WARN_BG     = colors.HexColor("#FEF3C7")
WARN_FG     = colors.HexColor("#92400E")

# ── Styles ────────────────────────────────────────────────────────────────────
def PS(name, **kw):
    return ParagraphStyle(name, **kw)

# Header
hdr_title    = PS('hdr_title',    fontName='Poppins-Bold',     fontSize=22, textColor=WHITE,    leading=28, spaceAfter=2)
hdr_sub      = PS('hdr_sub',      fontName='Poppins',          fontSize=10, textColor=colors.HexColor("#CBD5E1"), leading=16)
hdr_date     = PS('hdr_date',     fontName='Poppins',          fontSize=9,  textColor=colors.HexColor("#94A3B8"))
hdr_class    = PS('hdr_class',    fontName='Poppins-SemiBold', fontSize=8,  textColor=colors.HexColor("#92400E"), backColor=colors.HexColor("#FEF3C7"), borderPadding=(3,8,3,8))

# Metric cards
m_label      = PS('m_label',      fontName='Poppins',          fontSize=8,  textColor=GRAY_600, spaceAfter=2)
m_value      = PS('m_value',      fontName='Poppins-Bold',     fontSize=28, textColor=NAVY,     leading=32, spaceAfter=1)
m_sub        = PS('m_sub',        fontName='Poppins',          fontSize=8,  textColor=GRAY_600)

# Section
sec_head     = PS('sec_head',     fontName='Poppins-SemiBold', fontSize=8,  textColor=GRAY_600, spaceBefore=18, spaceAfter=6)
body_text    = PS('body_text',    fontName='Poppins',          fontSize=9,  textColor=NAVY,     leading=14, spaceAfter=6)
body_bold    = PS('body_bold',    fontName='Poppins-SemiBold', fontSize=9,  textColor=NAVY,     leading=14, spaceAfter=3, spaceBefore=8)
body_muted   = PS('body_muted',   fontName='Poppins',          fontSize=8,  textColor=GRAY_600, leading=13, spaceAfter=4)

# Highlights
row_title_s  = PS('row_title_s',  fontName='Poppins-SemiBold', fontSize=10, textColor=NAVY,     spaceAfter=2)
row_desc_s   = PS('row_desc_s',   fontName='Poppins',          fontSize=8,  textColor=GRAY_600, leading=13)

# Table
tbl_hdr_s    = PS('tbl_hdr_s',    fontName='Poppins-SemiBold', fontSize=8,  textColor=WHITE)
tbl_cell_s   = PS('tbl_cell_s',   fontName='Poppins',          fontSize=8,  textColor=NAVY,     leading=12)
tbl_cell_m_s = PS('tbl_cell_m_s', fontName='Poppins',          fontSize=8,  textColor=GRAY_600, leading=12)
tbl_ok       = PS('tbl_ok',       fontName='Poppins-SemiBold', fontSize=8,  textColor=GREEN_DARK)

# Footer
footer_s     = PS('footer_s',     fontName='Poppins',          fontSize=8,  textColor=GRAY_600)

# ── Document ──────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(OUTPUT, pagesize=letter,
    leftMargin=0.6*inch, rightMargin=0.6*inch,
    topMargin=0.5*inch, bottomMargin=0.6*inch)

story = []
PW = 7.3 * inch  # usable width

# ── HEADER BANNER ─────────────────────────────────────────────────────────────
# Single flat 2-col table. Col 0 = titles. Col 1 = classification label + value.
# NO nested tables — background colors applied directly to cells via TableStyle.

conf_label_s = PS('dc_lbl', fontName='Poppins',         fontSize=7,  textColor=colors.HexColor("#94A3B8"))
conf_text_s  = PS('dc_val', fontName='Poppins-SemiBold', fontSize=9,  textColor=colors.HexColor("#92400E"))

LW = PW - 1.5*inch  # left col width
RW = 1.5*inch        # right col width

header_table = Table([
    [
        Paragraph("Weekly Account Scorecard", hdr_title),
        Paragraph("DATA CLASSIFICATION", conf_label_s),
    ],
    [
        Paragraph("boomi_adambedenbaugh-WI542T", hdr_sub),
        Paragraph("CONFIDENTIAL", conf_text_s),
    ],
    [
        Paragraph("Reporting period: Mar 22 – Mar 29, 2026",
                  PS('hdr_date2', fontName='Poppins', fontSize=9, textColor=colors.HexColor("#94A3B8"))),
        Paragraph(""),
    ],
], colWidths=[LW, RW])

header_table.setStyle(TableStyle([
    # Whole banner = navy
    ('BACKGROUND',    (0,0), (-1,-1), NAVY),
    # Right col classification cell background = amber/yellow
    ('BACKGROUND',    (1,1), (1,1),   colors.HexColor("#FEF3C7")),
    # Padding
    ('TOPPADDING',    (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING',   (0,0), (-1,-1), 20),
    ('RIGHTPADDING',  (0,0), (-1,-1), 20),
    ('TOPPADDING',    (0,0), (-1,0),  16),
    ('BOTTOMPADDING', (0,2), (-1,2),  16),
    # Alignment
    ('ALIGN',         (1,0), (1,-1),  'RIGHT'),
    ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    # Coral underline
    ('LINEBELOW',     (0,2), (-1,2),  3, CORAL),
]))
story.append(header_table)
story.append(Spacer(1, 14))

# ── METRIC CARDS ──────────────────────────────────────────────────────────────
CW = (PW - 3*0.12*inch) / 4

def metric_card(label, value, sub, accent=CORAL):
    inner = Table([
        [Paragraph(label.upper(), m_label)],
        [Paragraph(value, m_value)],
        [Paragraph(sub, m_sub)],
    ], colWidths=[CW - 0.24*inch])
    inner.setStyle(TableStyle([
        ('TOPPADDING',    (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING',   (0,0), (-1,-1), 0),
        ('RIGHTPADDING',  (0,0), (-1,-1), 0),
    ]))
    outer = Table([[inner]], colWidths=[CW])
    outer.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), WHITE),
        ('BOX',           (0,0), (-1,-1), 0.5, GRAY_200),
        ('LINEABOVE',     (0,0), (-1,0),  3, accent),
        ('TOPPADDING',    (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('LEFTPADDING',   (0,0), (-1,-1), 14),
        ('RIGHTPADDING',  (0,0), (-1,-1), 14),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
    ]))
    return outer

metrics_row = [[
    metric_card("Production Executions", "1",  "100% success rate", CORAL),
    Spacer(0.12*inch, 1),
    metric_card("Errors / Warnings",     "0",  "Clean audit log",   GREEN),
    Spacer(0.12*inch, 1),
    metric_card("Active Users",          "3",  "2 Boomi · 1 DXC",  PURPLE),
    Spacer(0.12*inch, 1),
    metric_card("Components Transferred","14", "To wwt-I7UFBZ",    BLUE),
]]
mt = Table(metrics_row, colWidths=[CW, 0.12*inch, CW, 0.12*inch, CW, 0.12*inch, CW])
mt.setStyle(TableStyle([
    ('TOPPADDING',    (0,0), (-1,-1), 0),
    ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ('LEFTPADDING',   (0,0), (-1,-1), 0),
    ('RIGHTPADDING',  (0,0), (-1,-1), 0),
    ('VALIGN',        (0,0), (-1,-1), 'TOP'),
]))
story.append(mt)
story.append(Spacer(1, 16))

def section_header(text):
    accent_col = Table([['']], colWidths=[4])
    accent_col.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), CORAL),
        ('TOPPADDING',    (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING',   (0,0), (-1,-1), 0),
        ('RIGHTPADDING',  (0,0), (-1,-1), 0),
    ]))
    t = Table([[accent_col, Paragraph(text, sec_head)]], colWidths=[8, PW - 8])
    t.setStyle(TableStyle([
        ('TOPPADDING',    (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING',   (0,0), (-1,-1), 0),
        ('RIGHTPADDING',  (0,0), (-1,-1), 0),
        ('LEFTPADDING',   (0,1), (0,1),   8),
        ('LINEBELOW',     (0,0), (-1,-1), 0.5, GRAY_200),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t

# ── EXECUTIVE SUMMARY ─────────────────────────────────────────────────────────
story.append(section_header("EXECUTIVE SUMMARY"))
story.append(Spacer(1, 8))

story.append(Paragraph(
    "This account saw moderate but meaningful activity over the past 7 days, primarily driven by "
    "adam.bedenbaugh@boomi.com across several sessions. The week was characterized by active "
    "development and testing rather than production workloads — no errors, no warnings, and no "
    "anomalies were detected. Overall account health is clean.", body_text))

story.append(Paragraph("User Activity", body_bold))
story.append(Paragraph(
    "Three distinct users accessed the account: adam.bedenbaugh@boomi.com (primary, active across "
    "multiple days), brian.brinley@boomi.com (Mar 27), and fathi.sharif@dxc.com (Mar 23). "
    "A new user — adam.bedenbaugh@gmail.com — was added on Mar 24 and assigned the "
    "Developer - Environment Demo role.", body_text))

story.append(Paragraph("Configuration Changes", body_bold))
story.append(Paragraph(
    "On Mar 24, environment extensions were edited in the demo environment. On Mar 27, "
    "brian.brinley@boomi.com updated account CORS settings to allow http://localhost:3000 "
    "(GET, POST) — consistent with active local development. A Platform API token named "
    "\"Platform API Explorer\" was also created the same day.", body_text))

story.append(Paragraph("Component Transfer to WWT", body_bold))
story.append(Paragraph(
    "On Mar 27, adam.bedenbaugh@boomi.com performed a batch copy of 14 components to external "
    "account wwt-I7UFBZ. All were Platform API components centered around folder management and "
    "permissions. Connector credentials were not included (COPY_PASSWORDS: false). "
    "Role-based folder permissions are account-scoped and must be configured independently "
    "in the target account.", body_text))

story.append(Paragraph("Development Activity", body_bold))
story.append(Paragraph(
    "Heavy manual test execution activity was observed across Mar 23, 24, 26, and 28 — all "
    "triggered by adam.bedenbaugh@boomi.com. 20+ test-mode executions were recorded across "
    "multiple process IDs, consistent with active iterative process development. None represent "
    "scheduled or production workloads.", body_text))

story.append(Spacer(1, 6))

# ── EXECUTION SUMMARY ─────────────────────────────────────────────────────────
story.append(section_header("EXECUTION SUMMARY"))
story.append(Spacer(1, 8))

exec_data = [
    [Paragraph("Process", tbl_hdr_s),
     Paragraph("Date", tbl_hdr_s),
     Paragraph("Status", tbl_hdr_s),
     Paragraph("Duration", tbl_hdr_s),
     Paragraph("Type", tbl_hdr_s)],
    [Paragraph("[Toggl>CSV] Assignment Report", tbl_cell_s),
     Paragraph("Mar 24, 2026  6:45 PM UTC", tbl_cell_m_s),
     Paragraph("COMPLETE", tbl_ok),
     Paragraph("~45 sec", tbl_cell_m_s),
     Paragraph("Production", tbl_cell_m_s)],
]
col_w = [2.5*inch, 1.4*inch, 0.85*inch, 0.75*inch, 0.8*inch]
et = Table(exec_data, colWidths=col_w)
et.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0),  NAVY),
    ('BACKGROUND',    (0,1), (-1,1),  WHITE),
    ('TOPPADDING',    (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING',   (0,0), (-1,-1), 8),
    ('RIGHTPADDING',  (0,0), (-1,-1), 8),
    ('BOX',           (0,0), (-1,-1), 0.5, GRAY_200),
    ('INNERGRID',     (0,0), (-1,-1), 0.5, GRAY_200),
    ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ('LINEBELOW',     (0,0), (-1,0),  2, CORAL),
]))
story.append(et)
story.append(Spacer(1, 6))
story.append(Paragraph(
    "In addition to the single production execution, 20+ manual test executions were recorded "
    "during development sessions. No errors or anomalies were detected in any execution.",
    body_muted))
story.append(Spacer(1, 6))

# ── ACTIVITY HIGHLIGHTS ───────────────────────────────────────────────────────
story.append(section_header("ACTIVITY HIGHLIGHTS"))
story.append(Spacer(1, 8))

BADGE_W = 1.0*inch
GAP_W   = 0.15*inch
CONT_W  = PW - BADGE_W - GAP_W

highlights = [
    ("Execution",     colors.HexColor("#D1FAE5"), GREEN_DARK,
     "[Toggl>CSV] Assignment Report",
     "Ran once on Mar 24 · completed in ~45 sec · no errors"),
    ("User Mgmt",     colors.HexColor("#DBEAFE"), colors.HexColor("#1E40AF"),
     "New user added",
     "adam.bedenbaugh@gmail.com · assigned Developer - Environment Demo role on Mar 24"),
    ("Config",        colors.HexColor("#EDE9FE"), colors.HexColor("#5B21B6"),
     "API token created",
     '"Platform API Explorer" token created by brian.brinley@boomi.com on Mar 27'),
    ("Config",        colors.HexColor("#EDE9FE"), colors.HexColor("#5B21B6"),
     "CORS settings updated",
     "localhost:3000 (GET, POST) added by brian.brinley@boomi.com on Mar 27"),
    ("Transfer",      colors.HexColor("#DBEAFE"), colors.HexColor("#1E40AF"),
     "14 components copied to WWT (wwt-I7UFBZ)",
     "Platform API folder management suite · credentials not included · Mar 27"),
    ("Dev Activity",  WARN_BG, WARN_FG,
     "20+ manual test executions",
     "Active process development across Mar 23, 24, 26, 28 · test-mode only · no production impact"),
]

# Build as a single multi-row table: col0=badge, col1=gap, col2=content
# Each highlight = 1 row. Background color applied per-cell via TableStyle.
hl_rows = []
hl_styles = [
    ('TOPPADDING',    (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('LEFTPADDING',   (0,0), (-1,-1), 6),
    ('RIGHTPADDING',  (0,0), (-1,-1), 6),
    ('LEFTPADDING',   (1,0), (1,-1),  0),
    ('RIGHTPADDING',  (1,0), (1,-1),  0),
    ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ('VALIGN',        (2,0), (2,-1),  'TOP'),
]

for i, (label, bg, fg, title, desc) in enumerate(highlights):
    label_style = PS(f'hl_lbl_{i}', fontName='Poppins-SemiBold', fontSize=8, textColor=fg,
                     alignment=1)  # centered
    content = [Paragraph(title, row_title_s), Paragraph(desc, row_desc_s)]
    hl_rows.append([Paragraph(label, label_style), '', content])
    # Badge background for this row
    hl_styles.append(('BACKGROUND', (0,i), (0,i), bg))
    # Divider below each row
    hl_styles.append(('LINEBELOW', (0,i), (-1,i), 0.5, GRAY_200))

hl_table = Table(hl_rows, colWidths=[BADGE_W, GAP_W, CONT_W])
hl_table.setStyle(TableStyle(hl_styles))
story.append(hl_table)

story.append(Spacer(1, 6))

# ── COMPONENTS TRANSFERRED ────────────────────────────────────────────────────
story.append(section_header("COMPONENTS TRANSFERRED TO WWT"))
story.append(Spacer(1, 8))

components = [
    "Platform API Query Folder by Name",
    "Platform API - Enrich Data with Parent Id",
    "Platform API Folder Update",
    "Single Element",
    "Parent Folder Permissions",
    "Platform Query Folder by ParentName",
    "Boomi Platform API",
    "Platform API - Add Roles",
    "Boomi AtomSphere API Folder QUERY Response 2",
    "Boomi Platform API Folder UPDATE Request",
    "Boomi Platform API Folder UPDATE Response",
    "[SUB] Child Folder Recursive Query",
    "Platform API - Set Cascading Folder Permissions",
    "Boomi Platform API Folder QUERY Response",
]

comp_rows = [[Paragraph("#", tbl_hdr_s), Paragraph("Component Name", tbl_hdr_s)]]
for i, c in enumerate(components, 1):
    row_bg = WHITE if i % 2 == 0 else GRAY_50
    comp_rows.append([
        Paragraph(str(i), tbl_cell_m_s),
        Paragraph(c, tbl_cell_s)
    ])

ct = Table(comp_rows, colWidths=[0.35*inch, PW - 0.35*inch])
ct.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),  (-1,0),  NAVY),
    ('ROWBACKGROUNDS',(0,1),  (-1,-1), [WHITE, GRAY_50]),
    ('TOPPADDING',    (0,0),  (-1,-1), 5),
    ('BOTTOMPADDING', (0,0),  (-1,-1), 5),
    ('LEFTPADDING',   (0,0),  (-1,-1), 8),
    ('RIGHTPADDING',  (0,0),  (-1,-1), 8),
    ('BOX',           (0,0),  (-1,-1), 0.5, GRAY_200),
    ('INNERGRID',     (0,0),  (-1,-1), 0.5, GRAY_200),
    ('VALIGN',        (0,0),  (-1,-1), 'MIDDLE'),
    ('LINEBELOW',     (0,0),  (-1,0),  2, CORAL),
]))
story.append(ct)
story.append(Spacer(1, 5))
story.append(Paragraph(
    "Note: Connector credentials were not transferred (COPY_PASSWORDS: false). "
    "Role-based folder permissions are account-scoped and must be configured independently "
    "in the target account.", body_muted))

# ── FOOTER ────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 16))
ft = Table([[
    Paragraph("Generated Mar 29, 2026", footer_s),
    Paragraph("Source: Boomi audit log + execution history", footer_s),
    Paragraph("boomi_adambedenbaugh-WI542T", footer_s),
]], colWidths=[PW/3]*3)
ft.setStyle(TableStyle([
    ('LINEABOVE',     (0,0), (-1,-1), 0.5, GRAY_200),
    ('TOPPADDING',    (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ('LEFTPADDING',   (0,0), (-1,-1), 0),
    ('RIGHTPADDING',  (0,0), (-1,-1), 0),
    ('ALIGN',         (1,0), (1,0),   'CENTER'),
    ('ALIGN',         (2,0), (2,0),   'RIGHT'),
]))
story.append(ft)

doc.build(story)
print("Done")
