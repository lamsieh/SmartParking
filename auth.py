import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

from flask import jsonify

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


@bp.route('/dashboard', methods=['GET', 'POST'])
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
        with db:
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

        return render_template('dashboard/acceuil.html')
    else:
        return error, 400


@bp.route('/members', methods=['GET'])
def members_page():
    db = get_db()
    members = db.execute('SELECT * FROM Member').fetchall()
    return render_template('dashboard/members.html', members=members)


@bp.route('/members/data', methods=['GET'])
def members_data():
    db = get_db()
    try:
        query = """
        SELECT Member.ID, Member.LastName, Member.FirstName, Member.Phone, Member.Email, Member.isPayed,
        GROUP_CONCAT(LicensePlate.PlateNumber, ', ') AS Matricules
        FROM Member
        LEFT JOIN LicensePlate ON Member.ID = LicensePlate.MemberID
        GROUP BY Member.ID
        """
        members = db.execute(query).fetchall()
        print(members)  # Check what's being fetched
        return jsonify([dict(member) for member in members])
    except Exception as e:
        print(e)  # Log any errors
        return jsonify({'error': str(e)}), 500


@bp.route('/guests/data', methods=['GET'])
def guests_data():
    db = get_db()
    try:
        # Join Guest, LicensePlate, and calculate price to pay
        query = """
        SELECT Guest.ID, Guest.Code, LicensePlate.PlateNumber, LicensePlate.EntryDate, LicensePlate.ExitDate,
        ROUND((JULIANDAY(LicensePlate.ExitDate) - JULIANDAY(LicensePlate.EntryDate)) * 24 * Rates.Price, 2) AS PriceToPay
        FROM Guest
        JOIN LicensePlate ON Guest.ID = LicensePlate.GuestID
        JOIN Rates ON JULIANDAY(LicensePlate.ExitDate) - JULIANDAY(LicensePlate.EntryDate) <= Rates.Duration
        ORDER BY Guest.ID
        """
        guests = db.execute(query).fetchall()
        return jsonify([dict(guest) for guest in guests])
    except Exception as e:
        print(e)  # Log any errors
        return jsonify({'error': str(e)}), 500


@bp.route('/delete_member/<int:member_id>', methods=['POST'])
def delete_member(member_id):
    db = get_db()
    # Vérification si le membre existe
    member = db.execute('SELECT * FROM Member WHERE ID = ?', (member_id,)).fetchone()
    if not member:
        return jsonify({'error': 'Member not found'}), 404

    # Suppression du membre
    db.execute('DELETE FROM Member WHERE ID = ?', (member_id,))
    db.commit()
    return jsonify({'success': 'Member deleted successfully'}), 200


@bp.route('/update_member/<int:member_id>', methods=['POST'])
def update_member(member_id):
    db = get_db()
    data = request.get_json()  # This should correctly parse the JSON sent from the client

    try:
        db.execute('''
            UPDATE Member
            SET FirstName = ?, LastName = ?, Phone = ?, Email = ?, isPayed = ?
            WHERE ID = ?
        ''', (data['firstName'], data['lastName'], data['phone'], data['email'], data['isPayed'], member_id))
        db.commit()
        return jsonify({'status': 'success', 'message': 'Member updated successfully!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
