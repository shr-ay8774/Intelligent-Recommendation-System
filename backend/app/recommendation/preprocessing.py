import pandas as pd


def prepare_courses(courses):

    data = []

    for course in courses:

        data.append({
            "id": course.id,
            "title": course.title,
            "description": course.description or "",
            "category_id": course.category_id
        })

    return pd.DataFrame(data)