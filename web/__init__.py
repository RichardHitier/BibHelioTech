from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from bht_config import yml_settings
from web.app_logger import AppLogger
from web.config import Config, ProdConfig, DevConfig, TestConfig

db = SQLAlchemy()
mig = Migrate()
app_logger = AppLogger()


def create_app(bht_env=None):
    """App factory method
    takes environment variable as arg to choose between configuration:
    production, development, testing or default

    @return: running app
    """
    app = Flask(__name__)

    if bht_env is None or bht_env == "production":
        config_instance = ProdConfig()
    elif bht_env == "development":
        config_instance = DevConfig()
    elif bht_env == "testing":
        config_instance = TestConfig()
    else:
        config_instance = Config()

    app.config.from_mapping(yml_settings)
    app.config.from_object(config_instance)

    app_logger.init_app(app)
    db.init_app(app)
    mig.init_app(app, db)

    app.logger.info(
        "#+-#+-#+-#+-#+-#+-#+-#+-#+-#+- CREATE APP -+#-+#-+#-+#-+#-+#-+#-+#-+#-+#"
    )

    from web.main import bp as main_bp

    app.register_blueprint(main_bp)

    return app
