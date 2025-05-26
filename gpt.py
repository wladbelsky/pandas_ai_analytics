import os

import openai
import pandas as pd

MODEL = "gpt-4o-mini"


def set_openai_api_key(cli_key=None):
    """
    Устанавливает ключ API OpenAI из аргумента CLI или переменной окружения.
    """
    openai.api_key = cli_key or os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OpenAI API ключ не найден. Укажите его через CLI или переменную окружения.")


def interpret_question(question: str, df: pd.DataFrame) -> str:
    """
    Преобразует естественный вопрос в SQL-подобную инструкцию, используя схему таблицы и пример данных.
    """
    # Получение схемы таблицы
    schema = ", ".join([f"{col} ({dtype})" for col, dtype in zip(df.columns, df.dtypes)])

    # Получение одного примера данных
    example = df.iloc[0].to_dict()

    system_prompt = (
        "Ты аналитик данных. Получишь текстовый вопрос, схему таблицы и пример данных. "
        "Верни только SQL-подобный запрос к таблице с названием 'data'. Не добавляй пояснений и форматирование."
    )

    prompt = (
        f"Схема таблицы:\n{schema}\n\n"
        f"Пример данных:\n{example}\n\n"
        f"Вопрос:\n{question}"
    )

    response = openai.chat.completions.create(
        model=MODEL,
        messages=(
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ),
        temperature=0.2
    )

    return response.choices[0].message.content.strip()


def format_answer(raw_result, original_question: str) -> str:
    """
    Принимает результат SQL-запроса (строку или DataFrame) и исходный вопрос,
    возвращает человекочитаемый ответ.
    """
    if isinstance(raw_result, pd.DataFrame):
        result_text = raw_result.to_csv(index=False)
    else:
        result_text = str(raw_result)

    prompt = (
        "Ты должен красиво оформить аналитический вывод на основе результата анализа данных.\n\n"
        f"Вопрос пользователя:\n{original_question}\n\n"
        f"Результат запроса:\n{result_text}\n\n"
        "Ответь кратко и понятно на русском языке."
    )

    response = openai.chat.completions.create(
        model=MODEL,
        messages=(
            {"role": "system", "content": "Ты аналитик, умеющий понятно объяснять результаты анализа."},
            {"role": "user", "content": prompt}
        ),
        temperature=0.4
    )

    return response.choices[0].message.content.strip()
