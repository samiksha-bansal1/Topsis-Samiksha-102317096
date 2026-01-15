# TOPSIS Multi-Criteria Decision Analysis

**TOPSIS** (Technique for Order of Preference by Similarity to Ideal Solution) is a multi-criteria decision analysis method that ranks alternatives based on their distance from ideal solutions.

---

## 🎯 Assignment Overview

This repository contains three complete implementations of TOPSIS as part of an academic assignment:

| Program | Description | Link |
|---------|-------------|------|
| **Program 1** | Command-line Python script | [View Code](./Program1) |
| **Program 2** | Published PyPI Package | [PyPI Link](https://pypi.org/project/Topsis-Samiksha-102317096/) |
| **Program 3** | Web Application | [Live Demo](https://topsis-samiksha-102317096-kvch.vercel.app/) |

---

## 📦 Program 1: Command-Line Implementation

Standalone Python script for TOPSIS analysis via command line.

**Usage:**
```bash
python 102317096.py 102317096-data.csv "1,1,1,1,1" "+,+,-,+,-" 102317096-result.csv
```

📂 **[View Code →](./Program1)**

---

## 📦 Program 2: Python Package on PyPI

Installable Python package for TOPSIS analysis.

**Installation:**
```bash
pip install Topsis-Samiksha-102317096
```

**Usage:**
```bash
topsis input.csv "1,1,1,2" "+,+,-,+" result.csv
```

**Links:**
- 📦 [PyPI Package](https://pypi.org/project/Topsis-Samiksha-102317096/)
- 📂 [View Code →](./Program2%20(Pypi%20package))

---

## 🌐 Program 3: Web Application

Flask web app with email notification for TOPSIS results.

**Features:** File upload • Real-time validation • Email results • Responsive UI

**Links:**
- 🌐 [Live Demo](https://topsis-samiksha-102317096-kvch.vercel.app/)
- 📂 [View Code →](./Program3%20(Webapp))

**Run Locally:**
```bash
cd "Program3 (Webapp)"
pip install -r requirements.txt
python app.py
```

---

## 📊 Input Format

**CSV File:**
```csv
Model,Price,Storage,Camera,Looks
M1,250,16,12,5
M2,200,16,8,3
```

- **First column:** Names
- **Other columns:** Numeric values
- **Weights:** `"1,1,1,2"` (comma-separated)
- **Impacts:** `"+,+,-,+"` (+ benefit, - cost)

**Output:** Adds `Topsis Score` and `Rank` columns

---

## 📁 Repository Structure

```
Topsis-Samiksha-102317096/
│
├── Program1/                      # Command-line script
│   ├── 102317096.py              # Main TOPSIS implementation
│   ├── 102317096-data.csv        # Sample input
│   └── 102317096-result.csv      # Sample output
│
├── Program2 (Pypi package)/      # PyPI package source
│   ├── topsis_samiksha_102317096/
│   ├── setup.py
│   └── README.md
│
├── Program3 (Webapp)/            # Web application
│   ├── app.py                    # Flask backend
│   ├── templates/
│   │   └── index.html           # Frontend
│   ├── requirements.txt
│   ├── vercel.json
│   └── .env.example
│
└── README.md                     # This file
```

---

## 👤 Author

**Samiksha Bansal** • Roll Number: **102317096**  
🔗 [GitHub](https://github.com/samiksha-bansal1) • 📦 [PyPI Package](https://pypi.org/project/Topsis-Samiksha-102317096/)

---

**⭐ Star this repository if you find it helpful!**