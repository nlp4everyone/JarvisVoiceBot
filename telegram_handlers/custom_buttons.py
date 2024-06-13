from telethon.tl.custom.button import Button
import json, random
from config import voice_bot_params

# Get approved users
with open("./data/recommendation_questions.json",'r') as f:
    data = json.load(f)
all_questions = data["questions"]

def get_random_recommnedation_buttons():
    # Only get fixed number of recommendation to show
    # Shuffle the list
    random.shuffle(all_questions)
    chosen_question = random.choices(all_questions, k = voice_bot_params.recommendation_nums)

    buttons = []
    for (i,question) in enumerate(chosen_question):
        # Add question to buttons
        buttons.append([Button.inline(text = question, data = str(i+1).encode('UTF-8'))])
    return buttons


