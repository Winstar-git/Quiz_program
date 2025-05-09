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
                lines = block.strip().split("\n")
                if len(lines) < 6:
                    continue
                question_text = lines[0].replace("Question: ", "")
                choices = {
                    line[0]: line[3:] for line in lines[1:5] if line[1] == ")"
                }
                correct_answer = lines[5].replace("Answer: ", "").strip().lower()
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
    for number, question in enumerate(questions, 1):
        print(f"\nQuestion {number}: {question['question']}")
        for choice in sorted(question['choices']):
            print(f"{choice} {question['choices'][choice]}")

        user_answer = input("Your answer (a/b/c/d): ").lower()
        while user_answer not in ['a', 'b', 'c', 'd']:
            user_answer = input("Invalid input. Enter a/b/c/d: ").lower()

        if user_answer == question['answer']:
            score += 1
    
    print("\nQuiz Complete!!")
    print(f"Your Score : {score} / {len(questions)}")

base_directory = "Quizzes"
if not os.path.exists(base_directory):
    print("No quizzes available. Make sure the 'Quizzes' foler exist.")
    exit()

categories = list_categories(base_directory)
if not  categories:
    print("No quiz categories found.")
    exit()

print("\nAvailable Categories:")
for number, category in enumerate(categories, 1):
    print(f"{number}. {category}")

try:
    category_choice = int(input("\nSelect a category by number: "))
    selected_category = categories[category_choice - 1]
except (ValueError, IndexError):
    print("Invalid selection.")
    exit()

category_directory = os.path.join(base_directory, selected_category)
quiz_files = list_quiz_files(category_directory)
if not quiz_files:
    print("No quiz files found in this category.")
    exit()
    
print(f"Available quizzes in '{selected_category}':")
for number, quiz_file in enumerate(quiz_files, 1):
    print(f"{number}. {quiz_file}")

try:
    quiz_choice = int(input("\nSelect a quiz file by number: "))
    selected_quiz = quiz_files[quiz_choice - 1]
except (ValueError, IndexError):
    print("Invalid selection.")
    exit()

quiz_file_path = os.path.join(category_directory, selected_quiz)
questions = quiz(quiz_file_path)
if questions:
    run_quiz(questions)
else:
    print("No valid questions found")