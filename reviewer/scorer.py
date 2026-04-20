"""
Resume Scorer — Calculate scores from analysis results.
"""


def score_resume(analysis: dict) -> dict:
    """Calculate category-wise and overall scores from analysis results."""
    
    categories = {}
    
    # Section Completeness (0-10)
    sections = analysis["sections"]
    categories["Section Completeness"] = {
        "score": round(sections["completeness_score"] * 10),
        "max": 10,
        "weight": 1.5,
        "detail": _section_detail(sections),
    }
    
    # Content Quality (0-10)
    action = analysis["action_verbs"]
    passive = analysis["passive_voice"]
    content_score = round((action["score"] + passive["score"]) / 2)
    categories["Content Quality"] = {
        "score": content_score,
        "max": 10,
        "weight": 1.5,
        "detail": _content_detail(action, passive),
    }
    
    # Keyword Optimization (0-10)
    keywords = analysis["keywords"]
    categories["Keyword Optimization"] = {
        "score": keywords["score"],
        "max": 10,
        "weight": 1.0,
        "detail": _keyword_detail(keywords),
    }
    
    # Quantification (0-10)
    quant = analysis["quantification"]
    categories["Quantification & Metrics"] = {
        "score": quant["score"],
        "max": 10,
        "weight": 1.5,
        "detail": _quant_detail(quant),
    }
    
    # Length & Readability (0-10)
    length = analysis["length"]
    categories["Length & Readability"] = {
        "score": length["score"],
        "max": 10,
        "weight": 1.0,
        "detail": length["feedback"],
    }
    
    # Contact Info (0-10)
    contact = analysis["contact_info"]
    categories["Contact Information"] = {
        "score": contact["score"],
        "max": 10,
        "weight": 1.0,
        "detail": _contact_detail(contact),
    }
    
    # Bullet Points (0-10)
    bullets = analysis["bullet_points"]
    categories["Bullet Point Quality"] = {
        "score": bullets["score"],
        "max": 10,
        "weight": 1.0,
        "detail": bullets.get("feedback", ""),
    }
    
    # Calculate weighted overall
    total_weighted = sum(c["score"] * c["weight"] for c in categories.values())
    total_weight = sum(c["weight"] for c in categories.values())
    overall = round(total_weighted / total_weight * 10)  # Convert to 0-100
    
    # Generate strengths and improvements
    strengths = _find_strengths(categories, analysis)
    improvements = _find_improvements(categories, analysis)
    
    return {
        "overall": min(100, overall),
        "categories": categories,
        "strengths": strengths,
        "improvements": improvements,
    }


def _section_detail(sections: dict) -> str:
    missing = sections["missing_essential"]
    if not missing:
        return "All essential sections present ✅"
    return f"Missing: {', '.join(missing)}"


def _content_detail(action: dict, passive: dict) -> str:
    parts = []
    if action["strong_count"] >= 5:
        parts.append(f"Strong action verbs: {action['strong_count']} found ✅")
    elif action["strong_count"] > 0:
        parts.append(f"Action verbs: {action['strong_count']} (aim for 5+)")
    
    if passive["count"] > 3:
        parts.append(f"Passive voice detected {passive['count']} times — use active voice")
    
    if action["weak_count"] > 0:
        parts.append(f"Weak phrases: {', '.join(action['weak_verbs'][:3])}")
    
    return "; ".join(parts) if parts else "Needs more strong action verbs"


def _keyword_detail(keywords: dict) -> str:
    if keywords.get("note"):
        return keywords["note"]
    return f"Match: {keywords['match_percentage']}% — {len(keywords['matched'])} matched, {len(keywords['missing'])} missing"


def _quant_detail(quant: dict) -> str:
    if quant["metric_count"] == 0:
        return "No metrics found — add numbers to your achievements (%, $, x)"
    return f"{quant['metric_count']} metrics found"


def _contact_detail(contact: dict) -> str:
    if not contact["missing"]:
        return "All contact info present ✅"
    return f"Missing: {', '.join(contact['missing'])}"


def _find_strengths(categories: dict, analysis: dict) -> list:
    """Identify resume strengths."""
    strengths = []
    
    for name, data in categories.items():
        if data["score"] >= 8:
            strengths.append(f"{name}: {data['detail']}")
    
    if analysis["quantification"]["metric_count"] >= 5:
        strengths.append("Good use of metrics and quantifiable results")
    
    if analysis["action_verbs"]["strong_count"] >= 8:
        strengths.append("Excellent use of strong action verbs")
    
    return strengths[:5]


def _find_improvements(categories: dict, analysis: dict) -> list:
    """Identify areas for improvement."""
    improvements = []
    
    for name, data in categories.items():
        if data["score"] < 6:
            improvements.append(f"{name}: {data['detail']}")
    
    if analysis["quantification"]["metric_count"] < 3:
        improvements.append("Add metrics to bullet points (e.g., 'improved X by 40%')")
    
    if analysis["action_verbs"]["weak_count"] > 2:
        weak = analysis["action_verbs"]["weak_verbs"][:3]
        improvements.append(f"Replace weak phrases: {', '.join(weak)}")
    
    if analysis["bullet_points"].get("short_count", 0) > 2:
        improvements.append("Some bullet points are too short — expand with detail and results")
    
    return improvements[:5]
