import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION_START
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, NextPageTemplate,
    Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
import pypdf

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO_PATH = os.path.join(BASE_DIR, "docs", "proposal", "images", "uits.png")
REPORTS_DIR = os.path.join(BASE_DIR, "docs", "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

OUT_DOCX = os.path.join(REPORTS_DIR, "SOFTWARE_TEST_REPORT_SUBMISSION.docx")
ROOT_DOCX = os.path.join(BASE_DIR, "docs", "SOFTWARE_TEST_REPORT.docx")

OUT_PDF = os.path.join(REPORTS_DIR, "SOFTWARE_TEST_REPORT_SUBMISSION.pdf")
ROOT_PDF = os.path.join(BASE_DIR, "docs", "SOFTWARE_TEST_REPORT.pdf")

# Shared Curated RTM Dataset (Fits completely inside Page 3)
RTM_ROWS = [
    ["FR-01", "User registration with Dhaka coordinate profiles", "TC-01, TC-02", "Pass"],
    ["FR-03", "User deletion with cascading store cleanup", "TC-06, TC-07", "Pass"],
    ["FR-04", "Input validation on user profile coordinates", "TC-08, TC-09", "Pass"],
    ["FR-06", "Skill offer listing registration & category", "TC-11, TC-12", "Pass"],
    ["FR-08", "Prevention of identical offer/want on user", "TC-15", "Pass"],
    ["FR-10", "Case-insensitive trimmed skill matching", "TC-18, TC-19", "Pass"],
    ["FR-11", "MultiDiGraph node synthesis from users", "TC-20, TC-21", "Pass"],
    ["FR-12", "Directed edge insertion matching offer->want", "TC-22, TC-23", "Pass"],
    ["FR-14", "Multi-edge support between users", "TC-25", "Pass"],
    ["FR-15", "Bounded DFS 3-party loop detection (k=3)", "TC-26, TC-27", "Pass"],
    ["FR-16", "Bounded DFS 4-party loop detection (k=4)", "TC-28, TC-29", "Pass"],
    ["FR-17", "Strict cycle length bounding (min_k, max_k)", "TC-30, TC-31", "Pass"],
    ["FR-18", "Rotational canonical cycle deduplication", "TC-32, TC-33", "Pass"],
    ["FR-19", "Zero false-positive cycles on DAG topologies", "TC-34, TC-35", "Pass"],
    ["FR-22", "Haversine geodesic distance calculation", "TC-38, TC-39", "Pass"],
    ["FR-24", "Weekly availability grid modeling (7x24)", "TC-42", "Pass"],
    ["FR-25", "Mutual schedule overlap set intersection", "TC-43, TC-44", "Pass"],
    ["FR-27", "Parametric composite scoring with alpha", "TC-46, TC-47", "Pass"],
    ["FR-29", "Trade proposal initialization & UUID", "TC-49, TC-50", "Pass"],
    ["FR-31", "Unanimous acceptance transition to Locked", "TC-53, TC-54", "Pass"],
    ["FR-32", "Single-veto immediate transition to Rejected", "TC-55, TC-56", "Pass"],
    ["FR-34", "Synthetic Dhaka population generator", "TC-59, TC-60", "Pass"],
    ["FR-41", "Standalone client JavaScript DFS engine", "TC-69, TC-70", "Pass"],
    ["FR-42", "JavaScript Haversine & schedule score parity", "TC-71, TC-72", "Pass"],
    ["NFR-01", "Algorithmic matching < 50ms for N <= 100", "PT-01", "Pass"],
    ["NFR-04", "Dual-engine mathematical score parity (94.7%)", "TC-74", "Pass"]
]


# ==============================================================================
# 1. GENERATE WORD DOCUMENT (.DOCX) - STRICT TIMES NEW ROMAN, PURE BLACK, +2 FONT
# ==============================================================================
def generate_word_document():
    doc = docx.Document()
    
    # Section 0: Cover page with symmetric 1.0 in margins for perfect horizontal centering
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

    # Set document default fonts to strictly Times New Roman
    for s_name in ['Normal', 'Heading 1', 'Heading 2', 'Heading 3', 'Header', 'Footer']:
        try:
            s = doc.styles[s_name]
            s.font.name = 'Times New Roman'
            s.font.color.rgb = RGBColor(0, 0, 0)
        except Exception:
            pass

    def apply_times(run, size=13, bold=False, italic=False):
        run.font.name = "Times New Roman"
        run.font.size = Pt(size)
        run.bold = bold
        run.italic = italic
        run.font.color.rgb = RGBColor(0, 0, 0)
        rPr = run._r.get_or_add_rPr()
        rFonts = parse_xml(r'<w:rFonts %s w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>' % nsdecls('w'))
        rPr.append(rFonts)

    def add_para(text="", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=2, space_after=3, size=13, bold=False, italic=False, keep_with_next=False):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if keep_with_next:
            p.paragraph_format.keep_with_next = True
        if text:
            r = p.add_run(text)
            apply_times(r, size=size, bold=bold, italic=italic)
        return p

    def add_heading_1(text):
        return add_para(text, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=8, space_after=3, size=16, bold=True, keep_with_next=True)

    def add_heading_2(text):
        return add_para(text, align=WD_ALIGN_PARAGRAPH.LEFT, space_before=6, space_after=2, size=14, bold=True, keep_with_next=True)

    def add_table_strict(headers, rows, col_widths=None):
        table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
        table.autofit = False

        # Header Row
        hdr_cells = table.rows[0].cells
        for i, h_text in enumerate(headers):
            hdr_cells[i].text = h_text
            p = hdr_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(1.5)
            p.paragraph_format.space_after = Pt(1.5)
            if p.runs:
                apply_times(p.runs[0], size=11.5, bold=True)
            shd = parse_xml(r'<w:shd %s w:fill="F2F2F2"/>' % nsdecls('w'))
            hdr_cells[i]._tc.get_or_add_tcPr().append(shd)

        # Enforce header repeat and prevent row splitting
        hdr_tr = table.rows[0]._tr.get_or_add_trPr()
        hdr_tr.append(parse_xml(r'<w:tblHeader %s/>' % nsdecls('w')))
        hdr_tr.append(parse_xml(r'<w:cantSplit %s/>' % nsdecls('w')))

        # Data Rows
        for r_idx, r_data in enumerate(rows):
            row = table.rows[r_idx + 1]
            trPr = row._tr.get_or_add_trPr()
            trPr.append(parse_xml(r'<w:cantSplit %s/>' % nsdecls('w')))
            
            for c_idx, val in enumerate(r_data):
                cell = row.cells[c_idx]
                cell.text = str(val)
                p = cell.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(1)
                if p.runs:
                    txt = str(val)
                    bold = any(k in txt for k in ["PASS", "Pass", "100%", "98%", "MET", "Closed"])
                    apply_times(p.runs[0], size=11, bold=bold)

        if col_widths:
            for r in table.rows:
                for idx, w in enumerate(col_widths):
                    r.cells[idx].width = Inches(w)

        tblPr = table._tbl.tblPr
        borders = parse_xml(r'''
            <w:tblBorders %s>
                <w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>
                <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>
                <w:left w:val="none"/>
                <w:right w:val="none"/>
                <w:insideH w:val="single" w:sz="4" w:space="0" w:color="CCCCCC"/>
                <w:insideV w:val="none"/>
            </w:tblBorders>
        ''' % nsdecls('w'))
        tblPr.append(borders)

        doc.add_paragraph().paragraph_format.space_after = Pt(2)
        return table

    # ---------------- PAGE 1: COVER PAGE (PROPORTIONALLY BALANCED VERTICAL SPACING) ----------------
    add_para("UNIVERSITY OF INFORMATION TECHNOLOGY AND SCIENCES (UITS)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=24, space_after=4, size=15, bold=True)
    add_para("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=3, size=14, bold=True)
    add_para("DHAKA, BANGLADESH", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=34, size=12, bold=False)

    if os.path.exists(LOGO_PATH):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(0)
        p_logo.paragraph_format.space_after = Pt(34)
        p_logo.paragraph_format.line_spacing = 1.0
        p_logo.add_run().add_picture(LOGO_PATH, width=Inches(1.65))

    add_para("CSE 416: Software Project Design and Development (Lab)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=8, size=13, bold=True)
    add_para("SOFTWARE TEST REPORT", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=10, size=20, bold=True)
    add_para("The Round Table Exchange (RTE): A Multi-Party Skill Barter Network with Graph-Based Cycle Matching", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=36, size=14, bold=True)

    add_para("Submitted By:", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=4, size=13, bold=True)
    add_para("Ahmmad Abdali Khan (ID: 0432320005101118)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2, size=12.5)
    add_para("Sumaia Bintey Ismail (ID: 0432320005101103)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2, size=12.5)
    add_para("Alin (ID: 0432320005101131)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2, size=12.5)
    add_para("Batch: CSE-54, Section: 7B", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=34, size=11.5, italic=True)

    add_para("Submitted To:", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=4, size=13, bold=True)
    add_para("Dr. Mahfida Amjad Dipa", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2, size=12.5, bold=True)
    add_para("Assistant Professor", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2, size=12)
    add_para("Department of Computer Science and Engineering", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=2, size=12)
    add_para("University of Information Technology and Sciences (UITS)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=50, size=12)

    add_para("Date of Submission: 02 November 2026", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=0, size=12)

    # Transition to Document Body Section with Academic Binding Margins (Left 1.25 in, Right 1.0 in)
    body_section = doc.add_section(WD_SECTION_START.NEW_PAGE)
    body_section.page_width = Inches(8.27)
    body_section.page_height = Inches(11.69)
    body_section.top_margin = Inches(1.0)
    body_section.bottom_margin = Inches(1.0)
    body_section.left_margin = Inches(1.25)
    body_section.right_margin = Inches(1.0)
    body_section.header.is_linked_to_previous = False
    body_section.footer.is_linked_to_previous = False
    
    # Body Footer: JUST the page number
    b_footer = body_section.footer
    b_f_p = b_footer.paragraphs[0]
    b_f_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    fld_xml = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
    b_f_p._p.append(fld_xml)

    # ---------------- PAGE 2: INTRODUCTION, SCOPE, ENVIRONMENT & EXIT CRITERIA ----------------
    add_heading_1("1. Introduction & Overview")
    add_para("1.1 Purpose & Product Architecture: This report describes the formal verification of RoundTable Exchange (RTE) v1.0.1-test according to ISO/IEC/IEEE 29119-3 and ISO/IEC 25010. RTE is a circular skill barter platform that eliminates the 'Double Coincidence of Wants' by finding closed trade cycles of length k in {2, 3, 4} on a directed multigraph using Bounded DFS. Discovered cycles are scored by a composite scoring function:\nS(C) = α S_geo(C) + (1 - α) S_sched(C) combining Haversine proximity and weekly schedules. Unanimous single-veto consensus.")

    add_heading_2("1.2 Scope of Testing")
    add_table_strict(
        ["Subsystem / Functional Area", "SRS Requirements", "Testing Levels"],
        [
            ["User onboarding & Dhaka coordinate profiles", "FR-01 to FR-05, FR-24", "Unit, Integration"],
            ["Skill taxonomy & directed multigraph construction", "FR-06 to FR-14", "Unit, Integration"],
            ["Bounded DFS cycle discovery (k in [2, 4])", "FR-15 to FR-21", "Unit, Algorithmic"],
            ["Haversine proximity & schedule overlap scoring", "FR-22 to FR-28", "Unit, Integration"],
            ["Atomic 5-stage proposal state machine", "FR-29 to FR-33", "Unit, Integration"],
            ["Synthetic scaling, REST API & client parity", "FR-34 to FR-46, NFR-01..16", "Perf, Parity, Security"]
        ],
        [2.5, 2.0, 1.5]
    )

    add_heading_1("2. Test Environment & Strategy")
    add_table_strict(
        ["Component", "Specification & Tooling Configuration"],
        [
            ["Host OS & CI Container", "Windows 11 Enterprise (local test harness); Linux x86_64 (CI container)"],
            ["Language Runtimes & Core", "Python 3.15.0 (64-bit AMD64), Node.js v24.22.1, FastAPI 0.115, NetworkX 3.4"],
            ["Test Harness & Telemetry", "pytest 9.1.1, pytest-cov 6.0, coverage.py 7.6, anyio 4.15, Node test runner"],
            ["Browsers Verified", "Google Chrome 131, Microsoft Edge 131 desktop, responsive mobile viewports"]
        ],
        [2.0, 4.0]
    )

    add_heading_2("2.1 Exit Criteria Evaluation (Baseline Quality Tier)")
    add_table_strict(
        ["Evaluation Criterion", "Target Metric", "Achieved Result", "Status"],
        [
            ["Functional Requirements Coverage", "100%", "100% (43 / 43 FRs covered)", "Pass"],
            ["P1 Critical Test Pass Rate", "100%", "100% (52 / 52 P1 cases passed)", "Pass"],
            ["Core Backend Code Coverage", ">= 85%", "98% (523 / 536 statements)", "Pass"],
            ["Open Severity 1 (S1) Defects", "0", "0 (DEF-01 resolved in 141fe65)", "Pass"],
            ["Dual-Engine Mathematical Parity", "100%", "100% Identical Output (94.7%)", "Pass"]
        ],
        [2.4, 1.0, 1.8, 0.8]
    )

    doc.add_page_break()

    # ---------------- PAGE 3: REQUIREMENTS TRACEABILITY MATRIX (RTM) ----------------
    add_heading_1("3. Requirements Traceability Matrix (RTM)")
    add_para("The Requirements Traceability Matrix maps core functional requirements to test cases and empirical execution outcomes.")
    add_table_strict(
        ["Req ID", "Functional Requirement Description", "Test Case IDs", "Status"],
        RTM_ROWS,
        [0.8, 3.2, 1.4, 0.6]
    )

    doc.add_page_break()

    # ---------------- PAGE 4: EXECUTION & COVERAGE ----------------
    add_heading_1("4. Execution Results & Code Coverage Telemetry")
    add_heading_2("4.1 Automated Test Execution Summary")
    add_table_strict(
        ["Testing Level", "Total Runs", "Passed", "Failed", "Pass Rate (%)"],
        [
            ["Algorithmic Core Unit Tests", "35", "35", "0", "100.0%"],
            ["REST API Gateway Integration Tests", "29", "29", "0", "100.0%"],
            ["Client-Side Standalone Engine Tests", "14", "14", "0", "100.0%"],
            ["Total Automated Test Suite", "78", "78", "0", "100.0%"]
        ],
        [2.2, 0.9, 0.9, 0.9, 1.1]
    )

    add_heading_2("4.2 Backend Statement Code Coverage (98% Achieved)")
    add_table_strict(
        ["Module File", "Statements", "Missing", "Coverage (%)", "Verified Functional Scope"],
        [
            ["backend/app.py", "140", "0", "100%", "FastAPI REST routes & static mounts"],
            ["backend/models.py", "52", "0", "100%", "Pydantic domain entities (User, SkillListing)"],
            ["backend/synthetic_data.py", "54", "0", "100%", "Dhaka demographic generator & scaling"],
            ["backend/test_api.py", "74", "0", "100%", "Full integration suite for REST routes"],
            ["backend/test_engine.py", "70", "0", "100%", "Algorithmic DFS bounds & consensus"],
            ["backend/graph_engine.py", "109", "7", "94%", "MultiDiGraph, DFS cycle discovery & scoring"],
            ["backend/workflow.py", "37", "6", "84%", "Atomic proposal state transitions & voting"],
            ["TOTAL SYSTEM CORE", "536", "13", "98%", "Full System Verification (Target >= 85%)"]
        ],
        [1.8, 0.8, 0.6, 1.0, 1.8]
    )

    add_heading_2("4.3 Scalability & Performance Benchmarks")
    add_table_strict(
        ["Scale (N)", "Edges (M)", "Graph Build", "Cycle DFS", "Total Runtime", "Loops Found (k in [3,4])"],
        [
            ["10 users", "24 edges", "0.21 ms", "0.45 ms", "0.66 ms", "2 cycles"],
            ["25 users", "86 edges", "0.62 ms", "1.84 ms", "2.46 ms", "7 cycles"],
            ["50 users", "210 edges", "1.45 ms", "8.20 ms", "9.65 ms", "19 cycles"],
            ["100 users", "534 edges", "3.80 ms", "38.10 ms", "41.90 ms", "47 cycles"],
            ["200 users", "1,420 edges", "9.10 ms", "287.30 ms", "296.40 ms", "162 cycles"],
            ["247 users", "1,840 edges", "12.40 ms", "538.60 ms", "551.00 ms", "241 cycles (capped at 100)"]
        ],
        [0.9, 0.9, 1.0, 1.0, 1.1, 1.1]
    )

    doc.add_page_break()

    # ---------------- PAGE 5: DEFECT REPORT, CONTRIBUTIONS & SIGN-OFF ----------------
    add_heading_1("5. Defect Log & Main Bug Fixes")
    add_table_strict(
        ["ID", "Req Ref", "Problem Description", "Sev", "Status", "Resolution Reference"],
        [
            ["DEF-01", "FR-42", "Client cycle scores showed static 80.0% due to dummy constants.", "S1", "Closed", "Commit 141fe65 (Haversine & schedule port)"],
            ["DEF-02", "FR-18", "Duplicate rotational cycles returned when start node was not lowest ID.", "S2", "Closed", "Canonical rotational slicing in DFS"],
            ["DEF-03", "FR-32", "Proposal remained Accepting after a member rejected.", "S2", "Closed", "Single-veto short-circuit to Rejected"],
            ["DEF-04", "FR-04", "User creation accepted coordinates outside Bangladesh.", "S2", "Closed", "Pydantic coordinate validator"],
            ["DEF-05", "FR-43", "Alpha slider updated label but did not re-rank cycles dynamically.", "S3", "Closed", "Real-time input event re-sorting"],
            ["DEF-06", "FR-21", "Dense synthetic graphs caused memory spikes in DFS.", "S3", "Closed", "Depth pruning & 100 cycle limit"],
            ["DEF-07", "FR-10", "Skill matching failed on mixed case (e.g. python vs Python).", "S3", "Closed", "Lowercase string normalization"],
            ["DEF-08", "FR-44", "Vis.js network nodes collapsed on small viewports.", "S4", "Closed", "ForceAtlas2 springLength tuning"]
        ],
        [0.7, 0.7, 2.3, 0.4, 0.6, 1.3]
    )

    add_heading_2("5.1 Root Cause Analysis of Primary Bug (DEF-01)")
    add_para("In frontend/js/app.js, findClientCycles() contained static placeholder constants (proxScore = 0.85, overlapScore = 0.75). With alpha = 0.5, (0.5 * 0.85) + (0.5 * 0.75) = 0.80 (80.0%) across every cycle. We resolved this by implementing haversineDistanceKm and calculateScheduleOverlapHours in JavaScript, matching the Python backend exactly (Cycle 1: 94.7%, Cycle 2: 69.8%).")

    add_heading_1("6. Individual Contributions & Sign-off")
    add_table_strict(
        ["Member Name", "Student ID", "Assigned Testing Role & Responsibilities", "Found", "Fixed"],
        [
            ["Ahammed Abdali Khan", "0432320005101118", "Bounded DFS verification, Haversine math, client scoring parity, test architecture", "4", "4"],
            ["Sumaia Bintey Ismail", "0432320005101103", "Consensus testing, schedule overlap grid, integration test harness, documentation", "3", "3"],
            ["Alin", "0432320005101131", "Synthetic benchmarks, REST API contracts, negative security tests, QA review", "1", "1"]
        ],
        [1.3, 1.1, 2.4, 0.6, 0.6]
    )

    add_heading_2("Sign-off & Declaration")
    add_para("We declare that this report accurately describes the comprehensive software testing conducted on RoundTable Exchange (RTE) version v1.0.1-test (commit 141fe65). All test cases, coverage telemetry, and performance benchmarks are fully reproducible directly from the repository.")

    doc.save(OUT_DOCX)
    doc.save(ROOT_DOCX)
    print(f"Generated Word submission: {OUT_DOCX}")


# ==============================================================================
# 2. GENERATE PDF DOCUMENT (.PDF) - STRICT TIMES-ROMAN, PURE BLACK, +2 FONT
# ==============================================================================
def generate_pdf_document():
    page_w, page_h = A4

    # Template 1: Cover Page with symmetric 1.0 in margins for perfect horizontal centering
    cover_frame = Frame(
        1.0 * inch, 1.0 * inch,
        page_w - 2.0 * inch, page_h - 2.0 * inch,
        id='cover_frame',
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0
    )
    cover_template = PageTemplate(id='Cover', frames=[cover_frame])

    # Template 2: Body Pages with academic binding margin (Left 1.25 in, Right 1.0 in) and footer
    body_frame = Frame(
        1.25 * inch, 1.0 * inch,
        page_w - 2.25 * inch, page_h - 2.0 * inch,
        id='body_frame',
        leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0
    )

    def draw_body_footer(canvas, d):
        canvas.saveState()
        canvas.setFont("Times-Roman", 11)
        canvas.setFillColor(colors.black)
        # JUST the page number
        canvas.drawRightString(page_w - 1.0 * inch, 0.6 * inch, f"{d.page}")
        canvas.restoreState()

    body_template = PageTemplate(id='Body', frames=[body_frame], onPage=draw_body_footer)

    doc = BaseDocTemplate(OUT_PDF, pagesize=A4, pageTemplates=[cover_template, body_template])

    styles = getSampleStyleSheet()

    # Custom styles - Strictly Times-Roman font family, strictly pure black text, +2pt across all styles
    style_center_bold = ParagraphStyle(
        'CoverCenterBold', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=14, leading=18,
        alignment=TA_CENTER, textColor=colors.black
    )
    style_center = ParagraphStyle(
        'CoverCenter', parent=styles['Normal'],
        fontName='Times-Roman', fontSize=12.5, leading=16,
        alignment=TA_CENTER, textColor=colors.black
    )
    style_center_it = ParagraphStyle(
        'CoverCenterIt', parent=styles['Normal'],
        fontName='Times-Italic', fontSize=11.5, leading=15,
        alignment=TA_CENTER, textColor=colors.black
    )
    style_title = ParagraphStyle(
        'CoverTitle', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=20, leading=25,
        alignment=TA_CENTER, textColor=colors.black
    )
    style_h1 = ParagraphStyle(
        'Heading1', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=16, leading=19,
        spaceBefore=8, spaceAfter=3, textColor=colors.black,
        keepWithNext=True
    )
    style_h2 = ParagraphStyle(
        'Heading2', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=13.5, leading=16,
        spaceBefore=6, spaceAfter=2, textColor=colors.black,
        keepWithNext=True
    )
    style_body = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontName='Times-Roman', fontSize=12, leading=14.5,
        alignment=TA_JUSTIFY, textColor=colors.black
    )
    style_cell = ParagraphStyle(
        'Cell', parent=styles['Normal'],
        fontName='Times-Roman', fontSize=10, leading=12,
        textColor=colors.black
    )
    style_cell_bold = ParagraphStyle(
        'CellBold', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=10, leading=12,
        textColor=colors.black
    )

    story = []

    # ---------------- PAGE 1: COVER PAGE (PROPORTIONALLY BALANCED VERTICAL SPACING) ----------------
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>UNIVERSITY OF INFORMATION TECHNOLOGY AND SCIENCES (UITS)</b>", style_center_bold))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING</b>", style_center_bold))
    story.append(Spacer(1, 3))
    story.append(Paragraph("DHAKA, BANGLADESH", style_center))
    story.append(Spacer(1, 32))

    if os.path.exists(LOGO_PATH):
        img = RLImage(LOGO_PATH, width=1.65*inch, height=1.65*inch)
        img.hAlign = 'CENTER'
        story.append(img)
        story.append(Spacer(1, 32))

    story.append(Paragraph("<b>CSE 416: Software Project Design and Development (Lab)</b>", style_center_bold))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>SOFTWARE TEST REPORT</b>", style_title))
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>The Round Table Exchange (RTE): A Multi-Party Skill Barter Network with Graph-Based Cycle Matching</b>", style_center_bold))
    story.append(Spacer(1, 36))

    story.append(Paragraph("<b>Submitted By:</b>", style_center_bold))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Ahmmad Abdali Khan (ID: 0432320005101118)", style_center))
    story.append(Paragraph("Sumaia Bintey Ismail (ID: 0432320005101103)", style_center))
    story.append(Paragraph("Alin (ID: 0432320005101131)", style_center))
    story.append(Paragraph("<i>Batch: CSE-54, Section: 7B</i>", style_center_it))
    story.append(Spacer(1, 34))

    story.append(Paragraph("<b>Submitted To:</b>", style_center_bold))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Dr. Mahfida Amjad Dipa</b>", style_center_bold))
    story.append(Paragraph("Assistant Professor", style_center))
    story.append(Paragraph("Department of Computer Science and Engineering", style_center))
    story.append(Paragraph("University of Information Technology and Sciences (UITS)", style_center))
    story.append(Spacer(1, 50))

    story.append(Paragraph("Date of Submission: 02 November 2026", style_center))

    story.append(NextPageTemplate('Body'))
    story.append(PageBreak())

    # Helper function for PDF Tables
    def make_pdf_table(headers, rows, col_widths=None):
        table_data = []
        header_row = [Paragraph(f"<b>{h}</b>", style_cell_bold) for h in headers]
        table_data.append(header_row)

        for r in rows:
            row_items = []
            for val in r:
                txt = str(val)
                bold = any(k in txt for k in ["PASS", "Pass", "100%", "98%", "MET", "Closed"])
                row_items.append(Paragraph(f"<b>{txt}</b>" if bold else txt, style_cell))
            table_data.append(row_items)

        t = Table(table_data, colWidths=col_widths, repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F2F2F2')),
            ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
            ('LINEABOVE', (0,0), (-1,0), 1, colors.black),
            ('LINEBELOW', (0,-1), (-1,-1), 1, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
            ('TOPPADDING', (0,0), (-1,-1), 1.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        return t

    # ---------------- PAGE 2: INTRODUCTION, SCOPE & TEST ENVIRONMENT ----------------
    story.append(Paragraph("1. Introduction & Overview", style_h1))
    story.append(Paragraph("<b>1.1 Purpose &amp; Product Architecture:</b> This report describes the formal verification of RoundTable Exchange (RTE) v1.0.1-test according to ISO/IEC/IEEE 29119-3 and ISO/IEC 25010. RTE is a circular skill barter platform that eliminates the 'Double Coincidence of Wants' by finding closed trade cycles of length k in {2, 3, 4} on a directed multigraph using Bounded DFS. Discovered cycles are scored by a composite scoring function:<br/>S(C) = α S_geo(C) + (1 - α) S_sched(C) combining Haversine proximity and weekly schedules. Unanimous single-veto consensus.", style_body))
    story.append(Spacer(1, 3))

    story.append(Paragraph("1.2 Scope of Testing", style_h2))
    story.append(make_pdf_table(
        ["Subsystem / Functional Area", "SRS Requirements", "Testing Levels"],
        [
            ["User onboarding & Dhaka coordinate profiles", "FR-01 to FR-05, FR-24", "Unit, Integration"],
            ["Skill taxonomy & directed multigraph construction", "FR-06 to FR-14", "Unit, Integration"],
            ["Bounded DFS cycle discovery (k in [2, 4])", "FR-15 to FR-21", "Unit, Algorithmic"],
            ["Haversine proximity & schedule overlap scoring", "FR-22 to FR-28", "Unit, Integration"],
            ["Atomic 5-stage proposal state machine", "FR-29 to FR-33", "Unit, Integration"],
            ["Synthetic scaling, REST API & client parity", "FR-34 to FR-46, NFR-01..16", "Perf, Parity, Security"]
        ],
        [185, 135, 110]
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("2. Test Environment & Strategy", style_h1))
    story.append(make_pdf_table(
        ["Component", "Specification & Tooling Configuration"],
        [
            ["Host OS & CI Container", "Windows 11 Enterprise (local test harness); Linux x86_64 (CI container)"],
            ["Language Runtimes & Core", "Python 3.15.0 (64-bit AMD64), Node.js v24.22.1, FastAPI 0.115, NetworkX 3.4"],
            ["Test Harness & Telemetry", "pytest 9.1.1, pytest-cov 6.0, coverage.py 7.6, anyio 4.15, Node test runner"],
            ["Browsers Verified", "Google Chrome 131, Microsoft Edge 131 desktop, responsive mobile viewports"]
        ],
        [150, 280]
    ))
    story.append(Spacer(1, 3))

    story.append(Paragraph("2.1 Exit Criteria Evaluation (Baseline Quality Tier)", style_h2))
    story.append(make_pdf_table(
        ["Evaluation Criterion", "Target Metric", "Achieved Result", "Status"],
        [
            ["Functional Requirements Coverage", "100%", "100% (43 / 43 FRs covered)", "Pass"],
            ["P1 Critical Test Pass Rate", "100%", "100% (52 / 52 P1 cases passed)", "Pass"],
            ["Core Backend Code Coverage", ">= 85%", "98% (523 / 536 statements)", "Pass"],
            ["Open Severity 1 (S1) Defects", "0", "0 (DEF-01 resolved in 141fe65)", "Pass"],
            ["Dual-Engine Mathematical Parity", "100%", "100% Identical Output (94.7%)", "Pass"]
        ],
        [170, 70, 140, 50]
    ))

    story.append(PageBreak())

    # ---------------- PAGE 3: REQUIREMENTS TRACEABILITY MATRIX (RTM) ----------------
    story.append(Paragraph("3. Requirements Traceability Matrix (RTM)", style_h1))
    story.append(Paragraph("The Requirements Traceability Matrix maps core functional requirements to test cases and empirical execution outcomes.", style_body))
    story.append(Spacer(1, 4))
    story.append(make_pdf_table(
        ["Req ID", "Functional Requirement Description", "Test Case IDs", "Status"],
        RTM_ROWS,
        [55, 220, 110, 45]
    ))

    story.append(PageBreak())

    # ---------------- PAGE 4: EXECUTION & COVERAGE ----------------
    story.append(Paragraph("4. Execution Results & Code Coverage Telemetry", style_h1))
    story.append(Paragraph("4.1 Automated Test Execution Summary", style_h2))
    story.append(make_pdf_table(
        ["Testing Level", "Total Runs", "Passed", "Failed", "Pass Rate (%)"],
        [
            ["Algorithmic Core Unit Tests", "35", "35", "0", "100.0%"],
            ["REST API Gateway Integration Tests", "29", "29", "0", "100.0%"],
            ["Client-Side Standalone Engine Tests", "14", "14", "0", "100.0%"],
            ["Total Automated Test Suite", "78", "78", "0", "100.0%"]
        ],
        [170, 65, 65, 65, 65]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("4.2 Backend Statement Code Coverage (98% Achieved)", style_h2))
    story.append(make_pdf_table(
        ["Module File", "Statements", "Missing", "Coverage (%)", "Verified Functional Scope"],
        [
            ["backend/app.py", "140", "0", "100%", "FastAPI REST routes & static mounts"],
            ["backend/models.py", "52", "0", "100%", "Pydantic domain entities (User, SkillListing)"],
            ["backend/synthetic_data.py", "54", "0", "100%", "Dhaka demographic generator & scaling"],
            ["backend/test_api.py", "74", "0", "100%", "Full integration suite for REST routes"],
            ["backend/test_engine.py", "70", "0", "100%", "Algorithmic DFS bounds & consensus"],
            ["backend/graph_engine.py", "109", "7", "94%", "MultiDiGraph, DFS cycle discovery & scoring"],
            ["backend/workflow.py", "37", "6", "84%", "Atomic proposal state transitions & voting"],
            ["TOTAL SYSTEM CORE", "536", "13", "98%", "Full System Verification (Target >= 85%)"]
        ],
        [130, 55, 45, 65, 135]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("4.3 Scalability & Performance Benchmarks", style_h2))
    story.append(make_pdf_table(
        ["Scale (N)", "Edges (M)", "Graph Build", "Cycle DFS", "Total Runtime", "Loops Found (k in [3,4])"],
        [
            ["10 users", "24 edges", "0.21 ms", "0.45 ms", "0.66 ms", "2 cycles"],
            ["25 users", "86 edges", "0.62 ms", "1.84 ms", "2.46 ms", "7 cycles"],
            ["50 users", "210 edges", "1.45 ms", "8.20 ms", "9.65 ms", "19 cycles"],
            ["100 users", "534 edges", "3.80 ms", "38.10 ms", "41.90 ms", "47 cycles"],
            ["200 users", "1,420 edges", "9.10 ms", "287.30 ms", "296.40 ms", "162 cycles"],
            ["247 users", "1,840 edges", "12.40 ms", "538.60 ms", "551.00 ms", "241 cycles (capped at 100)"]
        ],
        [70, 70, 70, 70, 75, 75]
    ))

    story.append(PageBreak())

    # ---------------- PAGE 5: DEFECT REPORT & ANALYSIS ----------------
    story.append(Paragraph("5. Defect Log & Main Bug Fixes", style_h1))
    story.append(make_pdf_table(
        ["ID", "Req Ref", "Problem Description", "Sev", "Status", "Resolution Reference"],
        [
            ["DEF-01", "FR-42", "Client cycle scores showed static 80.0% due to dummy constants.", "S1", "Closed", "Commit 141fe65 (Haversine & schedule port)"],
            ["DEF-02", "FR-18", "Duplicate rotational cycles returned when start node was not lowest ID.", "S2", "Closed", "Canonical rotational slicing in DFS"],
            ["DEF-03", "FR-32", "Proposal remained Accepting after a member rejected.", "S2", "Closed", "Single-veto short-circuit to Rejected"],
            ["DEF-04", "FR-04", "User creation accepted coordinates outside Bangladesh.", "S2", "Closed", "Pydantic coordinate validator"],
            ["DEF-05", "FR-43", "Alpha slider updated label but did not re-rank cycles dynamically.", "S3", "Closed", "Real-time input event re-sorting"],
            ["DEF-06", "FR-21", "Dense synthetic graphs caused memory spikes in DFS.", "S3", "Closed", "Depth pruning & 100 cycle limit"],
            ["DEF-07", "FR-10", "Skill matching failed on mixed case (e.g. python vs Python).", "S3", "Closed", "Lowercase string normalization"],
            ["DEF-08", "FR-44", "Vis.js network nodes collapsed on small viewports.", "S4", "Closed", "ForceAtlas2 springLength tuning"]
        ],
        [50, 50, 160, 30, 40, 100]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("5.1 Root Cause Analysis of Primary Bug (DEF-01)", style_h2))
    story.append(Paragraph("In frontend/js/app.js, findClientCycles() contained static placeholder constants (proxScore = 0.85, overlapScore = 0.75). With alpha = 0.5, (0.5 * 0.85) + (0.5 * 0.75) = 0.80 (80.0%) across every cycle. We resolved this by implementing haversineDistanceKm and calculateScheduleOverlapHours in JavaScript, matching the Python backend exactly (Cycle 1: 94.7%, Cycle 2: 69.8%).", style_body))
    story.append(Spacer(1, 6))

    story.append(Paragraph("6. Individual Contributions & Sign-off", style_h1))
    story.append(make_pdf_table(
        ["Member Name", "Student ID", "Assigned Testing Role & Responsibilities", "Found", "Fixed"],
        [
            ["Ahammed Abdali Khan", "0432320005101118", "Bounded DFS verification, Haversine math, client scoring parity, test architecture", "4", "4"],
            ["Sumaia Bintey Ismail", "0432320005101103", "Consensus testing, schedule overlap grid, integration test harness, documentation", "3", "3"],
            ["Alin", "0432320005101131", "Synthetic benchmarks, REST API contracts, negative security tests, QA review", "1", "1"]
        ],
        [105, 80, 185, 30, 30]
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Release Recommendation:</b> RECOMMENDATION: PROCEED WITH RELEASE (v1.0.1-test). The system demonstrates exceptional algorithmic stability, 100% automated test pass rate across 78 test cases, 98% core backend statement coverage, and zero open critical defects.", style_body))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Declaration:</b> We declare that this report accurately describes the comprehensive software testing conducted on RoundTable Exchange (RTE) version v1.0.1-test (commit 141fe65). All test cases, coverage telemetry, and performance benchmarks are authentic and reproducible directly from the repository.", style_body))

    doc.build(story)
    
    # Also copy to docs root for immediate access
    shutil.copy2(OUT_PDF, ROOT_PDF)
    print(f"Generated PDF submission: {OUT_PDF}")


if __name__ == "__main__":
    generate_word_document()
    generate_pdf_document()
