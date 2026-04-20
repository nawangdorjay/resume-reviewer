# 📄 AI Resume Reviewer

An intelligent resume analysis tool that scores your resume and provides actionable improvement suggestions. Uses NLP to analyze content quality, keyword optimization, section completeness, and formatting.

> Built by [Nawang Dorjay](https://github.com/nawangdorjay) — B.Tech CSE (Data Science), MAIT Delhi.

---

## ✨ Features

- **Overall Score** — 0-100 rating with breakdown by category
- **Section Analysis** — Checks for essential sections (education, experience, skills, projects)
- **Keyword Matching** — Compares against job description keywords
- **Action Verb Check** — Flags passive language, suggests strong verbs
- **Quantification Detection** — Identifies missing metrics and numbers
- **Length & Readability** — Optimal length recommendations
- **Format Support** — PDF, DOCX, and plain text
- **Detailed Report** — Category-wise breakdown with specific fix suggestions

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/nawangdorjay/resume-reviewer.git
cd resume-reviewer

# Install
pip install -r requirements.txt

# Review a resume
python main.py resume.pdf

# Review against a job description
python main.py resume.pdf --job-desc job_description.txt

# JSON output
python main.py resume.pdf --format json
```

---

## 📊 Sample Output

```
═══════════════════════════════════════════════════
  📄 RESUME REVIEW REPORT
═══════════════════════════════════════════════════

  Overall Score: 72/100

  ┌─────────────────────────┬───────┐
  │ Category                │ Score │
  ├─────────────────────────┼───────┤
  │ Section Completeness    │  8/10 │
  │ Content Quality         │  7/10 │
  │ Keyword Optimization    │  6/10 │
  │ Action Verbs            │  8/10 │
  │ Quantification          │  5/10 │
  │ Length & Readability    │  9/10 │
  └─────────────────────────┴───────┘

  ✅ STRENGTHS
  • Well-structured with clear sections
  • Strong action verbs used consistently
  • Good project descriptions

  ⚠️ IMPROVEMENTS NEEDED
  • Add metrics to 3 bullet points (e.g., "improved X by 40%")
  • Missing keywords: docker, kubernetes, ci/cd
  • Experience section could use more detail
```

---

## 📁 Project Structure

```
resume-reviewer/
├── main.py                     # CLI entry point
├── reviewer/
│   ├── __init__.py
│   ├── parser.py               # Resume text extraction (PDF/DOCX/TXT)
│   ├── analyzer.py             # Core analysis engine
│   ├── scorer.py               # Scoring logic
│   ├── keywords.py             # Keyword matching & ATS optimization
│   └── report.py               # Report generation
├── templates/
│   └── strong_verbs.json       # Action verbs database
├── tests/
│   └── test_reviewer.py        # Test suite
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **pdfplumber** — PDF text extraction
- **python-docx** — DOCX parsing
- **spaCy** — NLP processing (tokenization, POS tagging)
- **rich** — Beautiful terminal output
- **argparse** — CLI interface

---

## 🧑‍💻 About

Built by **Nawang Dorjay** — 2nd-year B.Tech CSE (Data Science) student from Leh, Ladakh. This project demonstrates NLP skills, text processing, and building practical developer tools.

---

## 📜 License

MIT
