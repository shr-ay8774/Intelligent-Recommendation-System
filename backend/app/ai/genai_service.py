import os

from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables from .env
load_dotenv()


# Get OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")


# Create OpenAI client only if API key exists
client = None

if api_key:
    client = OpenAI(
        api_key=api_key
    )


def generate_local_explanation(
    user_name: str,
    skill_level: str,
    interests: str,
    recommendations: list
):
    """
    Generate a local explanation without using OpenAI.
    """

    if not recommendations:
        return (
            "There are currently no new course recommendations "
            "available for you."
        )

    course_names = [
        course["title"]
        for course in recommendations
    ]

    courses_text = ", ".join(course_names)

    explanation = (
        f"{user_name}, based on your "
        f"{skill_level.lower() if skill_level else 'current'} "
        f"skill level and your interest in "
        f"{interests if interests else 'your selected topics'}, "
        f"we recommend the following courses: "
        f"{courses_text}. "
        f"These recommendations are based on your profile "
        f"and learning activity."
    )

    return explanation


def explain_recommendations(
    user_name: str,
    skill_level: str,
    interests: str,
    recommendations: list
):
    """
    Generate an AI explanation.

    If OpenAI is unavailable or has no quota,
    use the local fallback.
    """

    # Local fallback
    fallback = generate_local_explanation(
        user_name=user_name,
        skill_level=skill_level,
        interests=interests,
        recommendations=recommendations
    )

    # No OpenAI API key
    if client is None:
        return fallback

    courses_text = "\n".join(
        [
            f"- {course['title']} "
            f"(score: {course['score']:.2f})"
            for course in recommendations
        ]
    )

    prompt = f"""
You are an AI learning assistant.

User:
Name: {user_name}
Skill level: {skill_level}
Interests: {interests}

Recommended courses:
{courses_text}

Explain why these courses may be useful for this user.

Keep the explanation concise and beginner-friendly.

Do not invent information about the courses.
Only use the information provided.
"""

    try:
        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        return response.output_text

    except Exception:
        # OpenAI unavailable / quota exhausted
        return fallback


def generate_local_assistant_response(
    user_name: str,
    skill_level: str,
    interests: str,
    question: str,
    recommendations: list
):
    """
    Generate a local learning assistant response
    without using OpenAI.
    """

    question_lower = question.lower()

    # --------------------------------
    # Python-related questions
    # --------------------------------

    if "python" in question_lower:

        return (
            f"{user_name}, since your interests include "
            f"{interests or 'Python'}, start with Python fundamentals. "
            "Focus on variables, data types, conditions, loops, "
            "functions, lists, dictionaries, and object-oriented "
            "programming. After that, move toward the Python courses "
            "recommended by the system."
        )

    # --------------------------------
    # Recommendation-related questions
    # --------------------------------

    if (
        "recommend" in question_lower
        or "course" in question_lower
        or "learn next" in question_lower
    ):

        if recommendations:

            course_names = [
                course["title"]
                for course in recommendations
            ]

            courses_text = ", ".join(course_names)

            return (
                f"Based on your profile and learning activity, "
                f"I recommend starting with: {courses_text}."
            )

        return (
            "There are currently no new course recommendations "
            "available. Try adding more interests or learning "
            "activity."
        )

    # --------------------------------
    # Learning-plan questions
    # --------------------------------

    if (
        "plan" in question_lower
        or "roadmap" in question_lower
        or "path" in question_lower
    ):

        return (
            "Start with fundamentals, then practice with small "
            "projects, followed by intermediate topics and a "
            "larger project. Your exact learning path can be "
            "refined using your course progress and interests."
        )

    # --------------------------------
    # Generic fallback
    # --------------------------------

    return (
        f"Your current skill level is "
        f"{skill_level or 'not specified'} and your interests "
        f"include {interests or 'not specified'}. "
        "Try asking me what to learn next, how to learn Python, "
        "or which course you should take."
    )
    
def generate_local_course_explanation(
    user_name: str,
    skill_level: str,
    interests: str,
    course_title: str,
    course_description: str
):

    return (
        f"{user_name}, the course '{course_title}' "
        f"may be useful for you because it matches your "
        f"current interests and learning profile. "
        f"Your current skill level is "
        f"{skill_level or 'not specified'}, and your interests "
        f"include {interests or 'not specified'}."
    )
    
def generate_local_learning_plan(
    user_name: str,
    skill_level: str,
    interests: str,
    goal: str,
    recommendations: list
):
    course_names = [
        course["title"]
        for course in recommendations
    ]

    if course_names:
        courses_text = ", ".join(course_names)
    else:
        courses_text = "the available courses"

    return (
        f"{user_name}, your learning plan for "
        f"{goal} is:\n\n"
        f"1. Start with the fundamentals of "
        f"{interests or 'your selected subject'}.\n"
        f"2. Complete the foundational courses.\n"
        f"3. Practice what you learn with small projects.\n"
        f"4. Move to intermediate concepts.\n"
        f"5. Build a practical project related to your goal.\n"
        f"6. Review your weak areas using your learning progress.\n\n"
        f"Based on your profile, consider these courses next: "
        f"{courses_text}."
    )
    
def generate_local_quiz(
    topic: str,
    number_of_questions: int
):
    quiz_bank = {
        "python": [
            {
                "question": "Which keyword is used to define a function in Python?",
                "options": [
                    "function",
                    "def",
                    "func",
                    "define"
                ],
                "answer": "def"
            },
            {
                "question": "Which data type stores True or False?",
                "options": [
                    "String",
                    "Integer",
                    "Boolean",
                    "List"
                ],
                "answer": "Boolean"
            },
            {
                "question": "Which symbol is used for comments in Python?",
                "options": [
                    "//",
                    "/*",
                    "#",
                    "--"
                ],
                "answer": "#"
            },
            {
                "question": "Which function is used to display output?",
                "options": [
                    "display()",
                    "echo()",
                    "print()",
                    "output()"
                ],
                "answer": "print()"
            },
            {
                "question": "Which collection is ordered and mutable?",
                "options": [
                    "Tuple",
                    "List",
                    "Set",
                    "FrozenSet"
                ],
                "answer": "List"
            }
        ],

        "javascript": [
            {
                "question": "Which keyword declares a block-scoped variable?",
                "options": [
                    "var",
                    "let",
                    "define",
                    "variable"
                ],
                "answer": "let"
            },
            {
                "question": "Which method converts JSON text into a JavaScript object?",
                "options": [
                    "JSON.parse()",
                    "JSON.object()",
                    "JSON.convert()",
                    "JSON.toObject()"
                ],
                "answer": "JSON.parse()"
            }
        ]
    }

    topic_key = topic.lower().strip()

    questions = quiz_bank.get(
        topic_key,
        []
    )

    if not questions:
        return []

    return questions[:number_of_questions]