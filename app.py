from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Fonction pour lire les tâches depuis le fichier taches.txt
def lire_taches():
    taches = []
    try:
        with open('taches.txt', 'r', encoding='utf-8') as f:  # Forcer l'encodage UTF-8
            for ligne in f:
                nom, description, statut, priorite = ligne.strip().split('|')
                taches.append((nom, description, statut, priorite))
    except FileNotFoundError:
        pass
    return taches

# Fonction pour écrire les tâches dans taches.txt
def ecrire_taches(taches):
    with open('taches.txt', 'w') as f:
        for tache in taches:
            f.write(f"{tache[0]}|{tache[1]}|{tache[2]}|{tache[3]}\n")

@app.route('/')
def index():
    tasks = lire_taches()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    nom_tache = request.form['task_name']
    desc_tache = request.form['task_desc']
    statut_tache = request.form['task_status']
    priorite_tache = request.form['task_priority']
    
    taches = lire_taches()
    taches.append((nom_tache, desc_tache, statut_tache, priorite_tache))
    ecrire_taches(taches)
    
    return redirect('/')

@app.route('/delete_task', methods=['POST'])
def delete_task():
    nom_tache = request.form['task_name']
    taches = lire_taches()
    taches = [t for t in taches if t[0] != nom_tache]
    ecrire_taches(taches)
    return redirect('/')

@app.route('/complete_task', methods=['POST'])
def complete_task():
    nom_tache = request.form['task_name']
    taches = lire_taches()
    taches = [(t[0], t[1], 'Complétée', t[3]) if t[0] == nom_tache else t for t in taches]
    ecrire_taches(taches)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
