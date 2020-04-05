#SQLALCHEMY_DATABASE_URI = 'sqlite:///hachione.db'
SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}/{name}'.format(**{
    'user': 'usr',
    'password': 'pass',
    'host': '127.0.0.1',
    'name': 'hachionemap'
})
SECRET_KEY = 'secret tamotamo'
