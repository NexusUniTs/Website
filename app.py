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
        pietro = TeamMember(name="Pietro Dean", persona="Pietro Dean", role="Presidente")
        martina = TeamMember(name="Martina Anese", persona="Martina Anese", role="Direttrice tecnica, Capa reparto elettronica")
        alessio = TeamMember(name="Alessio Tessaris", persona="Tessaris Alessio", role="Capo reparto Meccanica")
        db.session.add_all([pietro, martina, alessio])
        db.session.commit()
        
        andrea = TeamMember(name="Andrea Da Dalt", persona="Andrea", role="", manager_id=pietro.id)
        db.session.add(andrea)
        
        luka = TeamMember(name="Luka Dencic", persona="luka.dencic", role="", manager_id=alessio.id)
        daniele_t = TeamMember(name="Daniele Tessaris", persona="Daniele", role="", manager_id=alessio.id)
        
        denis = TeamMember(name="Denis Trokan", persona="TROKAN DENIS", role="Capo reparto Informatica")
        db.session.add(denis)
        db.session.commit()
        
        riccardo = TeamMember(name="Riccardo Samaritan", persona="Riccardo Samaritan", role="", manager_id=denis.id)
        tushy = TeamMember(name="Alessio Tushy", persona="tushy", role="", manager_id=denis.id)
        deiana = TeamMember(name="Daniele Deiana", persona="DEIANA DANIELE", role="", manager_id=denis.id)
        
        db.session.add_all([luka, daniele_t, riccardo, tushy, deiana])
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
            title='ROBOTIC ARM',
            short_desc="Braccio manipolatore a 6 gradi di libertà stampato in 3D con leghe leggere, motori stepper di precisione zero-backlash e cinematica inversa per computer vision.",
            long_desc="Questo braccio robotico a 6 DOF è ingegnerizzato tramite complessi calcoli matriciali. Integra un sistema modulare per scambiare strumenti. Grazie ad una telecamera collegata all'IA, possiede percezione ambientale nativa.",
            status='IN PROGRESS',
            status_color='magenta',
            order_num=3,
            image_paths="",
            video_url="",
            specs="KERNEL:STABLE|POWER:12V LI-ION|CONNECTION:SECURE"
        )
        db.session.add_all([p1, p2, p3])
        db.session.commit()

@app.route('/')
def index():
    leaders = TeamMember.query.filter_by(manager_id=None).all()
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