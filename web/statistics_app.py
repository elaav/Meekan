"""
Statistics App
"""

import webapp2
from handlers import handle_404, handle_500
import argparse
from paste import httpserver
import routes


PORT = 8081
HOST = '127.0.0.1'

def parse_args():
    parser = argparse.ArgumentParser(description='Slack Statistics WebApp.')
    parser.add_argument('-t', '--token', help='the bot token to use for statistics', required=True)
    return parser.parse_args()

def main():
    args = parse_args()

    # initiating the app
    config = {}
    config['general'] = {'bot_token': args.token,}
    app = webapp2.WSGIApplication(config=config)
    routes.add_routes(app)
    app.error_handlers[404] = handle_404
    app.error_handlers[500] = handle_500

    httpserver.serve(app, host=HOST, port=PORT)

if __name__ == '__main__':
    main()