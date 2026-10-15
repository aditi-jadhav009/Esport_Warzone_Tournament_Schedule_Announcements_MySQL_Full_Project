import os
from datetime import datetime
from functools import wraps

import mysql.connector
from flask import (Flask, flash, redirect, render_template, request, session,
                   url_for)
from mysql.connector import Error, IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

db_config = {
    "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "root"),
    "database": os.getenv("MYSQL_DATABASE", "esport_warzone")
}

def get_db_connection():
    return mysql.connector.connect(**db_config)


app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-before-deployment")

# Configure these environment variables, or edit defaults for your local MySQL setup.
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "root"),
    "database": os.getenv("MYSQL_DATABASE", "esport_warzone"),
}
GAMES = ["Free Fire", "BGMI", "Candy Crush Saga", "Subway Surfers", "Temple Run",
         "Mobile Legends: Bang Bang", "Dr. Driving", "Angry Birds", "Bubble Shooter"]

def get_connection():
    """Create a MySQL connection. MySQL Server must be running locally."""
    return mysql.connector.connect(**DB_CONFIG)

def query_all(sql, params=()):
    conn = get_connection()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params)
        return cur.fetchall()
    finally:
        cur.close()
        conn.close()

def init_db():
    """Create tables and seed the nine sample matches. Also provided in schema.sql."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS teams (
            id INT AUTO_INCREMENT PRIMARY KEY,
            team_name VARCHAR(100) NOT NULL UNIQUE,
            game_name VARCHAR(80) NOT NULL,
            captain_name VARCHAR(100) NOT NULL,
            contact VARCHAR(40) NOT NULL,
            department VARCHAR(80) NOT NULL DEFAULT 'ECE',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_teams_game_created (game_name, created_at)
        ) ENGINE=InnoDB""")
        cur.execute("""CREATE TABLE IF NOT EXISTS players (
            id INT AUTO_INCREMENT PRIMARY KEY,
            team_id INT NOT NULL,
            player_name VARCHAR(100) NOT NULL,
            game_uid VARCHAR(100) NOT NULL UNIQUE,
            role VARCHAR(60) NOT NULL DEFAULT 'Player',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_players_team FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
            INDEX idx_players_team (team_id)
        ) ENGINE=InnoDB""")
        cur.execute("""CREATE TABLE IF NOT EXISTS matches (
            id INT AUTO_INCREMENT PRIMARY KEY,
            match_name VARCHAR(120) NOT NULL,
            game_name VARCHAR(80) NOT NULL,
            arena VARCHAR(100) NOT NULL,
            start_at DATETIME NULL,
            end_at DATETIME NULL,
            status ENUM('Upcoming','Live','Completed') NOT NULL DEFAULT 'Upcoming',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_matches_game_status (game_name, status)
        ) ENGINE=InnoDB""")
        cur.execute("""CREATE TABLE IF NOT EXISTS announcements (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(160) NOT NULL,
            body TEXT NOT NULL,
            category ENUM('General','Registration','Schedule','Results','Rules') NOT NULL DEFAULT 'General',
            published TINYINT(1) NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_announcements_published (published, created_at)
        ) ENGINE=InnoDB""")
        # Lightweight migration for databases created by an earlier project version.
        cur.execute("SHOW COLUMNS FROM matches LIKE 'start_at'")
        if not cur.fetchone(): cur.execute("ALTER TABLE matches ADD COLUMN start_at DATETIME NULL AFTER arena")
        cur.execute("SHOW COLUMNS FROM matches LIKE 'end_at'")
        if not cur.fetchone(): cur.execute("ALTER TABLE matches ADD COLUMN end_at DATETIME NULL AFTER start_at")
        cur.execute("""CREATE TABLE IF NOT EXISTS player_accounts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(100) NOT NULL,
            email VARCHAR(160) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            game_name VARCHAR(80) NOT NULL,
            gamer_tag VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_player_accounts_game (game_name)
        ) ENGINE=InnoDB""")
        cur.execute("""CREATE TABLE IF NOT EXISTS results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            match_id INT NOT NULL,
            team_id INT NOT NULL,
            placement INT NOT NULL DEFAULT 0,
            kills INT NOT NULL DEFAULT 0,
            points INT NOT NULL DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            CONSTRAINT fk_results_match FOREIGN KEY (match_id) REFERENCES matches(id) ON DELETE CASCADE,
            CONSTRAINT fk_results_team FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
            UNIQUE KEY uq_result_match_team (match_id, team_id),
            INDEX idx_results_points (points)
        ) ENGINE=InnoDB""")
        conn.commit()
        cur.execute("SELECT COUNT(*) FROM matches")
        count = cur.fetchone()[0]
        if count == 0:
            sample = [
                ("Free Fire Qualifier", "Free Fire", "Bermuda", "2026-11-02 10:00:00", "2026-11-02 11:00:00"),
                ("BGMI Squad Qualifier", "BGMI", "Erangel", "2026-11-02 11:30:00", "2026-11-02 12:30:00"),
                ("Candy Crush Challenge", "Candy Crush Saga", "Classic Levels", "2026-11-02 13:00:00", "2026-11-02 13:30:00"),
                ("Subway Surfers Sprint", "Subway Surfers", "World Tour", "2026-11-02 13:45:00", "2026-11-02 14:15:00"),
                ("Temple Run Dash", "Temple Run", "Jungle Ruins", "2026-11-02 14:30:00", "2026-11-02 15:00:00"),
                ("Mobile Legends Showdown", "Mobile Legends: Bang Bang", "Land of Dawn", "2026-11-03 10:00:00", "2026-11-03 11:00:00"),
                ("Dr. Driving Time Trial", "Dr. Driving", "City Circuit", "2026-11-03 11:30:00", "2026-11-03 12:00:00"),
                ("Angry Birds Aim-Off", "Angry Birds", "Piggy Island", "2026-11-03 13:00:00", "2026-11-03 13:30:00"),
                ("Bubble Shooter Finals", "Bubble Shooter", "Arcade Arena", "2026-11-03 14:00:00", "2026-11-03 14:30:00"),
            ]
            cur.executemany("INSERT INTO matches (match_name, game_name, arena, start_at, end_at) VALUES (%s,%s,%s,%s,%s)", sample)
            cur.execute("INSERT INTO announcements (title, body, category, published) VALUES (%s,%s,%s,1)", ("Welcome to Esport Warzone", "Player registration is open. Check the match timetable regularly for schedule updates.", "Registration"))
            conn.commit()
    finally:
        cur.close()
        conn.close()

def db_is_available():
    try:
        conn = get_connection()
        conn.close()
        return True
    except Error:
        return False

@app.route("/")
def index():
    try:
        counts = query_all("""SELECT
            (SELECT COUNT(*) FROM teams) AS team_count,
            (SELECT COUNT(*) FROM players) AS player_count,
            (SELECT COUNT(*) FROM matches) AS match_count""")[0]
        upcoming = query_all("SELECT * FROM matches ORDER BY (start_at IS NULL), start_at, id LIMIT 9")
        announcements = query_all("SELECT * FROM announcements WHERE published=1 ORDER BY created_at DESC LIMIT 5")
        leaderboard = query_all("""SELECT t.team_name, t.game_name, SUM(r.points) AS points,
            SUM(r.kills) AS kills FROM results r JOIN teams t ON t.id=r.team_id
            GROUP BY t.id, t.team_name, t.game_name ORDER BY points DESC, kills DESC LIMIT 5""")
        connected = True
    except Error:
        counts, upcoming, leaderboard, announcements, connected = {"team_count": 0, "player_count": 0, "match_count": 0}, [], [], [], False
    return render_template("index.html", **counts, matches=upcoming, leaderboard=leaderboard,
                           announcements=announcements, games=GAMES, db_connected=connected)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        game = request.form.get("game_name", "").strip()
        name = request.form.get("team_name", "").strip()
        captain = request.form.get("captain_name", "").strip()
        contact = request.form.get("contact", "").strip()
        department = request.form.get("department", "ECE").strip() or "ECE"
        roster = [{"player_name": n.strip(), "game_uid": u.strip(), "role": r.strip() or "Player"}
                  for n, u, r in zip(request.form.getlist("player_name[]"),
                                     request.form.getlist("game_uid[]"), request.form.getlist("role[]"))
                  if n.strip() and u.strip()]
        if game not in GAMES or not all([name, captain, contact]):
            flash("Complete all team details and choose a valid game.", "error")
            return redirect(url_for("register"))
        if len(roster) < 2:
            flash("Add at least two players. For games without UIDs, enter a nickname or player ID.", "error")
            return redirect(url_for("register"))
        conn = None
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO teams (team_name, game_name, captain_name, contact, department) VALUES (%s,%s,%s,%s,%s)",
                        (name, game, captain, contact, department))
            team_id = cur.lastrowid
            cur.executemany("INSERT INTO players (team_id, player_name, game_uid, role) VALUES (%s,%s,%s,%s)",
                            [(team_id, p["player_name"], p["game_uid"], p["role"]) for p in roster])
            conn.commit()
            flash("Team registered successfully!", "success")
            return redirect(url_for("teams_page"))
        except IntegrityError:
            if conn: conn.rollback()
            flash("Team name or player ID already exists. Check your entries.", "error")
        except Error:
            if conn: conn.rollback()
            flash("Could not save registration. Check MySQL Server and database settings.", "error")
        finally:
            if conn:
                conn.close()
        return redirect(url_for("register"))
    return render_template("register.html", games=GAMES)

@app.route("/teams")
def teams_page():
    try:
        docs = query_all("""SELECT t.*, COUNT(p.id) AS player_count FROM teams t
            LEFT JOIN players p ON p.team_id=t.id GROUP BY t.id
            ORDER BY t.game_name, t.team_name""")
    except Error:
        docs = []
        flash("MySQL is unavailable. Start MySQL Server and check database settings.", "error")
    return render_template("teams.html", teams=docs)

@app.route("/leaderboard")
def leaderboard_page():
    try:
        rows = query_all("""SELECT t.team_name, t.game_name, SUM(r.points) AS points,
            SUM(r.kills) AS kills, COUNT(r.id) AS matches_played
            FROM results r JOIN teams t ON t.id=r.team_id
            GROUP BY t.id, t.team_name, t.game_name
            ORDER BY points DESC, kills DESC""")
    except Error:
        rows = []
        flash("MySQL is unavailable. Start MySQL Server and refresh.", "error")
    return render_template("leaderboard.html", rows=rows)

@app.route("/schedule")
def schedule_page():
    try:
        matches = query_all("SELECT * FROM matches ORDER BY (start_at IS NULL), start_at, id")
        announcements = query_all("SELECT * FROM announcements WHERE published=1 ORDER BY created_at DESC")
    except Error:
        matches, announcements = [], []
        flash("MySQL is unavailable. Start the database and refresh.", "error")
    return render_template("schedule.html", matches=matches, announcements=announcements)

def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            flash("Please sign in with the administrator account first.", "error")
            return redirect(url_for("admin_login"))
        return view(*args, **kwargs)
    return wrapped

@app.route("/player/register", methods=["GET", "POST"])
def player_register():
    if request.method == "POST":
        name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        game = request.form.get("game_name", "")
        tag = request.form.get("gamer_tag", "").strip()
        if not all([name, email, password, tag]) or game not in GAMES or len(password) < 8:
            flash("Complete all fields, choose a game, and use a password with at least 8 characters.", "error")
            return redirect(url_for("player_register"))
        try:
            conn = get_connection(); cur = conn.cursor()
            cur.execute("INSERT INTO player_accounts (full_name,email,password_hash,game_name,gamer_tag) VALUES (%s,%s,%s,%s,%s)",
                        (name, email, generate_password_hash(password), game, tag))
            conn.commit(); cur.close(); conn.close()
            flash("Player account created. You can now sign in.", "success")
            return redirect(url_for("player_login"))
        except IntegrityError:
            flash("That email is already registered. Please sign in instead.", "error")
        except Error:
            flash("Could not create account. Check the MySQL connection.", "error")
        return redirect(url_for("player_register"))
    return render_template("player_register.html", games=GAMES)

@app.route("/player/login", methods=["GET", "POST"])
def player_login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        try:
            rows = query_all("SELECT * FROM player_accounts WHERE email=%s LIMIT 1", (email,))
            if rows and check_password_hash(rows[0]["password_hash"], password):
                session.clear(); session["player_id"] = rows[0]["id"]
                flash("Welcome back to the Warzone!", "success")
                return redirect(url_for("player_dashboard"))
        except Error:
            flash("MySQL is unavailable. Check your database connection.", "error")
            return redirect(url_for("player_login"))
        flash("Invalid email or password.", "error")
    return render_template("player_login.html")

@app.route("/player/dashboard")
def player_dashboard():
    if not session.get("player_id"):
        return redirect(url_for("player_login"))
    try:
        player = query_all("SELECT id,full_name,email,game_name,gamer_tag,created_at FROM player_accounts WHERE id=%s", (session["player_id"],))[0]
        matches = query_all("SELECT * FROM matches WHERE game_name=%s ORDER BY id DESC", (player["game_name"],))
        scores = query_all("SELECT m.match_name,m.status,r.placement,r.kills,r.points FROM results r JOIN matches m ON m.id=r.match_id WHERE m.game_name=%s ORDER BY r.points DESC", (player["game_name"],))
    except (Error, IndexError):
        flash("Could not load your dashboard.", "error"); return redirect(url_for("player_login"))
    return render_template("player_dashboard.html", player=player, matches=matches, scores=scores)

@app.route("/player/logout")
def player_logout():
    session.pop("player_id", None); flash("You have been signed out.", "success")
    return redirect(url_for("index"))

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        # Configure ADMIN_USERNAME and ADMIN_PASSWORD in your environment before deployment.
        expected_user = os.getenv("ADMIN_USERNAME", "admin")
        expected_password = os.getenv("ADMIN_PASSWORD", "Warzone@2026")
        if username == expected_user and password == expected_password:
            session.clear(); session["is_admin"] = True; session["admin_name"] = username
            flash("Administrator access granted.", "success")
            return redirect(url_for("admin_dashboard"))
        flash("Incorrect administrator credentials.", "error")
    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None); session.pop("admin_name", None)
    flash("Administrator signed out.", "success")
    return redirect(url_for("index"))

@app.route("/admin")
@admin_required
def admin_dashboard():
    try:
        stats = query_all("SELECT (SELECT COUNT(*) FROM teams) teams,(SELECT COUNT(*) FROM player_accounts) players,(SELECT COUNT(*) FROM matches) matches,(SELECT COUNT(*) FROM results) results")[0]
        match_docs = query_all("SELECT * FROM matches ORDER BY id DESC")
        team_docs = query_all("SELECT * FROM teams ORDER BY team_name")
        result_docs = query_all("SELECT r.*,m.match_name,t.team_name,t.game_name FROM results r JOIN matches m ON m.id=r.match_id JOIN teams t ON t.id=r.team_id ORDER BY r.updated_at DESC")
        accounts = query_all("SELECT id,full_name,email,game_name,gamer_tag,created_at FROM player_accounts ORDER BY created_at DESC LIMIT 12")
        announcement_docs = query_all("SELECT * FROM announcements ORDER BY created_at DESC LIMIT 30")
    except Error:
        stats, match_docs, team_docs, result_docs, accounts, announcement_docs = {"teams":0,"players":0,"matches":0,"results":0}, [], [], [], [], []
        flash("Database unavailable. Start MySQL Server and refresh.", "error")
    return render_template("admin.html", matches=match_docs, teams=team_docs, results=result_docs, stats=stats, accounts=accounts, announcements=announcement_docs, games=GAMES)

@app.route("/admin/matches", methods=["POST"])
@admin_required
def admin_create_match():
    name = request.form.get("match_name", "").strip(); game = request.form.get("game_name", ""); arena = request.form.get("arena", "").strip()
    status = request.form.get("status", "Upcoming")
    start_at = request.form.get("start_at", "").strip() or None
    end_at = request.form.get("end_at", "").strip() or None
    if not name or not arena or game not in GAMES or status not in ["Upcoming", "Live", "Completed"] or (start_at and end_at and end_at < start_at):
        flash("Enter a match name, valid game, arena, and status.", "error")
    else:
        try:
            conn=get_connection(); cur=conn.cursor()
            cur.execute("INSERT INTO matches (match_name,game_name,arena,status,start_at,end_at) VALUES (%s,%s,%s,%s,%s,%s)",(name,game,arena,status,start_at,end_at))
            conn.commit(); cur.close(); conn.close(); flash("Tournament match created.", "success")
        except Error: flash("Could not create match. Check MySQL.", "error")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/matches/<int:match_id>/status", methods=["POST"])
@admin_required
def admin_match_status(match_id):
    status=request.form.get("status", "")
    if status not in ["Upcoming", "Live", "Completed"]:
        flash("Invalid match status.", "error")
    else:
        try:
            conn=get_connection(); cur=conn.cursor(); cur.execute("UPDATE matches SET status=%s WHERE id=%s",(status,match_id)); conn.commit(); cur.close(); conn.close()
            flash("Match status updated.", "success")
        except Error: flash("Could not update match status.", "error")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/matches/<int:match_id>/delete", methods=["POST"])
@admin_required
def admin_delete_match(match_id):
    try:
        conn=get_connection(); cur=conn.cursor(); cur.execute("DELETE FROM matches WHERE id=%s",(match_id,)); conn.commit(); cur.close(); conn.close()
        flash("Match deleted with its results.", "success")
    except Error: flash("Could not delete match.", "error")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/results", methods=["POST"])
@admin_required
def admin_results():
    try:
        match_id=int(request.form["match_id"]); team_id=int(request.form["team_id"])
        placement=int(request.form["placement"]); kills=int(request.form["kills"]); points=int(request.form["points"])
        if min(placement,kills,points)<0 or placement == 0: raise ValueError("Invalid score")
        conn=get_connection(); cur=conn.cursor()
        cur.execute("INSERT INTO results (match_id,team_id,placement,kills,points) VALUES (%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE placement=VALUES(placement),kills=VALUES(kills),points=VALUES(points)",(match_id,team_id,placement,kills,points))
        conn.commit(); cur.close(); conn.close(); flash("Score saved and leaderboard recalculated.", "success")
    except (ValueError, KeyError, Error): flash("Check score fields and database connection.", "error")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/announcements", methods=["POST"])
@admin_required
def admin_create_announcement():
    title = request.form.get("title", "").strip()
    body = request.form.get("body", "").strip()
    category = request.form.get("category", "General")
    published = 1 if request.form.get("published") == "on" else 0
    if not title or not body or category not in ["General", "Registration", "Schedule", "Results", "Rules"]:
        flash("Enter an announcement title, message, and valid category.", "error")
    else:
        try:
            conn=get_connection(); cur=conn.cursor()
            cur.execute("INSERT INTO announcements (title,body,category,published) VALUES (%s,%s,%s,%s)",(title,body,category,published))
            conn.commit(); cur.close(); conn.close()
            flash("Announcement saved and published settings applied.", "success")
        except Error:
            flash("Could not save announcement. Check MySQL connection.", "error")
    return redirect(url_for("admin_dashboard") + "#announcements")

@app.route("/admin/announcements/<int:announcement_id>/delete", methods=["POST"])
@admin_required
def admin_delete_announcement(announcement_id):
    try:
        conn=get_connection(); cur=conn.cursor(); cur.execute("DELETE FROM announcements WHERE id=%s", (announcement_id,)); conn.commit(); cur.close(); conn.close()
        flash("Announcement deleted.", "success")
    except Error:
        flash("Could not delete announcement.", "error")
    return redirect(url_for("admin_dashboard") + "#announcements")

@app.route("/delete-team/<int:team_id>", methods=["POST"])
@admin_required
def delete_team(team_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM teams WHERE id=%s", (team_id,))
        conn.commit()
        cur.close()
        conn.close()
        flash("Team and related records deleted.", "success")
    except Error:
        flash("Could not delete team. Check MySQL connection.", "error")
    return redirect(url_for("teams_page"))

@app.route("/dbms-lab")
def dbms_lab():
    return render_template("dbms_lab.html")

if __name__ == "__main__":
    try:
        init_db()
        print("MySQL connected. Tables are ready.")
    except Error as exc:
        print("MySQL connection error:", exc)
        print("Open MySQL Workbench, start your local MySQL Server, and check MYSQL_USER/MYSQL_PASSWORD.")
    app.run(host="0.0.0.0", port=5000, debug=False)
