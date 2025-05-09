import os
import random

def list_categories(path):
    return [category for category in os.listdir(path) if os.path.isdir(os.path.join(path, category))]

def list_quiz_files(path):
    return [file for file in os.listdir(path) if file.endswith(".txt")]

def quiz(filepath):
    questions = []
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            blocks = file.read().split("################")
            for block in blocks:
                lines = block.strip()
                if len(lines) < 6:
                    continue
                question_text = lines[0].replace("Question: ")
                choices = {
                    line[0]: line[3:] for line in lines[1:5] if line[1] == ")"
                }
                correct_answer = lines[5].replace("Answer: ").strip().lower()
                questions.append({
                    "question": question_text,
                    "choices": choices,
                    "answer": correct_answer
                })
        return questions
    except Exception as error:
        print(f"Error loading quiz: {error}")
        return 
    
def run_quiz(questions):
    score = 0 
    random.shuffle(questions)
    