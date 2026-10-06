import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# Paths
BASE_DIR = r"e:\Dev Stuff\RoundTable"
IMAGES_DIR = os.path.join(BASE_DIR, "docs", "frontend_doc_images")
DOWNLOADS_DIR = r"C:\Users\Fahim\Downloads"
OUTPUT_DOCX = os.path.join(BASE_DIR, "UI_UX_Scaffolding_Documentation.docx")
ALT_OUTPUT_DOCX = os.path.join(BASE_DIR, "Frontend_UI_UX_Architecture_Documentation.docx")

os.makedirs(IMAGES_DIR, exist_ok=True)

# 1. Ensure cover logo is available
cover_logo_path = os.path.join(IMAGES_DIR, "cover_logo.png")
if not os.path.exists(cover_logo_path):
    # check if extracted in current dir
    temp_logo = os.path.join(BASE_DIR, "cover_logo.png")
    if os.path.exists(temp_logo):
        shutil.copy2(temp_logo, cover_logo_path)
    else:
        # fallback to uits.png
        uits_png = os.path.join(BASE_DIR, "docs", "proposal", "images", "uits.png")
        if os.path.exists(uits_png):
            shutil.copy2(uits_png, cover_logo_path)

# 2. Image mappings
image_map = {
    "cover_logo": ("cover_logo.png", "cover_logo.png"),
    "layout": ("2.drawio.png", "2.drawio.png"),
    "component_tree": ("3.drawio.png", "3.drawio.png"),
    "wireframe": ("initial_UI.png", "initial_UI.png"),
    "architecture": ("Untitled Diagram.drawio.png", "Untitled_Diagram.drawio.png"),
    "ui_explorer": ("image1.png", "ui_network_explorer.png"),
    "ui_confirmations": ("image2.png", "ui_trade_confirmations.png"),
    "ui_profiles": ("image3.png", "ui_user_profiles.png"),
    "ui_benchmarks": ("image4.png", "ui_benchmarks.png"),
}

local_image_paths = {}
for key, (src_name, dst_name) in image_map.items():
    dst_path = os.path.join(IMAGES_DIR, dst_name)
    src_path = os.path.join(DOWNLOADS_DIR, src_name)
    if os.path.exists(dst_path):
        local_image_paths[key] = dst_path
    elif os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
        local_image_paths[key] = dst_path
    else:
        print(f"Notice: Image {src_name} checked.")

def add_page_number(run):
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = "PAGE"
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

# Create Document
doc = docx.Document()

# Standard Letter Page Setup with 1-inch margins
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    section.page_width = Inches(8.5)
    section.page_height = Inches(11.0)

# Configure Default Style to Times New Roman (Matching UITS Academic Proposal Template)
style_normal = doc.styles['Normal']
style_normal.font.name = 'Times New Roman'
style_normal.font.size = Pt(12)
style_normal.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
style_normal.paragraph_format.line_spacing = 1.2
style_normal.paragraph_format.space_after = Pt(6)

COLOR_PRIMARY = RGBColor(0x11, 0x18, 0x27)    # Deep academic dark
COLOR_SECONDARY = RGBColor(0x1E, 0x3A, 0x5F)  # Dark navy blue
COLOR_MUTED = RGBColor(0x4B, 0x55, 0x63)      # Muted gray for captions

# -------------------------------------------------------------
# COVER PAGE: EXACT REPLICA OF THE UITS PROPOSAL COVER PAGE
# -------------------------------------------------------------
cover_section = doc.sections[0]
cover_section.different_first_page_header_footer = True

# University Header Block
p_u1 = doc.add_paragraph()
p_u1.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_u1.paragraph_format.space_before = Pt(10)
p_u1.paragraph_format.space_after = Pt(2)
r_u1 = p_u1.add_run("UNIVERSITY OF INFORMATION TECHNOLOGY AND SCIENCES")
r_u1.font.bold = True
r_u1.font.size = Pt(14.5)

p_u2 = doc.add_paragraph()
p_u2.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_u2.paragraph_format.space_before = Pt(0)
p_u2.paragraph_format.space_after = Pt(4)
r_u2 = p_u2.add_run("(UITS)")
r_u2.font.bold = True
r_u2.font.size = Pt(14.5)

p_u3 = doc.add_paragraph()
p_u3.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_u3.paragraph_format.space_before = Pt(0)
p_u3.paragraph_format.space_after = Pt(2)
r_u3 = p_u3.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING")
r_u3.font.bold = True
r_u3.font.size = Pt(14)

p_u4 = doc.add_paragraph()
p_u4.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_u4.paragraph_format.space_before = Pt(0)
p_u4.paragraph_format.space_after = Pt(20)
r_u4 = p_u4.add_run("DHAKA, BANGLADESH")
r_u4.font.size = Pt(11)

# Center Logo
if "cover_logo" in local_image_paths and os.path.exists(local_image_paths["cover_logo"]):
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(6)
    p_logo.paragraph_format.space_after = Pt(24)
    run_logo = p_logo.add_run()
    run_logo.add_picture(local_image_paths["cover_logo"], width=Inches(1.65))

# Document Title Type: UI/UX SCAFFOLDING
p_dtype = doc.add_paragraph()
p_dtype.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_dtype.paragraph_format.space_before = Pt(8)
p_dtype.paragraph_format.space_after = Pt(12)
r_dtype = p_dtype.add_run("UI/UX SCAFFOLDING")
r_dtype.font.bold = True
r_dtype.font.size = Pt(17)
r_dtype.font.color.rgb = COLOR_SECONDARY

# Project Name
p_pname = doc.add_paragraph()
p_pname.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_pname.paragraph_format.space_before = Pt(4)
p_pname.paragraph_format.space_after = Pt(36)
r_pname = p_pname.add_run("The Round Table Exchange (RTE): A Multi-Party Skill Barter Network\nwith Graph-Based Cycle Matching")
r_pname.font.bold = True
r_pname.font.size = Pt(13.5)

# Submitted By Block
p_sby = doc.add_paragraph()
p_sby.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sby.paragraph_format.space_before = Pt(6)
p_sby.paragraph_format.space_after = Pt(3)
r_sby = p_sby.add_run("Submitted By:")
r_sby.font.bold = True
r_sby.font.size = Pt(12)

p_snames = doc.add_paragraph()
p_snames.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_snames.paragraph_format.space_before = Pt(0)
p_snames.paragraph_format.space_after = Pt(20)
r_s1 = p_snames.add_run("Ahmmad Abdali Khan (ID: 0432320005101118)\nSumaia Bintey Ismail (ID: 0432320005101103)\nAlin (ID: 0432320005101131)")
r_s1.font.size = Pt(12)

# Submitted To Block
p_sto = doc.add_paragraph()
p_sto.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sto.paragraph_format.space_before = Pt(6)
p_sto.paragraph_format.space_after = Pt(3)
r_sto = p_sto.add_run("Submitted To:")
r_sto.font.bold = True
r_sto.font.size = Pt(12)

p_tname = doc.add_paragraph()
p_tname.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_tname.paragraph_format.space_before = Pt(0)
p_tname.paragraph_format.space_after = Pt(32)
r_t1 = p_tname.add_run("Dr. Mahfida Amjad Dipa\nDepartment of Computer Science and Engineering\nUniversity of Information Technology and Sciences (UITS)")
r_t1.font.size = Pt(12)

# Date of Submission
p_date = doc.add_paragraph()
p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_date.paragraph_format.space_before = Pt(6)
p_date.paragraph_format.space_after = Pt(0)
r_date = p_date.add_run("Date of Submission: 13 September 2026")
r_date.font.size = Pt(11)

# End of Cover Page
doc.add_page_break()

# -------------------------------------------------------------
# BODY SECTION
# -------------------------------------------------------------
# Setup Footer with Page Numbers
footer = doc.sections[0].footer
p_ftr = footer.paragraphs[0]
p_ftr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r_ftr_label = p_ftr.add_run("UI/UX Scaffolding | Page ")
r_ftr_label.font.name = 'Times New Roman'
r_ftr_label.font.size = Pt(9.5)
r_ftr_label.font.color.rgb = COLOR_MUTED
r_page = p_ftr.add_run()
r_page.font.name = 'Times New Roman'
r_page.font.size = Pt(9.5)
r_page.font.color.rgb = COLOR_MUTED
add_page_number(r_page)

def add_h1(text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(18)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.keep_with_next = True
    r = h.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = COLOR_SECONDARY
    return h

def add_h2(text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(4)
    h.paragraph_format.keep_with_next = True
    r = h.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = COLOR_PRIMARY
    return h

def add_body_p(text, bold_prefix=None, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.2
    p.paragraph_format.space_after = Pt(space_after)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if bold_prefix:
        r_b = p.add_run(bold_prefix)
        r_b.font.bold = True
    p.add_run(text)
    return p

def add_bullet(bold_prefix, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(4)
    if bold_prefix:
        r_b = p.add_run(bold_prefix + " ")
        r_b.font.bold = True
    p.add_run(text)
    return p

def add_image_centered(img_key, caption_text, width=Inches(6.2)):
    if img_key in local_image_paths and os.path.exists(local_image_paths[img_key]):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run = p_img.add_run()
        run.add_picture(local_image_paths[img_key], width=width)
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(12)
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = 'Times New Roman'
        r_cap.font.size = Pt(10)
        r_cap.font.italic = True
        r_cap.font.color.rgb = COLOR_MUTED
    else:
        p_ph = doc.add_paragraph()
        p_ph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p_ph.add_run(f"[Image placeholder: {caption_text}]")
        r.font.bold = True
        r.font.color.rgb = RGBColor(0xCC, 0x00, 0x00)

# -------------------------------------------------------------
# 1. INTRODUCTION
# -------------------------------------------------------------
add_h1("1. Introduction")

add_h2("1.1 Purpose of this Document")
add_body_p(
    "The purpose of this document is to provide a comprehensive specification of the frontend UI/UX architecture "
    "for the Multi-Party Trade Cycle Discovery Platform (The Round Table Exchange - RTE v2.4). This web application "
    "is designed to address the multi-lateral barter problem by discovering cyclic exchange paths among users who have "
    "complementary skill sets and item needs. Because multi-party exchanges (such as 3-party or 4-party swap loops) "
    "present high cognitive load for end-users, an intuitive, structured, and visually responsive interface is vital. "
    "This document outlines the layout hierarchy, component decomposition, low-fidelity wireframing, implemented system screens, "
    "system boundary definitions, and the user experience rationale guiding the frontend implementation."
)

add_h2("1.2 Scope")
add_body_p(
    "This document strictly covers the frontend user interface and user experience (UI/UX) layer of the platform. "
    "It details how visual elements are structured, how user interface components relate to one another, and how state "
    "is presented within the browser. All backend algorithmic computations—such as multigraph construction, bounded "
    "Depth-First Search (DFS) traversals, geographic Haversine distance computations, and database indexing—are completely "
    "outside the primary scope of this document, except where the frontend interfaces with the backend service boundary "
    "via standardized REST/JSON APIs."
)

add_h2("1.3 Technology Stack Used for Frontend")
add_body_p(
    "To achieve fast rendering, low computational overhead, and direct control over DOM manipulation, the frontend is built using "
    "native web standards without heavy third-party framework overhead:"
)
add_bullet("HTML5:", "Provides semantic markup, accessible structure, and the foundation for the single-page dashboard.")
add_bullet("CSS3:", "Implements a modern, high-contrast dark theme utilizing Flexbox, CSS Grid layouts, and CSS custom variables for visual consistency.")
add_bullet("Vanilla JavaScript (ES6+):", "Manages application state, handles user interactions, orchestrates API requests via the Fetch API, and performs dynamic DOM manipulation.")
add_bullet("Vis.js (vis-network):", "A physics-driven canvas visualization library used to render interactive directed multi-graphs, representing users as nodes and barter desires as directed edges.")

# -------------------------------------------------------------
# 2. UI LAYOUT HIERARCHY
# -------------------------------------------------------------
add_h1("2. UI Layout Hierarchy")
add_body_p(
    "The user interface of the platform is organized as a unified single-page dashboard bounded within the active browser window. "
    "The display is arranged hierarchically from top to bottom and across functional workspace columns to minimize navigation friction "
    "and keep all operational tools in direct view."
)

add_image_centered("layout", "Figure 1: Overall UI Layout Hierarchy of the Platform.", width=Inches(4.6))

add_body_p("The layout hierarchy consists of the following primary structural sections:")
add_bullet("Browser Viewport (100vw x 100vh):", "Serves as the top-level boundary containing the entire web application. It prevents window scrolling and ensures that all sub-containers fit proportionally inside the user's active screen.")
add_bullet("Application Header:", "Positioned across the top of the viewport. It houses the platform identity, navigation module tabs, operational telemetry, and global controls.")
add_bullet("Metrics Strip:", "Located immediately below the header. It acts as an aggregate status banner displaying real-time platform metrics, including active users, registered listings, discovered cycles, and pending trade proposals.")
add_bullet("Explorer Grid Workspace:", "The primary multi-column work area of the application. It organizes complex user interactions into three distinct side-by-side functional blocks:")
add_bullet("  • Control Panel (Left Column):", "Houses input sliders, depth limit selectors, and execution triggers allowing the user to configure trade discovery parameters.")
add_bullet("  • Graph Visualizer Canvas (Center Column):", "An interactive HTML5 canvas surface powered by Vis.js that visually renders users as nodes and trade desires as directed edges, complete with real-time physics stabilization.")
add_bullet("  • Cycle Results Panel (Right Column):", "Displays ranked, card-based trade cycle suggestions generated by the system, allowing users to inspect trade paths and initiate multi-party proposals.")
add_bullet("Modal Presentation Layer:", "An overlay surface that sits above the primary dashboard. It is dynamically triggered whenever targeted actions require focused user attention, such as profile registration or multi-step trade confirmation.")

# -------------------------------------------------------------
# 3. COMPONENT TREE / COMPONENT HIERARCHY
# -------------------------------------------------------------
add_h1("3. Component Tree / Component Hierarchy")
add_body_p(
    "To maintain clean code organization and separation of concerns in Vanilla JavaScript, the UI architecture follows a "
    "modular, hierarchical component tree. The entire application originates from a single root component (AppRoot) and "
    "branches down into specialized structural and operational subcomponents."
)

add_image_centered("component_tree", "Figure 2: Component Tree and Structural Decomposition.", width=Inches(6.2))

add_h2("3.1 Description of Major Components")

add_body_p(
    "The main controller of the frontend application. It initializes global application state, coordinates asynchronous "
    "communication with the backend API, and mounts top-level UI containers into the DOM.",
    bold_prefix="AppRoot (Root Component): "
)

add_body_p(
    "Controls the upper banner of the dashboard. It contains two key subcomponents:",
    bold_prefix="HeaderRegion & HeaderContainer: "
)
add_bullet("NavigationTabs:", "Allows the user to switch between the primary 'Explorer View', 'Consensus View', 'User Profile', and 'Benchmark' screens without reloading the browser page.")
add_bullet("StatusIndicator:", "Provides visual feedback regarding engine connectivity, active data polling, and backend health status.")

add_body_p(
    "An independent overlay container that remains inactive until called. It hosts modal dialog forms (such as UserRegistrationModal) "
    "for inputting user attributes, adding trade listings, and validating inputs before dispatching them to the state manager.",
    bold_prefix="OverlayLayer & UserRegistrationModal: "
)

add_body_p(
    "Renders the horizontal summary row using repeated MetricCards. Each card binds directly to aggregate counters "
    "(e.g., Total Users, Discovered Cycles, Active Proposals) and updates dynamically whenever new cycles or network nodes are loaded.",
    bold_prefix="MetricsRegion & MetricsStrip: "
)

add_body_p(
    "The central container responsible for rendering the active functional view based on tab selection:",
    bold_prefix="MainWorkspace: "
)
add_bullet("ExplorerView (Active Default View):", "The primary view for graph inspection and cycle discovery, subdivided into three coordinated modules:")
add_bullet("  • EngineControlPanel:", "Contains controls such as the WeightSliderControl (for tuning scoring weights) and the Action: Run Engine button to trigger discovery routines.")
add_bullet("  • NetworkGraph:", "Encapsulates the Vis.js canvas viewport, handling node drag-and-drop actions, edge rendering, zoom-pan interactions, and visual highlight states.")
add_bullet("  • CycleResultsList:", "Renders a scrollable container of CycleCardComponent items. Each card represents a valid circular trade loop and provides an Action: Initiate Proposal trigger that moves the selected trade into multi-party negotiation.")
add_bullet("ConsensusView:", "The secondary workspace view used to monitor group confirmations, vote status, and execution progress for multi-party swaps that have already been proposed.")

# -------------------------------------------------------------
# 4. INITIAL HAND-DRAWN UI SKETCH (LOW-FIDELITY WIREFRAME)
# -------------------------------------------------------------
add_h1("4. Initial Hand-Drawn UI Sketch (Low-Fidelity Wireframe)")
add_body_p(
    "During the initial design and requirements gathering phase, a low-fidelity wireframe was sketched by hand. "
    "The purpose of this preliminary sketch was to conceptualize the information architecture, determine panel arrangements, "
    "and validate the usability of a single-screen layout prior to any software implementation."
)

add_image_centered("wireframe", "Figure 3: Initial Hand-Drawn Low-Fidelity UI Wireframe.", width=Inches(5.8))

add_h2("4.1 Evolution from Sketch to Final Architecture")
add_body_p("The initial sketch established the core functional layout that carried forward into the final system:")
add_bullet("1. Top Navigation & Metric Placement:", "The hand-drawn concept placed the title, navigation tabs (NETWORK, Trade con., U. PROFILE, BENCHMARK), and a dedicated metric strip (TOTAL USERS, Cycles, 3-PARTY, 4-PARTY, PROPOSAL) across the top. This validated that high-level telemetry should always remain visible to the user regardless of lower panel states.")
add_bullet("2. Three-Column Operational Division:", "The sketch partitioned the main operational area into three columns: ALGORITHM CONTROL on the left, GRAPH UI in the center, and RESULTS on the right. Testing this concept confirmed that users can logically adjust algorithmic inputs on the left, observe the network structure in the center, and inspect discovered outputs on the right in a natural left-to-right visual flow.")
add_bullet("3. Refinement into Component Hierarchy:", "While the initial sketch represented static screen sections, it was systematically translated into the formal layout hierarchy (Section 2) and component tree (Section 3). The GRAPH UI box evolved into the Vis.js-backed NetworkGraph canvas; the ALGORITHM CONTROL column became the parameter-driven EngineControlPanel; and the RESULTS column matured into the interactive, card-driven CycleResultsList equipped with proposal dispatch triggers.")

# -------------------------------------------------------------
# 5. FRONTEND POSITION WITHIN OVERALL SYSTEM ARCHITECTURE
# -------------------------------------------------------------
add_h1("5. Frontend Position within Overall System Architecture")
add_body_p(
    "The frontend client serves as the presentation and interaction gateway within the larger multi-tier platform architecture. "
    "It isolates the user from the internal complexity of algorithmic graph engines and database transactions while maintaining "
    "an interactive, real-time visual environment."
)

add_image_centered("architecture", "Figure 4: End-to-End System Architecture and Data Flow Boundary.", width=Inches(6.4))

add_h2("5.1 The Frontend Layer and API Boundary")
add_body_p(
    "As depicted in the system architecture diagram, the Frontend Layer (Vanilla JS + Vis.js) encompasses five core presentation modules:"
)
add_bullet("Live Graph Canvas:", "Implements real-time visualization using Vis.js with a ForceAtlas2 physics solver.")
add_bullet("Ranked Cycle Explorer:", "Presents ranked candidate cycles via responsive sidebar cards.")
add_bullet("Group Confirmation Console:", "Provides a state machine interface for multi-party trade consensus and voting.")
add_bullet("User & Listing Manager:", "Manages profile creation, item listings, and trade preferences through modal dialogs.")
add_bullet("Scalability Benchmark View:", "Displays performance metrics, execution times, and graph scale counters in a structured telemetry table.")

add_body_p(
    "The Frontend Layer communicates with the Backend Gateway (FastAPI) strictly across a decoupled REST/JSON boundary. "
    "The frontend serializes user inputs into JSON payloads, dispatches asynchronous HTTP requests (GET, POST) using the browser's "
    "Fetch API, and parses the returned JSON responses to update its local data stores and visual components. The frontend remains "
    "entirely decoupled from backend implementation details—such as whether the backend runs an in-memory graph store, executes "
    "bounded Depth-First Search (DFS) traversals, or computes multi-signal geographic ranking."
)

# -------------------------------------------------------------
# 6. IMPLEMENTED HIGH-FIDELITY WORKSPACE VIEWS
# -------------------------------------------------------------
add_h1("6. Implemented High-Fidelity Workspace Views")
add_body_p(
    "This section presents the actual implemented interfaces of RoundTable Exchange v2.4. Each screen demonstrates the concrete "
    "realization of the architectural wireframes and visual design tokens in a responsive, high-contrast cyber-teal dark interface."
)

add_h2("6.1 Network & Cycle Explorer Workspace")
add_body_p(
    "The Network Explorer serves as the primary operational console where evaluators tune ranking weights, select cycle depth bounds, "
    "and inspect circular trade dependencies on an interactive canvas."
)
add_image_centered("ui_explorer", "Figure 5: Implemented Network & Cycle Explorer Workspace (RoundTable Exchange v2.4).", width=Inches(6.2))
add_bullet("Ranking Weight Slider (α = 0.60):", "Interactively balances Schedule Overlap against Location Proximity (sched: 60% · loc: 40%).")
add_bullet("Loop Size Bounds Selector (k):", "Pill selector toggling between 2-party, 3-party (active), and 4-party trade loop detection.")
add_bullet("Interactive Graph Canvas:", "Vis.js-powered force-directed graph (8 Nodes · 8 Edges) highlighting active trade participants (U01-U04) in luminous purple/cyan edges while non-participating nodes (U05-U08) are dimmed.")
add_bullet("Active Cycle Telemetry:", "Step-by-step cycle breakdown (Rafi A. [Coding] → Mira K. [Design] → Tariq H. [Cooking]).")

add_h2("6.2 Group Confirmation Console (Trade Confirmations)")
add_body_p(
    "The Trade Confirmations screen implements an atomic multi-party state machine where all barter participants must approve a circular "
    "exchange before it transitions to execution."
)
add_image_centered("ui_confirmations", "Figure 6: Implemented Trade Confirmations Console & Atomic State Machine.", width=Inches(6.2))
add_bullet("Filter Status Controls:", "Categorizes trade agreements by status: ALL, PENDING (e.g. TXN-4821), PARTIAL (TXN-4819), CONFIRMED (TXN-4815), and EXPIRED (TXN-4810).")
add_bullet("5-Stage Atomic State Machine:", "Tracks consensus step-by-step: 1. Proposed (DFS matched) → 2. Notified (All participants alerted) → 3. Accepting → 4. Locked → 5. Executed.")
add_bullet("Skill Exchange Matrix & Action:", "Displays circular skill transfers (Coding → Design → Cooking → Coding) and provides the 'Accept Trade' confirmation button.")

add_h2("6.3 User Directory & Listing Manager (User Profiles)")
add_body_p(
    "The User Profiles screen manages registered participants, showing their neighborhood locations across Dhaka, reputation ratings, "
    "and skill competencies offered versus wanted."
)
add_image_centered("ui_profiles", "Figure 7: Implemented User Profiles Directory & Skill Tag Manager.", width=Inches(6.2))
add_bullet("Instant Directory Search:", "Search input supporting real-time filtering by user name, neighborhood (Gulshan, Banani, Dhanmondi, Uttara, Mirpur), or skill.")
add_bullet("Detailed Profile Card (Rafi Ahmed - U01):", "Shows verification status (ACTIVE), 14 trades completed, 4.9★ rating, skills offered (Python, React, ML, Data Viz), and skills wanted (UI/UX Design, Bengali tutoring).")
add_bullet("Action Triggers:", "Provides direct 'Propose Exchange' and 'View Graph' shortcuts.")

add_h2("6.4 Empirical Scalability Benchmarks View")
add_body_p(
    "The Benchmarks workspace provides runtime telemetry and empirical validation of the bounded cycle search algorithm across scaling user populations."
)
add_image_centered("ui_benchmarks", "Figure 8: Implemented Scalability Benchmarks & Complexity Telemetry.", width=Inches(6.2))
add_bullet("Complexity & Live Metrics:", "Highlights empirical complexity bound O(n · m^(k-1)), current population N=247 active users, average latency 551 ms (k=3), and 241 cycles found.")
add_bullet("Dual Empirical Tables:", "Telemetry tables charting Execution Time (ms) vs N (showing exponential inflection from 0.4 ms up to 551 ms) and Cycles Detected vs N.")
add_bullet("Synthetic Injection Buttons:", "Single-click '+20' and '+50' synthetic user injectors enabling live load-testing.")

# -------------------------------------------------------------
# 7. KEY UI/UX DESIGN DECISIONS
# -------------------------------------------------------------
add_h1("7. Key UI/UX Design Decisions")
add_body_p(
    "The user experience of the platform was shaped by several deliberate design choices aimed at reducing user confusion during multi-party trade operations:"
)
add_bullet("Single-Page Dashboard Layout:", "A single-page design with a fixed-height (100vh) viewport was chosen over traditional multi-page navigation. Because analyzing trade cycles requires concurrent visibility of parameters, network structures, and discovered loops, keeping all panels visible simultaneously eliminates context switching and cognitive fatigue.")
add_bullet("Real-Time Physics-Driven Graph Visualization (Vis.js):", "Representing barter dependencies as plain text tables makes multi-hop cycles (A gives to B, B gives to C, C gives to A) difficult to interpret. Integrating the Vis.js physics engine allows nodes to dynamically self-organize into natural clusters, enabling users to visually trace cycle paths and understand trade loops intuitively.")
add_bullet("Modal-Based Forms for Data Entry:", "User registration, listing submissions, and trade parameter updates are handled through focused modal dialogs rather than separate dedicated web pages. This preserves the current state of the graph canvas and inspection results in the background while the user completes focused data entry tasks.")
add_bullet("Ranked Card Pattern for Cycle Results:", "Discovered trade cycles are displayed in the right sidebar as individual, modular cards ordered by ranking score. Each card summarizes party participants, cycle size (e.g., 3-party vs. 4-party), and estimated trade quality, allowing users to easily scan, compare, and expand specific trade opportunities.")
add_bullet("Prominent Metric Strip for Situational Awareness:", "Positioning a dedicated horizontal metrics strip directly below the header guarantees that vital platform telemetry (e.g., total active participants, candidate loop count, and active trade proposals) is readable at a glance without having to drill into complex tables or reports.")

# -------------------------------------------------------------
# 8. CONCLUSION
# -------------------------------------------------------------
add_h1("8. Conclusion")
add_body_p(
    "This scaffolding document has presented the complete frontend UI/UX architecture for the Multi-Party Trade Cycle Discovery Platform "
    "(The Round Table Exchange - RTE v2.4). By establishing the visual layout hierarchy, defining the modular component tree, tracing the interface's "
    "evolution from low-fidelity wireframes, and detailing the implemented high-fidelity application screens and design decisions, "
    "this document captures both the conceptual planning and working reality of the software. The resulting architecture ensures that complex "
    "multi-lateral barter cycles can be explored, evaluated, and executed through a responsive, transparent, and user-friendly interface."
)

# Save document
doc.save(OUTPUT_DOCX)
print("Primary Docx created successfully at:", OUTPUT_DOCX)

# Also try writing to ALT_OUTPUT_DOCX if not locked
try:
    doc.save(ALT_OUTPUT_DOCX)
    print("Alternative Docx also updated at:", ALT_OUTPUT_DOCX)
except Exception as e:
    print("Notice: Could not overwrite alternate file (likely open in Word):", e)
