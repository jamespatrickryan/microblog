import os

from flask import Flask


def create_app(test_configuration=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='development',
        DATABASE=os.path.join(
            app.instance_path,
            'microblog.sqlite'
        )
    )

    from . import database, authentication, microblog

    database.initialize_app(app)

    app.register_blueprint(authentication.blueprint)
    app.register_blueprint(microblog.blueprint)

    if test_configuration is None:
        app.config.from_pyfile(
            'configuration.py',
            silent=True
        )
    else:
        app.config.from_mapping(test_configuration)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
