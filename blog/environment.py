"""Environment, for connecting to db, yada yada.
"""

import yaml
import sqlalchemy

from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL as db_url

from utils import memoized

class Error(Exception): pass
class LoadConfigError(Error): pass
class BadConfigError(Error): pass

class Environment(object):
    def __init__(self, config_path):
        self.config_path = config_path

    @property
    def config(self):
        """Returns config dictionary for blog.
        """
        try:
            return yaml.load(file(self.config_path, "r"))
        except IOError, e:
            raise LoadConfigError("Unable to load config file '%s': %s" % \
                                      (e.filename, e.strerror))

    @property
    def database_url(self):
        try:
            return db_url(**self.config["database"])
        except TypeError, e:
            raise BadConfigError("Could not load database details from config.")

    @property
    @memoized
    def database_engine(self):
        """Returns the sqlalchemy database engine object created via the
        details in the config.
        """
        return sqlalchemy.create_engine(self.database_url)

    @property
    @memoized
    def session_maker(self):
        """Session maker, for creating new database sessions.
        """
        return sessionmaker(bind=self.database_engine)

    def create_database_session(self):
        """Returns a new database session.
        """
        return self.session_maker()
