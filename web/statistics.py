"""
Statistics app
"""
import webapp2
from slackclient import SlackClient
import argparse
import slack_utils


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

# Specific user average
class UserAverageHandler(webapp2.RequestHandler):
    def get(self, user):
        #TODO parse args and create slack client just once!
        args = parse_args()
        token = args.token
        slack_client = SlackClient(token)
        if slack_utils.is_user(slack_client, user):
            messages = slack_utils.get_user_messages(slack_client, user)
            average = 0
            self.response.write('Average for user {}: {}'.format(user, average))
        else:
            self.response.write('User {} was not found'.format(user))

# The total average
class AverageHandler(webapp2.RequestHandler):

    # Assuming we want the average of all numbers ever writen (using the history)
    def get(self):
        #TODO move all logic to app
        args = parse_args()
        token = args.token
        slack_client = SlackClient(token)

        # Retrieving channels
        channel_ids = slack_utils.get_channels(slack_client)

        all_sum = 0
        counter = 0
        # Retrieving messages
        for c_id in channel_ids:
            current_messages = slack_client.api_call("channels.history", channel=c_id).get('messages')
            for m in current_messages:
                if m.has_key(u'user'):
                    text = m.get('text')

                    if slack_utils.is_float(text):
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
    webapp2.Route('/average', AverageHandler),
    webapp2.Route('/average/<user>', handler=UserAverageHandler, name='user'),
], debug=True)
app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500

def main():
    from paste import httpserver
    httpserver.serve(app, host=HOST, port=PORT)

if __name__ == '__main__':
    main()