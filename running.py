import subprocess
import threading

def execute_script(script_path):

    try:
        print(f"Exécution de {script_path}...")
        result = subprocess.run(["python3", script_path], check=True, text=True, capture_output=True)
        print(f"Sortie de {script_path} :\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de {script_path} :\n{e.stderr}")
    except FileNotFoundError:
        print(f"Le fichier {script_path} est introuvable.")

def main():

    scripts_to_run_first = ["./Algorithm/static.py", "./Algorithm/load_balancing.py","./Algorithm/adaptatif.py"]  # Liste des scripts à exécuter en premier
    final_script = "./comparaison-protocol.py"  # Script à exécuter après les autres
    animation_script = "./Animations/static.py"

    # Exécution des scripts initiaux
    for script in scripts_to_run_first:
        execute_script(script)



    # Création des threads
    final_thread = threading.Thread(target=execute_script, args=(final_script,))
    animation_thread = threading.Thread(target=execute_script, args=(animation_script,))

    # Démarrage des threads
    print("\nTous les scripts précédents sont terminés. Exécution du script final.")
    final_thread.start()
    
    print("\nAnimation:")
    animation_thread.start()

    # Attente de la fin des threads
    final_thread.join()
    animation_thread.join()


if __name__ == "__main__":
    main()
