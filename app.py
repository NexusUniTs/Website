from flask import Flask, render_template

app = Flask(__name__)

# Database fittizio dei progetti
PROJECTS_DB = {
    '1': {
        'id': '1',
        'title': 'BALL BALANCING BOT',
        'short_desc': "Robot sferico omidirezionale in grado di mantenere l'equilibrio dinamico perfetto su una singola sfera. Utilizza filtri di Kalman integrati con IMU ad alta frequenza.",
        'long_desc': "Il Ball Balancing Bot rappresenta l'avanguardia della teoria dei controlli automatizzati. Sfruttando 3 ruote omnidirezionali posizionate a 120 gradi, è capace di muoversi agilmente in ogni direzione bilanciandosi su una sfera. L'inversione cinematica e la reattività dei motori garantiscono movimenti ipnotici.",
        'status': 'CALIBRATING...',
        'status_color': 'cyan'
    },
    '2': {
        'id': '2',
        'title': 'LINE FOLLOWING BOT',
        'short_desc': "Il nostro primo progetto storico. Un robottino basato su Arduino con un array di sensori infrarossi frontali per seguire una linea nera.",
        'long_desc': "Questo line follower è stato il primo vero progetto del team. Costruito internamente utilizzando una scheda Arduino e un array di sensori IR frontali, ci ha permesso di imparare le basi dell'elettronica e del controllo PID per fargli seguire un percorso nero su fondo bianco in modo fluido.",
        'status': 'COMPLETED',
        'status_color': 'yellow'
    },
    '3': {
        'id': '3',
        'title': 'ROBOTIC ARM',
        'short_desc': "Braccio manipolatore a 6 gradi di libertà stampato in 3D con leghe leggere, motori stepper di precisione zero-backlash e cinematica inversa per computer vision.",
        'long_desc': "Questo braccio robotico a 6 DOF è ingegnerizzato tramite complessi calcoli matriciali. Integra un sistema modulare per scambiare strumenti. Grazie ad una telecamera collegata all'IA, possiede percezione ambientale nativa.",
        'status': 'ONLINE',
        'status_color': 'magenta'
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/project/<project_id>')
def project_detail(project_id):
    project = PROJECTS_DB.get(project_id)
    if not project:
        return "Progetto non trovato", 404
    return render_template('project.html', project=project)

if __name__ == '__main__':
    app.run(debug=False, port=5000)