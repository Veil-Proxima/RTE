# The Round Table Exchange (RTE) — System Details & Test Coverage
### *A Multi-Party Skill Barter Network with Graph-Based Cycle Matching (v2.4)*
**Department of Computer Science & Engineering | University of Information Technology and Sciences (UITS)**  
*Authors: Ahmmad Abdali Khan (0432320005101118), Sumaia Bintey Ismail (0432320005101103), Alin (0432320005101131) | Supervisor: Dr. Mahfida Amjad Dipa*  
*Date of Submission: 13 September 2026*

---

## 1. System Architectural Overview & Core Mechanics

The Round Table Exchange (RTE) is an algorithmic bartering platform designed to eliminate the *"Double Coincidence of Wants"* problem. Instead of forcing rigid 1-to-1 trades or introducing synthetic fiat/time credits, RTE discovers closed, cyclic barter paths across multiple participants ($k \in \{2, 3, 4\}$ users).

* **Graph Construction & Cycle Traversal:** The system constructs a directed multigraph where nodes represent users and directed edges indicate verified skill offers matching another user's skill wants. A Bounded-Depth Depth-First Search (DFS) engine traverses the multigraph to isolate cycles of length $k \in [2, 4]$ while applying rotational canonical deduplication to bound runtime complexity to $\mathcal{O}(n \cdot m^{k-1})$.
* **Multi-Signal Composite Ranking:** Discovered loops are scored using an empirical balancing equation:
  $$S(C) = \alpha \cdot S_{\text{geo}}(C) + (1 - \alpha) \cdot S_{\text{sched}}(C)$$
  where $\alpha \in [0.0, 1.0]$ dynamically weights Haversine geographic proximity decay against shared weekly availability windows.
* **Atomic Consensus State Machine:** Multi-party agreements are coordinated via an atomic 5-stage state machine (`Proposed` $\rightarrow$ `Notified` $\rightarrow$ `Accepting` $\rightarrow$ `Locked` $\rightarrow$ `Executed`). The protocol enforces single-veto integrity—if any participant rejects, the proposal terminates immediately to protect barter safety.
* **Dual-Engine Execution Architecture:** High-throughput production deployments communicate with a **FastAPI** Python REST backend, while a self-contained **In-Browser JavaScript Engine** guarantees 100% offline client-side functionality for static hosting on GitHub Pages.

---

## 2. Technical Specifications

| Layer / Subsystem | Primary Technologies | Core Operational Responsibilities |
|---|---|---|
| **Client Frontend** | HTML5, CSS3, Vanilla JS (ES6+), Vis.js | Single-page responsive dashboard, ForceAtlas2 physics canvas, cycle isolation, consensus console |
| **Backend Gateway** | FastAPI, Uvicorn, Pydantic v2, Python 3.14 | High-performance asynchronous REST API, schema validation, state storage, and static serving |
| **Algorithmic Core** | NetworkX, Bounded DFS, Geodesic math | Directed multigraph modeling, bounded cycle detection, Haversine proximity & schedule ranking |
| **State Machine** | Python Workflow Engine (In-Memory/Client) | Atomic multi-user consensus management, timeout invalidation, group voting lifecycle |
| **Benchmarking Suite** | Synthetic Dhaka Population Generator | Empirical scaling verification ($\mathcal{O}(n \cdot m^{k-1})$) from 20 up to 500+ nodes with latency telemetry |

---

## 3. Automated Test Verification & Code Coverage (98%)

The platform includes a test suite covering both algorithmic graph routines and FastAPI REST endpoints.

* **Test Execution Summary:** **13 / 13 tests passed** in **0.63s** (100% test pass rate).
* **Overall Core Coverage:** **98%** (523 of 536 statements covered).

```bash
# Automated Test Execution Commands
python -m pytest
python -m coverage run --source=backend -m pytest
python -m coverage report -m
```

| Module File | Statements | Miss | Coverage | Tested Scope & Quality Assurance |
|---|:---:|:---:|:---:|---|
| [`backend/app.py`](file:///e:/Dev%20Stuff/RoundTable/backend/app.py) | 140 | 0 | **100%** | All REST endpoints (users, matching, proposals, synthetic benchmarks, reset) |
| [`backend/models.py`](file:///e:/Dev%20Stuff/RoundTable/backend/models.py) | 52 | 0 | **100%** | Pydantic v2 domain models (`User`, `SkillListing`, `TradeCycle`, `TradeProposal`) |
| [`backend/synthetic_data.py`](file:///e:/Dev%20Stuff/RoundTable/backend/synthetic_data.py) | 54 | 0 | **100%** | Synthetic Dhaka population generator and empirical scaling benchmarking suite |
| [`backend/test_api.py`](file:///e:/Dev%20Stuff/RoundTable/backend/test_api.py) | 74 | 0 | **100%** | Full integration test harness verifying REST API contract compliance & error handling |
| [`backend/test_engine.py`](file:///e:/Dev%20Stuff/RoundTable/backend/test_engine.py) | 70 | 0 | **100%** | Algorithmic unit tests (3-loops, 4-loops, DAG acyclic checks, Haversine, consensus) |
| [`backend/graph_engine.py`](file:///e:/Dev%20Stuff/RoundTable/backend/graph_engine.py) | 109 | 7 | **94%** | Multigraph construction, bounded DFS traversal, cycle deduplication & scoring |
| [`backend/workflow.py`](file:///e:/Dev%20Stuff/RoundTable/backend/workflow.py) | 37 | 6 | **84%** | Proposal creation, unanimous group acceptance, single-rejection termination |
| **TOTAL (Backend System)** | **536** | **13** | **98%** | **Comprehensive End-to-End System & Algorithmic Verification** |

---
*Official 1-Page Academic Summary Document — University of Information Technology and Sciences (UITS)*
