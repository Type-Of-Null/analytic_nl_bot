from llm.prompt_manager import DB_SCHEMA, PROMPT_TEMPLATE
import json
import requests

# --- Настройки Ollama ---
OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_TRANSLATOR = "phi3"
MODEL_SQL_GENERATOR = "llama3"


def call_ollama_api(model_name, prompt_text):
    payload = {"model": model_name, "prompt": prompt_text, "stream": False}
    response = requests.post(OLLAMA_API_URL, data=json.dumps(payload))
    response.raise_for_status()
    result = json.loads(response.text)
    return result["response"].strip()


def translate_to_english(russian_question):
    """Переводит русский вопрос в краткую английскую фразу."""
    prompt = f"""
    Translate the following Russian question into a concise English phrase. 
    Only provide the translation, nothing else.

    Russian: '{russian_question}'

    English:
    """
    return call_ollama_api(MODEL_TRANSLATOR, prompt)


def generate_sql_with_ollama(english_question):
    """Генерирует SQL из английского вопроса с использованием схемы."""

    database_schema = DB_SCHEMA

    prompt = f"""
    {PROMPT_TEMPLATE}

    Schema:
    {database_schema}

    Question:
    {english_question}

    """
    return call_ollama_api(MODEL_SQL_GENERATOR, prompt)


def format_sql(sql: str) -> str:
    if sql.startswith("```sql"):
        sql = sql[6:].strip()
    elif sql.startswith("```"):
        sql = sql[3:].strip()

    if sql.endswith("```"):
        sql = sql[:-3].strip()
        return sql
