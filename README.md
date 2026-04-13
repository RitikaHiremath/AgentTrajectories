# SWE-bench Trajectory Analyzer
 
A set of command-line tools for downloading, processing, and analysing
[mini-SWE-agent-v2](https://github.com/SWE-agent/mini-swe-agent) trajectory files
from [swebench.com](https://swebench.com).

Built as part of the JetBrains internship application tasks.

---
 
## Repository Structure
 
```
swe-trajectory-analyzer/
├── Trackdata.py       # Task 1: CLI tool — counts messages in a trajectory file
├── Trajectories.py    # Downloads all trajectories from Docent for a given model
├── Analysis.ipynb     # Task 2 descriptive analsysis file
├── Task_2.pdf         # Final report of task 2
├── Task_3.pdf         # Final report of task 3     
├── tracked_data/
│   ├── claude-4-5-opus-high_counts.csv
│   ├── claude-opus-4-6_counts.csv
│   ├── gemini-3-flash-high_counts.csv
│   ├── minimax-m2-5-high_counts.csv
|   └── gpt5-2-codex_counts.csv
└── README.md
```
 
---

## Requirements
 
```bash
pip install docent-python   # only needed for trajectories.py to extract data from Docent
```

To download trajectories, create a free account at docent.transluce.org and generate an API key under Settings.
Everything else uses the Python standard library. Python 3.11+ required.

---
