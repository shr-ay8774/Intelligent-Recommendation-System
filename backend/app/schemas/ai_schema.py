from pydantic import BaseModel


class AIRecommendationResponse(BaseModel):
    explanation: str


class AssistantRequest(BaseModel):
    question: str


class AssistantResponse(BaseModel):
    answer: str


class CourseExplanationResponse(BaseModel):
    course_id: int
    course_title: str
    explanation: str


class LearningPlanRequest(BaseModel):
    goal: str


class LearningPlanResponse(BaseModel):
    plan: str


class QuizRequest(BaseModel):
    topic: str
    number_of_questions: int = 5


class QuizQuestion(BaseModel):
    question: str
    options: list[str]
    answer: str


class QuizResponse(BaseModel):
    topic: str
    questions: list[QuizQuestion]