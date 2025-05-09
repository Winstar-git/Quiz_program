import os
import random
import sys
import time
from rich.text import Text
from rich.console import Console
from rich.panel import Panel
from colorama import Fore, Style, init

init(autoreset=True)
console = Console()


ascii_art = """
 ██████╗ ██╗   ██╗██╗███████╗
██╔═══██╗██║   ██║██║╚══███╔╝
██║   ██║██║   ██║██║  ███╔╝ 
██║▄▄ ██║██║   ██║██║ ███╔╝  
╚██████╔╝╚██████╔╝██║███████╗
 ╚══▀▀═╝  ╚═════╝ ╚═╝╚══════╝"""

def typewriter(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def loading(message="Loading...", delay=2.5):
    with console.status(f"[bold green]{message}"):
        time.sleep(delay)

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
        print(Fore.RED + f"❌ Error loading quiz: {error}")
        return 
    
def run_quiz(questions):
    score = 0 
    random.shuffle(questions)
    for number, question in enumerate(questions, 1):
        question_text = f"[bold yellow]Question {number}:[/bold yellow] {question['question']}\n\n"
        for choice in sorted(question['choices']):
            question_text += f"[cyan]{choice})[/cyan] {question['choices'][choice]}\n"
        console.print(Panel.fit(Text.from_markup(question_text.strip()), border_style="bright_magenta"))

        user_answer = input(Fore.GREEN + "👉 Your answer (a/b/c/d): " + Style.RESET_ALL).lower()
        while user_answer not in ['a', 'b', 'c', 'd']:
            user_answer = input(Fore.RED + "❌ Invalid input. Enter a/b/c/d: " + Style.RESET_ALL).lower()

        if user_answer == question['answer']:
            score += 1
    
    console.print("\n[bold cyan]🏁 Quiz Complete![/bold cyan]")
    console.print(f"[bold green]🎯 Your Score: {score} / {len(questions)}[/bold green]")

console.print(Panel.fit(ascii_art, border_style="bright_red"))
loading("Loading Quiz Runner...")
typewriter("🧠 Ready to test your knowledge...\n")


base_directory = "Quizzes"
if not os.path.exists(base_directory):
    print(Fore.RED + "❌ No quizzes available. Make sure the 'Quizzes' folder exists.")
    exit()

categories = list_categories(base_directory)
if not  categories:
    print(Fore.RED + "❌ No quiz categories found.")
    exit()

print("\nAvailable Categories:")
for number, category in enumerate(categories, 1):
    print(Fore.YELLOW + f"{number}. {category}")

try:
    category_choice = int(input(Fore.CYAN + "\n🎯 Select a category by number: " + Style.RESET_ALL))
    selected_category = categories[category_choice - 1]
except (ValueError, IndexError):
    print(Fore.RED + "❌ Invalid selection.")
    exit()

category_directory = os.path.join(base_directory, selected_category)
quiz_files = list_quiz_files(category_directory)
if not quiz_files:
    print(Fore.RED + "❌ No quiz files found in this category.")
    exit()
    
console.print(f"\n[bold blue]📚 Available quizzes in '{selected_category}':[/bold blue]")
for number, quiz_file in enumerate(quiz_files, 1):
    print(Fore.GREEN + f"{number}. {quiz_file}")

try:
    quiz_choice = int(input(Fore.CYAN + "\n🗂️  Select a quiz file by number: " + Style.RESET_ALL))
    selected_quiz = quiz_files[quiz_choice - 1]
except (ValueError, IndexError):
    print(Fore.RED + "❌ Invalid selection.")
    exit()

quiz_file_path = os.path.join(category_directory, selected_quiz)
questions = quiz(quiz_file_path)
if questions:
    run_quiz(questions)
else:
    print(Fore.RED + "❌ No valid questions found.")
