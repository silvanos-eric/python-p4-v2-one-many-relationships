# server/models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, event
from sqlalchemy.engine import Engine
from sqlite3 import Connection

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    })

db = SQLAlchemy(metadata=metadata)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    SQLite backend doesn't enable foreign key constraints by default. This
    enables foreign key constraints on the database connections.

    This is a workaround for a missing feature in Flask-SQLAlchemy, which
    doesn't support passing the sqlite_pragmas parameter to the underlying
    SQLAlchemy engine.

    See: https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#foreign-key-support
    """
    if isinstance(dbapi_connection, Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    hire_date = db.Column(db.Date)

    reviews = db.relationship('Review', backref="employee")
    onboarding = db.relationship('Onboarding',
                                 back_populates='employee',
                                 uselist=False)

    def __repr__(self):
        return f"<Employee {self.id}, {self.name}, {self.hire_date}>"


class Onboarding(db.Model):
    __tablename__ = "onboardings"

    id = db.Column(db.Integer, primary_key=True)
    orientation = db.Column(db.DateTime)
    forms_complete = db.Column(db.Boolean, default=False)

    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))

    employee = db.relationship('Employee', back_populates='onboarding')

    def __repr__(self):
        return f"<Onboarding {self.id}, {self.orientation}, {self.forms_complete}>"


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    summary = db.Column(db.String)

    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))

    def __repr__(self):
        return f"<Review {self.id}, {self.year}, {self.summary}>"
