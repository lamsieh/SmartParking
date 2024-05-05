import os
from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Chemin absolu fixe pour la base de données
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE = r'C:\Users\Hp\Desktop\SmartParking\instance\smart_parking.sqlite',
    )

    print("Instance path:", app.instance_path)  # Afficher le chemin d'instance

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Vérifier si le dossier instance existe avant de le créer
    if not os.path.exists(app.instance_path):
        try:
            os.makedirs(app.instance_path)
            # Confirmer la création du dossier
            print("Instance folder created.")
        except OSError as e:
            print(f"Error creating instance folder: {e}")
    else:
        print("Instance folder already exists.")

    from . import db
    db.init_app(app)


    from . import auth
    app.register_blueprint(auth.bp)

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
