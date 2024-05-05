import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')





@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form)
        # Utilisez 'get' pour éviter les exceptions KeyError
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            # Gérez l'erreur si les données requises ne sont pas fournies
            flash('Username and password are required.')
            return render_template('auth/login.html'), 400  # Ajoutez un code de statut HTTP pour clarifier l'erreur

        db = get_db()
        user = db.execute(
            'SELECT * FROM User WHERE Username = ?', (username,)
        ).fetchone()

        if user is None:
            flash('Incorrect username.')
            return render_template('auth/login.html'), 404  # Utilisateur non trouvé

        if not check_password_hash(user['Password'], password):
            flash('Incorrect password.')
            return render_template('auth/login.html'), 403  # Mot de passe incorrect

        session.clear()
        session['UserID'] = user['ID']
        return redirect(url_for('auth.dashboard'))

    return render_template('auth/login.html')


@bp.route('/dashboard')
def dashboard():
    if 'UserID' in session:
        user_id = session['UserID']
        user = get_db().execute(
            'SELECT * FROM User WHERE ID = ?', (user_id,)
        ).fetchone()
        # Assuming you pass user details to the template
        return render_template('dashboard/acceuil.html', user=user)
    else:
        return redirect(url_for('auth.login'))


@bp.route('/logout')
def logout():
    # Clear any user information from the session
    session.pop('UserID', None)
    session.pop('logged_in', None)
    # Redirect to login page or home page
    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('UserID')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM User WHERE ID = ?', (user_id,)
        ).fetchone()


@bp.route('/create_admin', methods=['POST'])
def create_admin():
    db = get_db()
    error = None
    user = db.execute(
        'SELECT * FROM User WHERE Username = ?', ('admin',)
    ).fetchone()

    if user is not None:
        error = 'Admin user already exists.'

    if error is None:
        db.execute(
            'INSERT INTO User (Username, Password) VALUES (?, ?)',
            ('admin', generate_password_hash('admin'))
        )
        db.commit()
        return 'Admin user created successfully.'
    else:
        return error, 400


@bp.route('/members')
def members():
    # Rendre le template HTML pour la page "members.html" dans le dossier "dashboard"
    return render_template('dashboard/members.html')


@bp.route('/guests')
def guests():
    # Rendre le template HTML pour la page "guests.html" dans le dossier "dashboard"
    return render_template('dashboard/guests.html')


@bp.route('/parking')
def parking():
    # Rendre le template HTML pour la page "parking.html" dans le dossier "dashboard"
    return render_template('dashboard/parking.html')


@bp.route('/tarifs')
def tarifs():
    # Rendre le template HTML pour la page "tarifs.html" dans le dossier "dashboard"
    return render_template('dashboard/tarifs.html')

@bp.route('/camera')
def camera():
    # Rendre le template HTML pour la page "camera.html" dans le dossier "dashboard"
    return render_template('dashboard/camera.html')

@bp.route('/create_member', methods=['POST'])
def create_member():
    db = get_db()
    error = None

    data = request.form

    member = db.execute(
        'SELECT * FROM Member WHERE Email = ?', (data['email'],)
    ).fetchone()

    if member is not None:
        error = 'Member with this email already exists.'

    if error is None:
        # Insert the member into the Member table
        db.execute(
            'INSERT INTO Member (LastName, FirstName, Phone, Email, isPayed) VALUES (?, ?, ?, ?, ?)',
            (data['lastName'], data['firstName'], data['phone'], data['email'], data['isPayed'] == 'yes')
        )
        db.commit()

        # Get the ID of the newly inserted member
        member_id = db.execute('SELECT last_insert_rowid()').fetchone()[0]

        # Insert each matricule into the LicensePlate table
        matricules = request.form.getlist('matricule[]')
        for matricule in matricules:
            db.execute(
                'INSERT INTO LicensePlate (PlateNumber, MemberID) VALUES (?, ?)',
                (matricule, member_id)
            )
        db.commit()

        return 'Member created successfully.'
    else:
        return error, 400