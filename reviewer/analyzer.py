"""
Resume Analyzer — Core analysis engine.
Detects sections, checks content quality, finds issues.
"""

import re
import json
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


def analyze_resume(text: str, job_text: str = "") -> dict:
    """Run all analysis checks on resume text and return structured results."""
    
    return {
        "sections": _detect_sections(text),
        "action_verbs": _check_action_verbs(text),
        "quantification": _check_quantification(text),
        "contact_info": _check_contact_info(text),
        "length": _check_length(text),
        "keywords": _match_keywords(text, job_text),
        "passive_voice": _detect_passive_voice(text),
        "bullet_points": _analyze_bullet_points(text),
        "raw_text": text,
    }


# ── Section Detection ──────────────────────────────────────────────

SECTION_PATTERNS = {
    "education": [
        r"(?i)\b(education|academic|qualification|degree|university|college|school)\b",
        r"(?i)\b(b\.?tech|m\.?tech|b\.?sc|m\.?sc|bca|mca|mba|phd|diploma)\b",
    ],
    "experience": [
        r"(?i)\b(experience|employment|work history|professional|internship|intern)\b",
        r"(?i)\b(work experience|professional experience|employment history)\b",
    ],
    "skills": [
        r"(?i)\b(skills?|technical skills?|competenc|technolog|proficien|expertise)\b",
        r"(?i)\b(programming languages?|tools?|frameworks?|stack)\b",
    ],
    "projects": [
        r"(?i)\b(projects?|personal projects?|academic projects?|portfolio)\b",
    ],
    "certifications": [
        r"(?i)\b(certification|certificate|certified|credential|license)\b",
    ],
    "summary": [
        r"(?i)\b(summary|objective|profile|about me|professional summary|career objective)\b",
    ],
    "achievements": [
        r"(?i)\b(achievement|award|honor|recognition|accomplishment)\b",
    ],
    "extracurricular": [
        r"(?i)\b(extracurricular|volunteer|community|leadership|activity|club)\b",
    ],
}


def _detect_sections(text: str) -> dict:
    """Detect which sections are present in the resume."""
    found = {}
    for section, patterns in SECTION_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text):
                found[section] = True
                break
        if section not in found:
            found[section] = False
    
    # Essential sections
    essential = ["education", "experience", "skills"]
    missing_essential = [s for s in essential if not found.get(s, False)]
    
    return {
        "found": found,
        "missing_essential": missing_essential,
        "completeness_score": sum(1 for v in found.values() if v) / len(found),
    }


# ── Action Verbs ───────────────────────────────────────────────────

STRONG_VERBS = [
    "achieved", "built", "created", "designed", "developed", "engineered",
    "established", "executed", "implemented", "improved", "increased",
    "initiated", "launched", "led", "managed", "optimized", "organized",
    "reduced", "resolved", "spearheaded", "streamlined", "transformed",
    "delivered", "deployed", "automated", "architected", "mentored",
    "orchestrated", "pioneered", "collaborated", "analyzed", "configured",
]

WEAK_VERBS = [
    "responsible for", "helped", "assisted", "worked on", "was part of",
    "duties included", "tasked with", "involved in", "participated in",
]


def _check_action_verbs(text: str) -> dict:
    """Check for strong vs weak action verbs."""
    text_lower = text.lower()
    
    strong_found = [v for v in STRONG_VERBS if v in text_lower]
    weak_found = [v for v in WEAK_VERBS if v in text_lower]
    
    return {
        "strong_verbs": strong_found,
        "strong_count": len(strong_found),
        "weak_verbs": weak_found,
        "weak_count": len(weak_found),
        "score": min(10, len(strong_found) - len(weak_found) + 5),
    }


# ── Quantification ─────────────────────────────────────────────────

def _check_quantification(text: str) -> dict:
    """Check if resume uses numbers, metrics, and quantifiable results."""
    
    # Patterns for numbers/metrics
    number_patterns = [
        r'\d+%',                    # percentages
        r'\$[\d,]+',                # dollar amounts
        r'₹[\d,]+',                 # rupee amounts
        r'\d+[kK]\+?',              # 10K, 5k+
        r'\d+x\b',                  # multipliers (3x, 10x)
        r'\d+\s*(users?|customers?|clients?|members?|people|students?)',
        r'increased.*\d+',          # "increased by 40%"
        r'reduced.*\d+',            # "reduced costs by 25%"
        r'improved.*\d+',           # "improved performance by 3x"
        r'grew.*\d+',               # "grew revenue by 50%"
    ]
    
    matches = []
    for pattern in number_patterns:
        found = re.findall(pattern, text, re.IGNORECASE)
        matches.extend(found)
    
    # Count bullet points
    bullets = re.findall(r'^\s*[-•●▪]\s', text, re.MULTILINE)
    
    return {
        "metrics_found": matches,
        "metric_count": len(matches),
        "bullet_count": len(bullets),
        "has_quantification": len(matches) > 0,
        "score": min(10, len(matches) + 3),
    }


# ── Contact Info ───────────────────────────────────────────────────

def _check_contact_info(text: str) -> dict:
    """Check for essential contact information."""
    
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'[\+]?[\d\s\-\(\)]{10,15}'
    linkedin_pattern = r'(?i)linkedin\.com/in/[\w\-]+'
    github_pattern = r'(?i)github\.com/[\w\-]+'
    
    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    linkedin = re.findall(linkedin_pattern, text)
    github = re.findall(github_pattern, text)
    
    missing = []
    if not emails:
        missing.append("email")
    if not phones:
        missing.append("phone number")
    if not linkedin:
        missing.append("LinkedIn profile")
    
    return {
        "has_email": len(emails) > 0,
        "has_phone": len(phones) > 0,
        "has_linkedin": len(linkedin) > 0,
        "has_github": len(github) > 0,
        "missing": missing,
        "score": 10 - len(missing) * 2,
    }


# ── Length Check ───────────────────────────────────────────────────

def _check_length(text: str) -> dict:
    """Check resume length and readability."""
    
    words = text.split()
    word_count = len(words)
    lines = text.split("\n")
    line_count = len([l for l in lines if l.strip()])
    
    # Ideal: 400-800 words for freshers, 600-1000 for experienced
    if word_count < 300:
        feedback = "Too short — expand your descriptions"
        score = 4
    elif word_count < 450:
        feedback = "Slightly short — add more detail to projects/experience"
        score = 6
    elif word_count <= 800:
        feedback = "Good length for a 1-2 page resume"
        score = 10
    elif word_count <= 1200:
        feedback = "Acceptable but consider trimming — recruiters scan quickly"
        score = 7
    else:
        feedback = "Too long — cut to 1-2 pages max"
        score = 4
    
    return {
        "word_count": word_count,
        "line_count": line_count,
        "feedback": feedback,
        "score": score,
    }


# ── Keyword Matching ───────────────────────────────────────────────

def _match_keywords(resume_text: str, job_text: str) -> dict:
    """Match resume keywords against job description."""
    
    if not job_text:
        return {
            "matched": [],
            "missing": [],
            "match_percentage": 0,
            "score": 5,  # neutral if no job description
            "note": "No job description provided — skipping keyword analysis",
        }
    
    # Extract keywords from job description (simple approach)
    # Filter for meaningful words (3+ chars, not common stop words)
    stop_words = {
        "the", "and", "for", "with", "this", "that", "from", "will", "have",
        "are", "was", "were", "been", "being", "can", "has", "had", "does",
        "did", "not", "but", "also", "you", "our", "any", "all", "may",
        "should", "would", "could", "must", "shall", "about", "into", "more",
        "other", "than", "its", "their", "your", "they", "them", "what",
    }
    
    job_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', job_text.lower()))
    job_keywords = job_words - stop_words
    
    resume_lower = resume_text.lower()
    matched = [kw for kw in job_keywords if kw in resume_lower]
    missing = [kw for kw in job_keywords if kw not in resume_lower]
    
    match_pct = (len(matched) / len(job_keywords) * 100) if job_keywords else 0
    
    return {
        "matched": matched[:20],  # Top 20
        "missing": sorted(missing)[:15],  # Top 15 missing
        "match_percentage": round(match_pct, 1),
        "score": min(10, int(match_pct / 10)),
    }


# ── Passive Voice Detection ────────────────────────────────────────

PASSIVE_PATTERNS = [
    r'\b(?:was|were|been|being|is|are|am)\s+\w+ed\b',
    r'\b(?:was|were|been|being|is|are|am)\s+\w+en\b',
    r'\bresponsible for\b',
    r'\bin charge of\b',
]


def _detect_passive_voice(text: str) -> dict:
    """Detect passive voice usage in resume."""
    
    matches = []
    for pattern in PASSIVE_PATTERNS:
        found = re.findall(pattern, text, re.IGNORECASE)
        matches.extend(found)
    
    return {
        "passive_phrases": matches[:10],
        "count": len(matches),
        "score": max(0, 10 - len(matches)),
    }


# ── Bullet Point Analysis ──────────────────────────────────────────

def _analyze_bullet_points(text: str) -> dict:
    """Analyze bullet point quality."""
    
    bullets = re.findall(r'^\s*[-•●▪]\s*(.+)', text, re.MULTILINE)
    
    if not bullets:
        return {
            "count": 0,
            "too_short": [],
            "good_examples": [],
            "score": 3,
            "feedback": "No bullet points found — use bullets for experience/projects",
        }
    
    too_short = [b for b in bullets if len(b.split()) < 5]
    good = [b for b in bullets if len(b.split()) >= 8 and any(c.isdigit() for c in b)]
    
    return {
        "count": len(bullets),
        "too_short": too_short[:5],
        "good_examples": good[:5],
        "short_count": len(too_short),
        "score": min(10, 10 - len(too_short)),
        "feedback": f"Found {len(bullets)} bullets, {len(too_short)} are too short (< 5 words)",
    }
