# NEXUS - Official Team Website

Il sito web ufficiale di **NEXUS UniTS**, il team universitario di robotica e innovazione con base operativa presso l'Innovation LAB **Asperastra** (Urban Center Trieste).

Il sito presenta le attività e i progetti del team (es. braccio robotico, ball balancing table, line follower), la composizione dei reparti con la gerarchia interna e la mappa interattiva della nostra sede.

---

## 🛠️ Stack Tecnologico

- **Backend:** Python + [Flask](https://flask.palletsprojects.com/)
- **Database:** SQLite gestito con [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- **Frontend:** HTML5, CSS3 personalizzato (stile Cyberpunk/Tech con canvas interattivo e video carousel), JavaScript nativo

---

## 📁 Struttura del Progetto

```text
Website/
├── app.py              # Applicazione Flask, modelli DB e logica delle rotte
├── nexus.db            # Database SQLite (generato automaticamente al primo avvio)
├── requirements.txt    # Dipendenze Python (Flask, Flask-SQLAlchemy)
├── templates/
│   ├── index.html      # Homepage (Hero, Progetti, Chi Siamo / Team, Location)
│   └── project.html    # Pagina di dettaglio per ciascun singolo progetto
└── static/
    ├── css/            # Fogli di stile (style.css con palette neon/dark)
    ├── js/             # Script del canvas interattivo e rotazione video
    ├── images/         # Foto dei progetti, logo Nexus e asset grafici
    └── videos/         # Clip video in background per la sezione Hero
```

---

## 🚀 Come avviare il sito in locale

### 1. Apri il terminale nella cartella del sito
Assicurati di trovarti nella cartella principale del progetto (la cartella che contiene `app.py`):
```bash
cd /percorso/del/progetto/Website
```

### 2. Prepara l'ambiente virtuale
Se hai già l'ambiente virtuale `.venv`, attivalo semplicemente:
```bash
source .venv/bin/activate
```

*(Se stai partendo da zero su un nuovo computer, puoi crearlo e installare le librerie così:)*
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Avvia il server Flask
Questo progetto **non è Django**: non usa `manage.py runserver`. È un'applicazione Flask con entry point `app.py`.

Fai partire l'app con:
```bash
python app.py
```

In alternativa puoi usare il comando Flask equivalente:
```bash
flask --app app run
```

*(Senza attivare prima il venv:)*
```bash
./.venv/bin/python app.py
```

### 4. Apri il sito nel browser
Una volta avviato il terminale, apri il browser e visita:
👉 **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

---

## 🛑 Come spegnere il server

Quando hai finito di lavorare o visualizzare il sito:
1. Torna nella finestra del terminale dove il server è in esecuzione.
2. Premi la combinazione **`CTRL + C`**.
3. Il server si arresterà liberando la porta.

---

## 💡 Note Utili & FAQ

### Come funziona il Database (`nexus.db`)?
- Il file `nexus.db` viene creato e popolato automaticamente all'avvio dell'app se non esiste già (tramite `db.create_all()` in `app.py`).
- **Vuoi ripristinare o resettare i dati del team e dei progetti ai valori di fabbrica?**  
  Basta eliminare il file `nexus.db`:
  ```bash
  rm nexus.db
  ```
  Al prossimo avvio con `python app.py` (oppure `flask --app app run`), il database verrà ricreato da zero con tutti i dati aggiornati definiti in `app.py`.

### Vuoi cambiare la porta da 5000 a 8000?
Su alcuni Mac la porta 5000 potrebbe essere utilizzata dal servizio di sistema AirPlay Receiver. Se vuoi cambiare la porta o usare la classica `8000`, basta modificare l'ultima riga di `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=False, port=8000)
```
In questo caso il sito sarà raggiungibile su `http://127.0.0.1:8000/`.

---

## 🔐 Backend amministrativo

Il pannello amministrativo è disponibile su:

```text
http://127.0.0.1:5000/admin/
```

Account temporaneo iniziale:

```text
Username: admin
Password: thisisunsafe
```

**Cambiare la password appena possibile.** Il pannello legge e modifica direttamente `nexus.db`, quindi i membri e i progetti già presenti sono disponibili automaticamente. Le immagini caricate vengono salvate in `static/images/projects/`.

Per caricare un'immagine associata a un progetto, aprire:

```text
/admin/upload/<ID_PROGETTO>
```

Sono consentiti JPG, JPEG, PNG, WebP e GIF, con limite massimo di 16 MB.

### Produzione su AWS Lightsail

Per un deploy Linux usare Gunicorn dietro Nginx. Esempio di avvio locale sul server:

```bash
source .venv/bin/activate
pip install -r requirements.txt
gunicorn --bind 127.0.0.1:8000 app:app
```

Impostare almeno una `SECRET_KEY` lunga e casuale nell'ambiente del servizio. Non esporre direttamente la porta Gunicorn su Internet: Nginx deve gestire il dominio e HTTPS.

Sono disponibili esempi pronti in `deploy/nexus.service` e `deploy/nginx-nexus.conf`. Dopo aver copiato il servizio:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now nexus
sudo nginx -t
sudo systemctl reload nginx
```

`ADMIN_USERNAME` e `ADMIN_PASSWORD` servono solo quando si crea un database nuovo senza utenti. Non impostare `ADMIN_PASSWORD` in modo permanente sul server: rimuoverla dopo la prima inizializzazione.
