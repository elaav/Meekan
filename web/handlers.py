import webapp2
from slackclient import SlackClient
import slack_utils


def handle_404(request, response, exception):
    response.write('Oops! I could swear this page was here!')
    response.set_status(404)

def handle_500(request, response, exception):
    response.write('A server error occurred!')
    response.set_status(500)

# Specific user average
class UserAverageHandler(webapp2.RequestHandler):
    def get(self, user):

        token = self.app.config.get('general').get('bot_token')
        slack_client = SlackClient(token)
        if slack_utils.is_user(slack_client, user):
            messages = slack_utils.get_user_messages(slack_client, user)
            sum = 0
            count = 0
            for m in messages:
                if slack_utils.is_float(m):
                    sum += float(m)
                    count += 1
            if count == 0:
                self.response.write('There were no numbers for user "{}"'.format(user))
            else:
                average = sum / count
                self.response.write('Average for user "{}": {}'.format(user, average))
        else:
            self.response.write('User "{}" is not a user'.format(user))

# The total average
class AverageHandler(webapp2.RequestHandler):

    # Assuming we want the average of all numbers ever writen (using the history)
    def get(self):
        token = self.app.config.get('general').get('bot_token')
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