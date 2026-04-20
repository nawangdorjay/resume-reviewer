"""
AI Resume Reviewer — CLI Entry Point
Usage: python main.py resume.pdf [--job-desc job.txt] [--format text|json]
"""

import argparse
import sys
from pathlib import Path

from reviewer.parser import parse_resume
from reviewer.analyzer import analyze_resume
from reviewer.scorer import score_resume
from reviewer.report import print_report, json_report


def main():
    parser = argparse.ArgumentParser(
        description="📄 AI Resume Reviewer — Score and improve your resume"
    )
    parser.add_argument("resume", help="Path to resume file (PDF, DOCX, or TXT)")
    parser.add_argument("--job-desc", "-j", help="Path to job description file for keyword matching")
    parser.add_argument("--format", "-f", choices=["text", "json"], default="text", help="Output format")

    args = parser.parse_args()

    resume_path = Path(args.resume)
    if not resume_path.exists():
        print(f"❌ File not found: {resume_path}")
        sys.exit(1)

    # Step 1: Parse resume
    print("📄 Parsing resume...", file=sys.stderr)
    text = parse_resume(resume_path)
    if not text.strip():
        print("❌ Could not extract text from resume. Is the file corrupted?")
        sys.exit(1)

    # Step 2: Parse job description (optional)
    job_text = ""
    if args.job_desc:
        job_path = Path(args.job_desc)
        if job_path.exists():
            job_text = parse_resume(job_path)
        else:
            print(f"⚠️ Job description not found: {job_path}, skipping keyword matching", file=sys.stderr)

    # Step 3: Analyze
    print("🔍 Analyzing...", file=sys.stderr)
    analysis = analyze_resume(text, job_text)

    # Step 4: Score
    scores = score_resume(analysis)

    # Step 5: Report
    if args.format == "json":
        print(json_report(scores, analysis))
    else:
        print_report(scores, analysis)


if __name__ == "__main__":
    main()
