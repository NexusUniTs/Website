from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'nexus.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class TeamMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    persona = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(200), nullable=True)
    department = db.Column(db.String(100), nullable=True)
    order_num = db.Column(db.Integer, default=0)
    manager_id = db.Column(db.Integer, db.ForeignKey('team_member.id'), nullable=True)
    subordinates = db.relationship('TeamMember', backref=db.backref('manager', remote_side=[id]))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    short_desc = db.Column(db.Text, nullable=False)
    long_desc = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50))
    status_color = db.Column(db.String(50))
    order_num = db.Column(db.Integer, default=0)
    image_paths = db.Column(db.Text, nullable=True)
    video_url = db.Column(db.String(300), nullable=True)
    specs = db.Column(db.Text, nullable=True)

with app.app_context():
    db.create_all()
    if not TeamMember.query.first():
        # 1. Reparto Informatica
        denis = TeamMember(
            name="Denis Trokan",
            role="Capo Reparto Informatica",
            department="REPARTO INFORMATICA",
            order_num=1
        )
        # 2. Reparto Design e Struttura
        alessio = TeamMember(
            name="Alessio Tessaris",
            role="Capo Reparto & Direttore Tecnico",
            department="REPARTO DESIGN E STRUTTURA",
            order_num=2
        )
        # 3. Reparto Elettronica
        martina = TeamMember(
            name="Martina Anese",
            role="Capa Reparto & Direttrice Tecnica",
            department="REPARTO ELETTRONICA",
            order_num=3
        )
        # 4. Reparto Marketing
        pietro = TeamMember(
            name="Pietro Dean",
            role="Presidente & Capo Reparto Marketing",
            department="REPARTO MARKETING",
            order_num=4
        )
        db.session.add_all([denis, alessio, martina, pietro])
        db.session.commit()
        
        # Membri Reparto Informatica
        elia = TeamMember(name="Elia Covi", role="Membro Reparto", manager_id=denis.id)
        daniele_d = TeamMember(name="Daniele Deiana", role="Membro Reparto", manager_id=denis.id)
        raoul = TeamMember(name="Raoul Merotto", role="Membro Reparto", manager_id=denis.id)
        martucci = TeamMember(name="Alessio Martucci", role="Membro Reparto", manager_id=denis.id)
        
        # Membri Reparto Design e Struttura
        enrico = TeamMember(name="Enrico Deiana", role="Membro Reparto", manager_id=alessio.id)
        luca = TeamMember(name="Luca Dencic", role="Membro Reparto", manager_id=alessio.id)
        daniele_t = TeamMember(name="Daniele Tessaris", role="Membro Reparto", manager_id=alessio.id)
        
        db.session.add_all([elia, daniele_d, raoul, martucci, enrico, luca, daniele_t])
        db.session.commit()
        
    if not Project.query.first():
        p1 = Project(
            title='LINE FOLLOWING BOT',
            short_desc="Robot autonomo basato su sensori IR e motori indipendenti per tracciare percorsi. Correzione dinamica della traiettoria in tempo reale.",
            long_desc="Il robot è progettato per seguire autonomamente un percorso tracciato da una linea nera su sfondo bianco (o viceversa). Utilizza una serie di sensori a infrarossi (IR) posti sulla parte anteriore per rilevare il contrasto. La logica di controllo riceve i segnali dai sensori e corregge la traiettoria modulando la velocità dei due motori indipendenti per mantenere la linea al centro del robot.",
            status='COMPLETED',
            status_color='yellow',
            order_num=1,
            image_paths="line_following/img1.jpg,line_following/img2.png",
            video_url="/static/images/projects/line_following/Working_line_bot.mp4",
            specs="MICROCONTROLLORE:Arduino Uno|POWER:12V Li-Ion|SENSORI:Array IR"
        )
        p2 = Project(
            title='BALL BALANCING BOT',
            short_desc="Sistema di feedback a ciclo chiuso in tempo reale per stabilizzare dinamicamente una sfera su una Stewart Platform tramite PID.",
            long_desc="Un progetto di robotica avanzata progettato per dimostrare l'efficacia dei sistemi di feedback a ciclo chiuso in tempo reale. L'obiettivo del sistema è stabilizzare dinamicamente una sfera al centro di una piattaforma mobile (Stewart Platform).<br><br><strong>Componenti e Tecnologie Chiave:</strong><br>• <strong>Sensore (Input):</strong> Un pannello touchscreen resistivo legge la posizione esatta della pallina sull'asse X e Y.<br>• <strong>Elaborazione (Core):</strong> Un Raspberry Pi elabora i dati grezzi e utilizza due algoritmi PID separati per calcolare l'errore di posizionamento.<br>• <strong>Cinematica Inversa:</strong> Il software traduce matematicamente la correzione del PID nell'altezza esatta (Z) che ciascuno dei tre snodi deve raggiungere.<br>• <strong>Attuazione (Output):</strong> Un controller PWM (PCA9685) via I2C muove 3 servomotori ad alta velocità per inclinare il piano e annullare l'inerzia della sfera.<br><br>Un'applicazione pratica che unisce programmazione Python, calcolo matematico e calibrazione hardware.",
            status='IN PROGRESS',
            status_color='cyan',
            order_num=2,
            image_paths="ball_balancing/img1.jpg,ball_balancing/img2.jpg,ball_balancing/img3.jpg",
            video_url="",
            specs="INPUT:Touchscreen Resistivo|CORE:Raspberry Pi (PID)|KINEMATICS:Cinematica Inversa|OUTPUT:PWM I2C e 3 Servomotori"
        )
        p3 = Project(
            title='ROBOTIC ARM (PROTO V1)',
            short_desc="Prototipo di braccio robotico telecomandato via Wi-Fi. Realizzato per far testare la logica di controllo al reparto informatica mentre si progetta la versione finale.",
            long_desc="Questo braccio robotico è attualmente nella sua primissima fase di prototipazione (ispirato a piattaforme open-source come LeRobot SO-100). L'obiettivo di questa build iniziale è avere una base hardware pronta all'uso, permettendo al reparto informatica di iniziare a sviluppare il codice parallelamente alla progettazione 3D della versione finale.<br><br><strong>Direzione Tecnica Attuale:</strong><br>• <strong>Elaborazione (Core):</strong> Scheda con connettività Wi-Fi (es. Raspberry Pi 3B / MCU compatibili) per una gestione wireless.<br>• <strong>Interfaccia (Input):</strong> Pilotaggio remoto tramite 'Mini-me controller' e controlli analogici fisici (joystick) per movimenti fluidi.<br>• <strong>Meccanica (Output):</strong> Struttura base stampata in 3D azionata da un kit di servomotori standard.<br><br>Un perfetto esempio di sviluppo parallelo hardware/software: non si aspetta la meccanica perfetta per iniziare a programmare l'intelligenza del braccio.",
            status='IN PROGRESS',
            status_color='magenta',
            order_num=3,
            image_paths="",
            video_url="",
            specs="CORE:Modulo Wi-Fi (Pi 3B)|INPUT:Joystick & Mini-me controller|STRUTTURA:Stampa 3D (Ref. SO-100)|MOTORI:Servo Kit"
        )
        db.session.add_all([p1, p2, p3])
        db.session.commit()

@app.route('/')
def index():
    leaders = TeamMember.query.filter_by(manager_id=None).order_by(TeamMember.order_num).all()
    projects = Project.query.order_by(Project.order_num).all()
    return render_template('index.html', leaders=leaders, projects=projects)

@app.route('/project/<project_id>')
def project_detail(project_id):
    project = Project.query.get(project_id)
    if not project:
        return "Progetto non trovato", 404
    # Parse image paths
    images = project.image_paths.split(',') if project.image_paths else []
    return render_template('project.html', project=project, images=images)

if __name__ == '__main__':
    app.run(debug=False, port=5000)