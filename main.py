import argparse

import pandas as pd

from gpt import set_openai_api_key, interpret_question, format_answer
from query_engine import execute_query


def main():
    parser = argparse.ArgumentParser(
        description="Анализ статистики по естественным запросам"
    )
    parser.add_argument(
        "data_path",
        type=str,
        help="Путь к CSV-файлу с данными (например, data/freelancer_data.csv)"
    )
    parser.add_argument(
        "question",
        type=str,
        nargs="+",
        help="Вопрос на естественном языке (например: 'Какой средний доход у экспертов?')"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="Ключ API OpenAI (опционально, можно также задать через переменную окружения OPENAI_API_KEY)"
    )

    args = parser.parse_args()
    question = " ".join(args.question)

    try:
        set_openai_api_key(args.api_key)
    except ValueError as e:
        print(e)
        return

    try:
        df = pd.read_csv(args.data_path)
    except FileNotFoundError:
        print(f"Файл данных не найден: {args.data_path}")
        return

    try:
        instruction = interpret_question(question, df)
        result = execute_query(df, instruction)
        result = format_answer(result, question)
        print(f"\nОтвет:\n{result}")
    except Exception as e:
        print(f"Ошибка при обработке запроса: {e}")


if __name__ == "__main__":
    main()
