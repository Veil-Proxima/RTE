# 🔄 The Round Table Exchange (RTE)
### *A Multi-Party Skill Barter Network with Graph-Based Cycle Matching*

[![GitHub Pages](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-blue?style=for-the-badge&logo=github)](https://kryton-system.github.io/RoundTable/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

---

## 📖 Overview

**The Round Table Exchange (RTE)** is an algorithmic skill-bartering platform that eliminates the traditional *"Double Coincidence of Wants"* bottleneck. Instead of requiring direct 1-to-1 matches or relying on synthetic time credits, RTE discovers **multi-party barter loops ($k = 3$ and $k = 4$ people)** using directed graph cycle matching algorithms inspired by Kidney Paired Donation models.

$$\text{User A (Teaches Python)} \xrightarrow{} \text{User B (Teaches Guitar)} \xrightarrow{} \text{User C (Teaches Spanish)} \xrightarrow{} \text{User A}$$

---

## ✨ Key Features

- **Directed Compatibility Graph Engine**: Automatically connects skill supply (`OFFER`) to demand (`WANT`) across users.
- **Bounded-Depth DFS Cycle Detection ($k \in [3, 4]$)**: Discovers closed triangular and quad exchange loops with rotational deduplication in $O(n \cdot m^{k-1})$ time.
- **Multi-Signal Ranking Function**:
  $$\text{score}(C) = \alpha \cdot \text{prox}(C) + (1 - \alpha) \cdot \text{overlap}(C)$$
  Balances Haversine geographic proximity decay with shared weekly availability hours.
- **Group Confirmation State Machine**: Atomic multi-user accept/reject protocol (`PENDING` $\to$ `CONFIRMED` / `REJECTED`).
- **Interactive Visual Network Canvas**: Visualizes the graph and illuminates active barter loops using `Vis.js`.
- **Synthetic Data Generator & Empirical Benchmarking**: Generates test populations (20 to 500+ nodes) and benchmarks algorithm latency in milliseconds.

---

## 🚀 Quick Start (Run Locally)

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/Kryton-System/RoundTable.git
cd RoundTable
pip install -r backend/requirements.txt
```

### 2. Start the FastAPI Server
```bash
python -m uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000
```
Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser.

### 3. Run Automated Tests & Code Coverage
```bash
python -m pytest
python -m coverage run --source=backend -m pytest
python -m coverage report -m
```

#### 🧪 Test Suite & Code Coverage Summary (98% Coverage)
All 13 unit and integration tests pass with comprehensive coverage across the entire system core:

| Module File | Statements | Missing | Coverage | Primary Tested Functionality |
|---|:---:|:---:|:---:|---|
| `backend/app.py` | 140 | 0 | **100%** | REST API gateway, route schemas, cycle matching & static mounts |
| `backend/models.py` | 52 | 0 | **100%** | Pydantic v2 data models, enums & entity validation |
| `backend/synthetic_data.py` | 54 | 0 | **100%** | Dhaka population generator & empirical benchmark runner |
| `backend/test_api.py` | 74 | 0 | **100%** | End-to-end integration tests for all REST endpoints & error paths |
| `backend/test_engine.py` | 70 | 0 | **100%** | Algorithmic DFS traversal, loop bounds, Haversine ranking & DAG checks |
| `backend/graph_engine.py` | 109 | 7 | **94%** | Multigraph construction, cycle deduplication & composite scoring |
| `backend/workflow.py` | 37 | 6 | **84%** | Atomic multi-party consensus state machine & group voting |
| **TOTAL (Backend Core)** | **536** | **13** | **98%** | **Full System Coverage (13/13 Tests Passing in 0.63s)** |

📄 **1-Page System Brief PDF:** [`SYSTEM_OVERVIEW_AND_COVERAGE.pdf`](file:///e:/Dev%20Stuff/RoundTable/SYSTEM_OVERVIEW_AND_COVERAGE.pdf)

---

## 🌐 Live In-Browser Demo
Visit the live interactive prototype on GitHub Pages:
👉 **[https://kryton-system.github.io/RoundTable/](https://kryton-system.github.io/RoundTable/)**

---

## 🏛️ Project Structure

```
RoundTable/
├── backend/
│   ├── app.py                 # FastAPI application, REST endpoints, and static mounts
│   ├── models.py              # Pydantic models (User, Listing, TradeCycle, TradeProposal)
│   ├── graph_engine.py        # Directed multigraph builder, Bounded-Depth DFS, ranking
│   ├── workflow.py            # Group confirmation state machine
│   ├── synthetic_data.py      # Dhaka presets, synthetic generator & benchmark suite
│   ├── requirements.txt       # Dependencies
│   └── test_engine.py         # Automated pytest test suite
├── frontend/
│   ├── index.html             # Semantic single-page dashboard layout
│   ├── css/
│   │   └── style.css          # Modern dark-mode glassmorphic design system
│   └── js/
│       ├── app.js             # Dual-mode REST client + in-browser fallback engine
│       └── graph_viz.js       # Interactive Vis.js network visualizer
├── docs/                      # Academic proposal documents & LaTeX sources
└── .github/workflows/
    └── deploy-pages.yml       # Automated GitHub Pages CI/CD workflow
```

---

## 👥 Authors
- **Ahmmad Abdali Khan** — Lead Software Engineer (*UITS CSE, Dhaka, Bangladesh*)
- **Sumaia Bintey Ismail** — Application & Systems Engineer (*UITS CSE, Dhaka, Bangladesh*)
- **Alin** — Software Engineer (*UITS CSE, Dhaka, Bangladesh*)
- **Supervised By:** Dr. Mahfida Amjad Dipa
