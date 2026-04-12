# SWE-bench Trajectory Analyzer
 
A set of command-line tools for downloading, processing, and analysing
[mini-SWE-agent-v2](https://github.com/SWE-agent/mini-swe-agent) trajectory files
from [swebench.com](https://swebench.com).
 
Built as part of the JetBrains internship application (Quality Metrics for Agent Trajectories).
 
 ---
 
## Repository Structure
 
```
swe-trajectory-analyzer/
├── trackdata.py       # Task 1: CLI tool — counts messages in a trajectory file
├── trajectories.py    # Downloads all trajectories from Docent for a given model
├── analysis.ipynb     # Task 2 descriptive analsysis file
├── task-2.pdf         # Final report of task 2       
├── tracked_data/
│   ├── claude-4-5-opus-high_counts.csv
│   ├── claude-opus-4-6_counts.csv
│   ├── gemini-3-flash-high_counts.csv
│   ├── minimax-m2-5-high_counts.csv
│   ├── gpt5-2-codex_counts.csv
|   └── gpt5-2-codex_counts.csv
├── report.md                   # Task 2: Observations on top-5 model trajectories
├── paper_summary.md            # Task 3: Summary of the research paper
└── README.md
```
 
---

## Requirements
 
```bash
pip install docent-python   # only needed for trajectories.py to extract data from Docent
```
 
Everything else uses the Python standard library. Python 3.11+ required.
 
Create a account and a API Key to successfully utilize these scripts
---