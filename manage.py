""" RUN RUN RUN !

"""
from ButterSalt import app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("migrate", MigrateCommand)

if __name__ == "__main__":
    manager.run()
