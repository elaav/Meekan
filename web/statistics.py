"""
Statistics app
"""
import webapp2
from slackclient import SlackClient
import argparse


PORT = 8081
HOST = '127.0.0.1'

def parse_args():
    parser = argparse.ArgumentParser(description='Slack Statistics WebApp.')
    parser.add_argument('-t', '--token', help='the bot token to use for statistics', required=True)
    return parser.parse_args()

def handle_404(request, response, exception):
    response.write('Oops! I could swear this page was here!')
    response.set_status(404)

def handle_500(request, response, exception):
    response.write('A server error occurred!')
    response.set_status(500)

#TODO import this from utils module
def is_float(str):
    try:
        float(str)
        # Yeah, i'm sure there's a better way to do this.
        #  might be some regex like r"^[-+]?(?:\b[0-9]+(?:\.[0-9]*)?|\.[0-9]+\b)(?:[eE][-+]?[0-9]+\b)?$"
        if str in ["NaN", "-NaN", "+NaN", "infinity", "-iNF", "nan", "-nan", "+nan"]:
            return False
        return True
    except ValueError:
        return False


# The total average
class Average(webapp2.RequestHandler):

    # Assuming we want the average of all numbers ever writen (using the history)
    def get(self):
        #TODO move all logic to app
        args = parse_args()
        token = args.token
        self.slack_client = SlackClient(token)

        # Retrieving channels
        channel_ids = []
        channels = self.slack_client.api_call("channels.list").get('channels')
        for channel in channels:
            channel_ids.append(channel.get('id'))

        all_sum = 0
        counter = 0
        # Retrieving messages
        for c_id in channel_ids:
            current_messages = self.slack_client.api_call("channels.history", channel=c_id).get('messages')
            for m in current_messages:
                if m.has_key(u'user'):
                    text = m.get('text')

                    if is_float(text):
                        all_sum += float(text)
                        counter += 1
        # Calculating the average
        if counter == 0:
            average = 0
        else:
            average = all_sum / counter

        self.response.write('Total average: {}'.format(str(average)))

# app config
app = webapp2.WSGIApplication([
    ('/average', Average),
], debug=True)
app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500

def main():
    from paste import httpserver
    httpserver.serve(app, host=HOST, port=PORT)

if __name__ == '__main__':
    main()