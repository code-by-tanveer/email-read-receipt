import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI',
        'mysql+pymysql://user:password@localhost/email_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
