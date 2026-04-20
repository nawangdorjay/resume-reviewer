"""
Report Generator — Format analysis results for display.
"""

import json


def print_report(scores: dict, analysis: dict) -> None:
    """Print a beautiful text report to terminal."""
    
    overall = scores["overall"]
    
    # Grade emoji
    if overall >= 80:
        grade = "🟢 Excellent"
    elif overall >= 65:
        grade = "🟡 Good"
    elif overall >= 50:
        grade = "🟠 Needs Work"
    else:
        grade = "🔴 Needs Major Improvement"
    
    print()
    print("═" * 51)
    print("  📄 RESUME REVIEW REPORT")
    print("═" * 51)
    print()
    print(f"  Overall Score: {overall}/100 — {grade}")
    print()
    
    # Category table
    print("  ┌──────────────────────────────┬───────┬────────┐")
    print("  │ Category                     │ Score │ Weight │")
    print("  ├──────────────────────────────┼───────┼────────┤")
    
    for name, data in scores["categories"].items():
        score = data["score"]
        weight = "★" * int(data["weight"])
        bar = "█" * score + "░" * (10 - score)
        print(f"  │ {name:<28} │ {score:>2}/10 │ {weight:<6} │")
    
    print("  └──────────────────────────────┴───────┴────────┘")
    print()
    
    # Strengths
    if scores["strengths"]:
        print("  ✅ STRENGTHS")
        for s in scores["strengths"]:
            print(f"  • {s}")
        print()
    
    # Improvements
    if scores["improvements"]:
        print("  ⚠️  IMPROVEMENTS NEEDED")
        for imp in scores["improvements"]:
            print(f"  • {imp}")
        print()
    
    # Quick stats
    quant = analysis["quantification"]
    contact = analysis["contact_info"]
    length = analysis["length"]
    
    print("  📊 QUICK STATS")
    print(f"  • Words: {length['word_count']}")
    print(f"  • Metrics found: {quant['metric_count']}")
    print(f"  • Bullet points: {analysis['bullet_points']['count']}")
    print(f"  • Strong verbs: {analysis['action_verbs']['strong_count']}")
    
    if contact["missing"]:
        print(f"  • ⚠️ Missing contact: {', '.join(contact['missing'])}")
    else:
        print(f"  • Contact info: Complete ✅")
    
    # Keyword match (if job description provided)
    keywords = analysis["keywords"]
    if not keywords.get("note"):
        print(f"  • Keyword match: {keywords['match_percentage']}%")
        if keywords["missing"]:
            print(f"  • Missing keywords: {', '.join(keywords['missing'][:8])}")
    
    print()
    print("═" * 51)
    print()


def json_report(scores: dict, analysis: dict) -> str:
    """Generate JSON report."""
    
    report = {
        "overall_score": scores["overall"],
        "categories": {
            name: {
                "score": data["score"],
                "max": data["max"],
                "detail": data["detail"],
            }
            for name, data in scores["categories"].items()
        },
        "strengths": scores["strengths"],
        "improvements": scores["improvements"],
        "stats": {
            "word_count": analysis["length"]["word_count"],
            "metric_count": analysis["quantification"]["metric_count"],
            "bullet_count": analysis["bullet_points"]["count"],
            "strong_verbs": analysis["action_verbs"]["strong_count"],
            "weak_verbs": analysis["action_verbs"]["weak_count"],
            "keyword_match": analysis["keywords"]["match_percentage"],
            "missing_keywords": analysis["keywords"]["missing"][:10],
            "missing_contact": analysis["contact_info"]["missing"],
        },
    }
    
    return json.dumps(report, indent=2)
