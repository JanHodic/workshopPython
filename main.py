from home import home_screen
from game import run_game

def main():
    start = home_screen()
    if start:
        run_game()

if __name__ == "__main__":
    main()