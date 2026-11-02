import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
import pypdf

PDF_PATH = r"e:\Dev Stuff\RoundTable\SYSTEM_OVERVIEW_AND_COVERAGE.pdf"

doc = SimpleDocTemplate(
    PDF_PATH,
    pagesize=letter,
    leftMargin=36,
    rightMargin=36,
    topMargin=32,
    bottomMargin=32
)

styles = getSampleStyleSheet()

# Custom styles
style_title = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=15,
    leading=17,
    alignment=TA_CENTER,
    textColor=colors.HexColor('#0F172A')
)

style_subtitle = ParagraphStyle(
    'DocSubtitle',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=8.5,
    leading=11,
    alignment=TA_CENTER,
    textColor=colors.HexColor('#2563EB')
)

style_meta = ParagraphStyle(
    'DocMeta',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=7.5,
    leading=9.5,
    alignment=TA_CENTER,
    textColor=colors.HexColor('#64748B')
)

style_h2 = ParagraphStyle(
    'SectionHeading',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=9.5,
    leading=12,
    textColor=colors.HexColor('#1E3A8A'),
    spaceBefore=0,
    spaceAfter=0
)

style_body = ParagraphStyle(
    'BodyJustified',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=7.5,
    leading=10,
    alignment=TA_JUSTIFY,
    textColor=colors.HexColor('#1E293B')
)

style_cell = ParagraphStyle(
    'TableCell',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=7,
    leading=8.5,
    textColor=colors.HexColor('#0F172A')
)

style_cell_bold = ParagraphStyle(
    'TableCellBold',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=7,
    leading=8.5,
    textColor=colors.HexColor('#0F172A')
)

style_cell_center = ParagraphStyle(
    'TableCellCenter',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=7,
    leading=8.5,
    alignment=TA_CENTER,
    textColor=colors.HexColor('#0F172A')
)

style_cell_center_bold = ParagraphStyle(
    'TableCellCenterBold',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=7,
    leading=8.5,
    alignment=TA_CENTER,
    textColor=colors.HexColor('#0F172A')
)

story = []

# Header
story.append(Paragraph("The Round Table Exchange (RTE) — System Architecture & Test Coverage", style_title))
story.append(Spacer(1, 2))
story.append(Paragraph("A Multi-Party Skill Barter Network with Graph-Based Cycle Matching (v2.4)", style_subtitle))
story.append(Paragraph("Authors: Ahmmad Abdali Khan, Sumaia Bintey Ismail, Alin | Dept. of CSE, UITS | Date: 13 Sep 2026", style_meta))
story.append(Spacer(1, 4))
story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E1"), spaceAfter=5, spaceBefore=0))

# Section 1: Overview & Architecture (2 column table)
story.append(Paragraph("1. System Architectural Overview", style_h2))
story.append(Spacer(1, 3))

col1_text = (
    "<b>Core Algorithmic Engine:</b> RTE solves multi-lateral trade imbalances by constructing a directed multigraph "
    "where nodes represent users and directed edges indicate skill offerings and desires. A Bounded-Depth DFS engine "
    "traverses exchange loops of length <i>k</i> &isin; {2, 3, 4}, avoiding exponential branch explosion. Cycles are dynamically "
    "scored using a composite multi-signal formula: <i>S</i> = &alpha; &middot; <i>S</i><sub>geo</sub> + (1 - &alpha;) &middot; <i>S</i><sub>sched</sub>, "
    "balancing Haversine geographic proximity with weekly timetable overlap."
)
col2_text = (
    "<b>Consensus & Dual-Engine Architecture:</b> Implements an atomic 5-stage group state machine "
    "(<i>Proposed &rarr; Notified &rarr; Accepting &rarr; Locked &rarr; Executed</i>) with single-veto integrity. "
    "The system operates on a dual execution model: a high-performance <b>FastAPI</b> Python REST backend for enterprise servers, "
    "and a zero-dependency <b>In-Browser Client Engine</b> for serverless static hosting (GitHub Pages) with full algorithmic parity."
)

t_overview = Table(
    [[Paragraph(col1_text, style_body), Paragraph(col2_text, style_body)]],
    colWidths=[265, 265]
)
t_overview.setStyle(TableStyle([
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('LEFTPADDING', (0,0), (-1,-1), 0),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 0),
    ('BOTTOMPADDING', (0,0), (-1,-1), 0),
]))
story.append(t_overview)
story.append(Spacer(1, 6))

# Section 2: Specifications & Technology Stack
story.append(Paragraph("2. System Specifications & Technology Stack", style_h2))
story.append(Spacer(1, 3))

specs_data = [
    [
        Paragraph("<b>Component</b>", style_cell_bold),
        Paragraph("<b>Primary Technologies</b>", style_cell_bold),
        Paragraph("<b>Architectural Responsibility</b>", style_cell_bold)
    ],
    [
        Paragraph("Frontend UI/UX", style_cell),
        Paragraph("HTML5, CSS3 (Dark Cyber), Vanilla JS, Vis.js", style_cell),
        Paragraph("Single-page dashboard, ForceAtlas2 physics canvas, real-time loop inspector, consensus UI", style_cell)
    ],
    [
        Paragraph("Backend Gateway", style_cell),
        Paragraph("FastAPI, Uvicorn, Pydantic v2, Python 3.14", style_cell),
        Paragraph("Asynchronous REST API, input schema validation, CORS security, in-memory state store", style_cell)
    ],
    [
        Paragraph("Graph & Matching", style_cell),
        Paragraph("NetworkX, Bounded DFS, Haversine geodesics", style_cell),
        Paragraph("Multigraph construction, cyclic path discovery, multi-signal candidate ranking", style_cell)
    ],
    [
        Paragraph("State Machine", style_cell),
        Paragraph("Python Workflow Engine (in-memory & client)", style_cell),
        Paragraph("Atomic multi-user proposal tracking, timeout expiration, group voting orchestration", style_cell)
    ],
    [
        Paragraph("Benchmarking Suite", style_cell),
        Paragraph("Synthetic Dhaka Generator (20–500 nodes)", style_cell),
        Paragraph("Empirical complexity verification: <i>O</i>(<i>n</i> &middot; <i>m</i><sup><i>k</i>-1</sup>) latency & cycle count profiling", style_cell)
    ]
]
t_specs = Table(specs_data, colWidths=[90, 165, 285])
t_specs.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ('TOPPADDING', (0,0), (-1,-1), 2),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
]))
story.append(t_specs)
story.append(Spacer(1, 6))

# Section 3: Verification & Test Coverage
story.append(Paragraph("3. System Verification & Automated Test Coverage Report", style_h2))
story.append(Spacer(1, 3))

# Banner box for Test status
t_banner = Table(
    [[
        Paragraph("<b>Test Execution Status:</b> 13 / 13 Automated Tests PASSED (100% Success Rate in 0.63s)", style_cell_bold),
        Paragraph("<b>Cumulative Core Coverage:</b> 98% (523 / 536 Statements)", style_cell_center_bold)
    ]],
    colWidths=[340, 200]
)
t_banner.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#DCFCE7')),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#16A34A')),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
]))
story.append(t_banner)
story.append(Spacer(1, 4))

cov_table_data = [
    [
        Paragraph("<b>Module File</b>", style_cell_bold),
        Paragraph("<b>Stmts</b>", style_cell_center_bold),
        Paragraph("<b>Miss</b>", style_cell_center_bold),
        Paragraph("<b>Cover</b>", style_cell_center_bold),
        Paragraph("<b>Tested Scope & Functional Verification</b>", style_cell_bold)
    ],
    [
        Paragraph("<code>backend/app.py</code>", style_cell),
        Paragraph("140", style_cell_center),
        Paragraph("0", style_cell_center),
        Paragraph("<b>100%</b>", style_cell_center_bold),
        Paragraph("FastAPI REST endpoints, input validation, graph payloads, proposals & static routes", style_cell)
    ],
    [
        Paragraph("<code>backend/models.py</code>", style_cell),
        Paragraph("52", style_cell_center),
        Paragraph("0", style_cell_center),
        Paragraph("<b>100%</b>", style_cell_center_bold),
        Paragraph("Pydantic domain entities (User, SkillListing, Location, ScheduleWindow, TradeCycle)", style_cell)
    ],
    [
        Paragraph("<code>backend/synthetic_data.py</code>", style_cell),
        Paragraph("54", style_cell_center),
        Paragraph("0", style_cell_center),
        Paragraph("<b>100%</b>", style_cell_center_bold),
        Paragraph("Dhaka synthetic population generator, skill taxonomy distribution, scalability benchmarks", style_cell)
    ],
    [
        Paragraph("<code>backend/test_api.py</code>", style_cell),
        Paragraph("74", style_cell_center),
        Paragraph("0", style_cell_center),
        Paragraph("<b>100%</b>", style_cell_center_bold),
        Paragraph("Full integration suite verifying HTTP GET/POST/DELETE contracts & error paths", style_cell)
    ],
    [
        Paragraph("<code>backend/test_engine.py</code>", style_cell),
        Paragraph("70", style_cell_center),
        Paragraph("0", style_cell_center),
        Paragraph("<b>100%</b>", style_cell_center_bold),
        Paragraph("Unit test harness for cycle bounds, Haversine ranking, DAG non-cycles & consensus states", style_cell)
    ],
    [
        Paragraph("<code>backend/graph_engine.py</code>", style_cell),
        Paragraph("109", style_cell_center),
        Paragraph("7", style_cell_center),
        Paragraph("<b>94%</b>", style_cell_center_bold),
        Paragraph("Multigraph construction, bounded DFS cycle detection (k=3,4), composite scoring math", style_cell)
    ],
    [
        Paragraph("<code>backend/workflow.py</code>", style_cell),
        Paragraph("37", style_cell_center),
        Paragraph("6", style_cell_center),
        Paragraph("<b>84%</b>", style_cell_center_bold),
        Paragraph("Atomic group proposal lifecycle, unanimous acceptance, single-rejection termination", style_cell)
    ],
    [
        Paragraph("<b>TOTAL (Full Backend Core)</b>", style_cell_bold),
        Paragraph("<b>536</b>", style_cell_center_bold),
        Paragraph("<b>13</b>", style_cell_center_bold),
        Paragraph("<b>98%</b>", style_cell_center_bold),
        Paragraph("<b>Comprehensive end-to-end algorithmic and integration verification</b>", style_cell_bold)
    ]
]

t_cov = Table(cov_table_data, colWidths=[125, 35, 30, 45, 305])
t_cov.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
    ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#F8FAFC')),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ('TOPPADDING', (0,0), (-1,-1), 2),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ('LEFTPADDING', (0,0), (-1,-1), 4),
    ('RIGHTPADDING', (0,0), (-1,-1), 4),
]))
story.append(t_cov)
story.append(Spacer(1, 6))

# Footer note
story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E2E8F0"), spaceAfter=3, spaceBefore=0))
story.append(Paragraph(
    "<b>Verification Environment:</b> Python 3.14.6 | Pytest 9.1.1 | Coverage.py 7.16.0 | OS: Windows 11 AMD64 | "
    "All tests automated & reproducible via <code>pytest --cov=backend</code> | <i>RoundTable Exchange v2.4 (Single-Page Brief)</i>",
    style_meta
))

# Build Document
doc.build(story)

# Verify page count
reader = pypdf.PdfReader(PDF_PATH)
page_count = len(reader.pages)
print(f"Generated PDF: {PDF_PATH} with {page_count} page(s).")
assert page_count == 1, f"Expected 1 page, but got {page_count} pages!"
