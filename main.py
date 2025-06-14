from home import home_screen
from game import run_game

def main():
    result = home_screen()
    if result == "start":
        run_game()
    elif result == "settings":
        print("Zde můžeš otevřít nastavení…")

if __name__ == "__main__":
    main()