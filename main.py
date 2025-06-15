from home import home_screen
from game import run_game

def main():
    while True:
        action, difficulty = home_screen()
        if action == "start":
            run_game(difficulty)
        elif action == "exit":
            break  # nebo sys.exit()

if __name__ == "__main__":
    main()