from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_PATH = "./my_t5_sql_model"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH)


def translate_to_sql_select(english_query):
    input_text = english_query
    input_ids = tokenizer.encode(input_text, return_tensors="pt")
    outputs = model.generate(input_ids)
    sql_query = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return sql_query


# Example usage
english_query = "Show all employees with salary greater than $50000"
sql_query = translate_to_sql_select(english_query)
print("SQL Query:", sql_query)
