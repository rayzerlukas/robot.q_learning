from q_learning import run_play_episode, Q
import json
import pygame as pg

def main():
    # Q-Tabelle laden, falls vorhanden
    try:
        with open("q_learning_log.json", "r") as f:
            loaded = json.load(f)
            Q.update({eval(k): v for k, v in loaded.items()})
    except FileNotFoundError:
        print("Keine Q-Tabelle gefunden.")
        pg.quit()
        exit()

    run_play_episode()

if __name__ == "__main__":
    main()
    pg.quit()
