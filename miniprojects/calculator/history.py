def save_history(expression, result, filename="history.txt"):
    with open(filename, "a") as f:
        f.write(f"{expression} = {result}\n")

def show_history(filename="history.txt"):
    with open(filename, "r") as f:
        return f.read()
