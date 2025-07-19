from q_learning import run_episode, Q
import json
from multiprocessing import Process, Manager
import multiprocessing as mp

def main():
    prozesse = []
    manager = Manager()
    shared_Q = manager.dict()

    # Q-Tabelle laden, falls vorhanden
    try:
        with open("q_learning_log.json", "r") as f:
            shared_Q.update(json.load(f))
    except FileNotFoundError:
        print("Keine Q-Tabelle gefunden. Starte Training...")
        pass
    
    # Anzahl der parallelen Prozesse
    for i in range(50):  # Anzahl der parallelen Prozesse
        p = Process(target=run_episode, args=(i, shared_Q,))
        prozesse.append(p)
        p.start()

    for p in prozesse:
        p.join()    
        
    # Q-Tabelle speichern
    with open("q_learning_log.json", "w") as f:
        json.dump({str(k): v for k, v in shared_Q.items()}, f, indent=4)

    print("Training abgeschlossen. Q-Tabelle gespeichert.")


if __name__ == "__main__":
    mp.set_start_method('spawn')
    max_processes = 10
    main()
    
  