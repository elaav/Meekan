from webapp2 import Route
from handlers import UserAverageHandler, AverageHandler

_routes = [
    Route('/average', AverageHandler),
    Route('/average/<user>', handler=UserAverageHandler, name='user')
]

def get_routes():
    return _routes

def add_routes(app):
    for r in _routes:
        app.router.add(r)