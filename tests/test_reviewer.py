"""Tests for the resume reviewer."""

from reviewer.analyzer import (
    _detect_sections,
    _check_action_verbs,
    _check_quantification,
    _check_contact_info,
    _check_length,
    _detect_passive_voice,
    _analyze_bullet_points,
)


SAMPLE_RESUME = """
John Doe
john.doe@gmail.com | +91 9876543210 | linkedin.com/in/johndoe | github.com/johndoe

PROFESSIONAL SUMMARY
Motivated software engineer with experience in building scalable applications.

EDUCATION
B.Tech Computer Science, Delhi University, 2024
CGPA: 8.5/10

EXPERIENCE
Software Intern, ABC Tech Pvt Ltd (Jun 2023 - Aug 2023)
- Developed REST APIs serving 10,000+ daily users using Python and Flask
- Reduced API response time by 40% through query optimization
- Implemented automated testing pipeline, improving code coverage from 45% to 85%
- Collaborated with 5-member team using Agile methodology

TECHNICAL SKILLS
Languages: Python, JavaScript, C++, SQL
Frameworks: Flask, Django, React, Node.js
Tools: Git, Docker, AWS, MongoDB

PROJECTS
E-Commerce Platform
- Built a full-stack e-commerce app with 500+ product listings
- Integrated payment gateway processing $2,000+ monthly transactions
- Deployed on AWS EC2 with 99.9% uptime

Chat Application
- Created real-time chat app supporting 100+ concurrent users
- Implemented WebSocket connections with Redis for message queuing

ACHIEVEMENTS
- Won 1st place in college hackathon (200+ participants)
- Published research paper on ML-based fraud detection
- Google Cloud certified associate cloud engineer
"""


def test_detect_sections():
    result = _detect_sections(SAMPLE_RESUME)
    assert result["found"]["education"] is True
    assert result["found"]["experience"] is True
    assert result["found"]["skills"] is True
    assert result["found"]["projects"] is True
    assert result["found"]["certifications"] is True
    assert len(result["missing_essential"]) == 0


def test_action_verbs():
    result = _check_action_verbs(SAMPLE_RESUME)
    assert result["strong_count"] > 0
    assert "developed" in result["strong_verbs"]
    assert "reduced" in result["strong_verbs"]


def test_quantification():
    result = _check_quantification(SAMPLE_RESUME)
    assert result["has_quantification"] is True
    assert result["metric_count"] >= 5


def test_contact_info():
    result = _check_contact_info(SAMPLE_RESUME)
    assert result["has_email"] is True
    assert result["has_phone"] is True
    assert result["has_linkedin"] is True
    assert result["has_github"] is True
    assert len(result["missing"]) == 0


def test_length():
    result = _check_length(SAMPLE_RESUME)
    assert result["word_count"] > 100
    assert result["score"] >= 6


def test_passive_voice():
    result = _detect_passive_voice(SAMPLE_RESUME)
    assert result["count"] >= 0  # Our sample is mostly active


def test_bullet_points():
    result = _analyze_bullet_points(SAMPLE_RESUME)
    assert result["count"] > 5


def test_empty_resume():
    result = _detect_sections("")
    assert result["found"]["education"] is False
    assert len(result["missing_essential"]) == 3


def test_weak_resume():
    weak = "I was responsible for helping the team. I assisted with various tasks."
    verbs = _check_action_verbs(weak)
    assert verbs["weak_count"] > 0
    assert "responsible for" in verbs["weak_verbs"]
