import os
import random

def list_categories(path):
    return [category for category in os.listdir(path) if os.path.isdir(os.path.join(path, category))]

def list_quiz_files(path):
    return [file for file in os.listdir(path) if file.endswith(".txt")]

def quiz(filepath):
    questions = []
    try:
        with open(filpath, r, encoding="utf-8") as file:
            blocks = file.read().split("################")
            for block in blocks:
                line = block.strip()
                if len(line) < 6:
                    continue
                