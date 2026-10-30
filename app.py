from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from flask_wtf.csrf import CSRFProtect
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from markupsafe import Markup
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-this-secret-in-production')
app.config['MAX_CONTENT_LENGTH'] = 250 * 1024 * 1024  # 250 MB per video e immagini ad alta risoluzione
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'images', 'projects')
app.config['VIDEO_FOLDER'] = os.path.join(os.path.dirname(__file__), 'static', 'videos')
csrf = CSRFProtect(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'nexus.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class AdminUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(AdminUser, int(user_id))

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
    if not AdminUser.query.first() and os.environ.get('ADMIN_PASSWORD'):
        db.session.add(AdminUser(
            username=os.environ.get('ADMIN_USERNAME', 'admin'),
            password_hash=generate_password_hash(os.environ['ADMIN_PASSWORD'])
        ))
        db.session.commit()
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
        # 4. Reparto Marketing e Amministrazione
        pietro = TeamMember(
            name="Pietro Dean",
            role="Presidente & Capo Reparto Marketing e Amministrazione",
            department="REPARTO MARKETING E AMMINISTRAZIONE",
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
            long_desc="Questo braccio robotico è attualmente nella sua primissima fase di prototipazione (ispirato a piattaforme open-source come LeRobot SO-100). L'obiettivo di questa build iniziale è avere una base hardware pronta all'uso, permettendo al reparto informatica di iniziare a sviluppare il codice parallelamente alla progettazione 3D della versione finale.<br><br><strong>Direzione Tecnica Attuale:</strong><br>• <strong>Elaborazione (Core):</strong> Scheda con connettività Wi-Fi (es. Raspberry Pi 3B / MCU compatibili) per una gestione wireless.<br>• <strong>Interfaccia (Input):</strong> Pilotaggio remoto tramite 'Mini-me controller' e controlli analogici fisici (joystick) per movimenti fluidi.<br>• <strong>Meccanica (Output):</strong> Struttura base stampata in 3D azionata da un kit di servomotori standard.<br><br>Un approccio orientato all'iterazione rapida, che consente di portare avanti lo sviluppo software e gli algoritmi di controllo senza dover attendere la versione meccanica definitiva.",
            status='IN PROGRESS',
            status_color='magenta',
            order_num=3,
            image_paths="",
            video_url="",
            specs="CORE:Modulo Wi-Fi (Pi 3B)|INPUT:Joystick & Mini-me controller|STRUTTURA:Stampa 3D (Ref. SO-100)|MOTORI:Servo Kit"
        )
        db.session.add_all([p1, p2, p3])
        db.session.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    if request.method == 'POST':
        user = AdminUser.query.filter_by(username=request.form.get('username', '').strip()).first()
        if user and user.check_password(request.form.get('password', '')):
            login_user(user)
            return redirect(url_for('admin.index'))
        flash('Credenziali non valide.', 'error')
    return render_template('admin/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin/change-password', methods=['GET', 'POST'])
def change_password():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method == 'POST':
        current = request.form.get('current_password', '')
        new = request.form.get('new_password', '')
        if not current_user.check_password(current):
            flash('La password attuale non è corretta.', 'error')
        elif len(new) < 12:
            flash('La nuova password deve contenere almeno 12 caratteri.', 'error')
        else:
            current_user.password_hash = generate_password_hash(new)
            db.session.commit()
            flash('Password aggiornata.', 'success')
            return redirect(url_for('admin.index'))
    return render_template('admin/change_password.html')

class SecureAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return super().index()

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class TeamMemberAdminView(SecureModelView):
    column_list = ['order_num', 'department', 'name', 'role', 'manager']
    column_labels = {
        'order_num': '#',
        'department': 'Reparto',
        'name': 'Nome e Cognome',
        'role': 'Ruolo',
        'manager': 'Responsabile Diretto'
    }
    column_default_sort = ('order_num', False)
    column_filters = ['department']
    column_searchable_list = ['name', 'role', 'department']

class ProjectAdminView(SecureModelView):
    # Rimuoviamo long_desc e short_desc dalla lista per non comprimere la tabella orizzontalmente
    column_list = ['order_num', 'title', 'status', 'video_url', 'media_manager']
    column_labels = {
        'order_num': '#',
        'title': 'Titolo Progetto',
        'status': 'Stato',
        'video_url': 'Video Demo',
        'media_manager': 'Media (Foto / Video)'
    }
    column_default_sort = ('order_num', False)
    column_searchable_list = ['title', 'short_desc']
    column_filters = ['status']
    
    form_columns = ['order_num', 'title', 'short_desc', 'long_desc', 'status', 'status_color', 'specs', 'video_url', 'image_paths']
    form_widget_args = {
        'short_desc': {'rows': 3},
        'long_desc': {'rows': 8},
        'specs': {'rows': 2}
    }

    def _video_formatter(view, context, model, name):
        if model.video_url:
            return Markup(f'<a href="{model.video_url}" target="_blank" class="badge badge-success" style="padding: 6px 10px; font-size: 11px; text-decoration: none;">▶ Guarda Video</a>')
        return Markup('<span class="badge badge-secondary" style="padding: 6px 10px; font-size: 11px; opacity: 0.6;">Nessun video</span>')

    def _status_formatter(view, context, model, name):
        color = model.status_color or '#1a91f7'
        return Markup(f'<span class="badge badge-info" style="padding: 6px 10px; font-size: 11px; border: 1px solid {color}; background: rgba(0,0,0,0.3); color: #fff;">{model.status}</span>')

    def _media_manager_formatter(view, context, model, name):
        upload_url = url_for('upload_project_media', project_id=model.id)
        img_count = len([p for p in (model.image_paths or '').split(',') if p])
        has_video = '🎬 ' if model.video_url else '📁 '
        return Markup(f'<a href="{upload_url}" class="btn btn-sm btn-primary" style="font-weight: bold; padding: 6px 12px; font-size: 12px; border-radius: 4px;">{has_video}Carica Video / Foto ({img_count})</a>')

    column_formatters = {
        'video_url': _video_formatter,
        'status': _status_formatter,
        'media_manager': _media_manager_formatter
    }

admin = Admin(app, name='NEXUS Admin', index_view=SecureAdminIndexView())
admin.add_view(TeamMemberAdminView(TeamMember, db.session, name='Membri Team'))
admin.add_view(ProjectAdminView(Project, db.session, name='Progetti'))

@app.route('/admin/upload/<int:project_id>', methods=['GET', 'POST'])
def upload_project_media(project_id):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    project = db.session.get(Project, project_id)
    if not project:
        return 'Progetto non trovato', 404

    if request.method == 'GET':
        images = [p for p in (project.image_paths or '').split(',') if p]
        return render_template('admin/upload.html', project=project, images=images)

    action = request.form.get('action')

    # 1. Caricamento Video
    if action == 'upload_video':
        video_file = request.files.get('video_file')
        external_url = request.form.get('video_url', '').strip()

        if external_url:
            project.video_url = external_url
            db.session.commit()
            flash('Link video esterno aggiornato con successo!', 'success')
        elif video_file and video_file.filename:
            allowed_videos = {'mp4', 'webm', 'mov', 'm4v'}
            ext = video_file.filename.rsplit('.', 1)[-1].lower() if '.' in video_file.filename else ''
            if ext not in allowed_videos:
                flash('Formato video non valido. Usa MP4, WebM o MOV.', 'error')
                return redirect(url_for('upload_project_media', project_id=project.id))
            
            os.makedirs(app.config['VIDEO_FOLDER'], exist_ok=True)
            fname = secure_filename(f"project_{project.id}_{video_file.filename}")
            save_path = os.path.join(app.config['VIDEO_FOLDER'], fname)
            video_file.save(save_path)
            project.video_url = f"/static/videos/{fname}"
            db.session.commit()
            flash('Video caricato e collegato al progetto!', 'success')
        else:
            flash('Nessun file o URL video selezionato.', 'error')

    # 2. Rimozione Video
    elif action == 'remove_video':
        project.video_url = None
        db.session.commit()
        flash('Video rimosso dal progetto.', 'success')

    # 3. Caricamento Immagini (supporta upload multiplo)
    elif action == 'upload_images':
        image_files = request.files.getlist('image_files')
        allowed_images = {'jpg', 'jpeg', 'png', 'webp', 'gif'}
        uploaded_count = 0
        
        project_folder = os.path.join(app.config['UPLOAD_FOLDER'], f'project_{project.id}')
        os.makedirs(project_folder, exist_ok=True)
        paths = [p for p in (project.image_paths or '').split(',') if p]

        for img in image_files:
            if img and img.filename and '.' in img.filename:
                ext = img.filename.rsplit('.', 1)[-1].lower()
                if ext in allowed_images:
                    fname = secure_filename(img.filename)
                    save_path = os.path.join(project_folder, fname)
                    img.save(save_path)
                    rel_path = f'project_{project.id}/{fname}'
                    if rel_path not in paths:
                        paths.append(rel_path)
                        uploaded_count += 1

        if uploaded_count > 0:
            project.image_paths = ','.join(paths)
            db.session.commit()
            flash(f'{uploaded_count} foto caricate con successo!', 'success')
        else:
            flash('Nessuna immagine valida caricata.', 'error')

    # 4. Rimozione singola Immagine
    elif action == 'remove_image':
        img_to_remove = request.form.get('image_path')
        paths = [p for p in (project.image_paths or '').split(',') if p]
        if img_to_remove in paths:
            paths.remove(img_to_remove)
            project.image_paths = ','.join(paths)
            db.session.commit()
            flash('Immagine rimossa dalla galleria.', 'success')

    return redirect(url_for('upload_project_media', project_id=project.id))

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
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, port=port)
