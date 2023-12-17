def is_yes_prompt(msg):
    user_answer = input(msg)
    return user_answer.lower() in ["yes", "y"]
