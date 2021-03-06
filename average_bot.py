"""
Live bot for notifying users with their average
"""
import time
from slackclient import SlackClient
import argparse

UPDATE_INTERVAL = 60 # seconds delay between updating the total average
READ_WEBSOCKET_DELAY = 1 # second delay between reading

def parse_args():
    parser = argparse.ArgumentParser(description='Slack Average Calc Bot.')
    parser.add_argument('-t', '--token', help='the bot token', required=True)
    return parser.parse_args()

# Dummy way to determine if str is float
def is_float(str):
    try:
        float(str)
        # Yeah, i'm sure there's a better way to do this.
        #  might be some regex like r"^[-+]?(?:\b[0-9]+(?:\.[0-9]*)?|\.[0-9]+\b)(?:[eE][-+]?[0-9]+\b)?$"
        if str in ['NaN', '-NaN', '+NaN', 'infinity', '-iNF', 'nan', '-nan', '+nan']:
            return False
        return True
    except ValueError:
        return False

# Calculating the average of all users
# @param sums_dict: dictionary of dictionaries {user:{sum:[float], count:[int]}}
def calc_all_average(sums_dict):
    all_sum = sum([x.get("sum") for x in sums_dict.values()])
    counter = sum([x.get("count") for x in sums_dict.values()])
    if counter == 0:
        return 0
    else:
        return all_sum/counter

# Updating the sums dict with the new number
# @param sums: sums dictionary of the form {user:{sum:int , count:int}}
# @param user: the user to update in the sums dict
# @param number: the number to add to the sum
def update_sums(sums, user, number):
    if not sums.has_key(user):
        sums[user] = {}
        sums[user][u'sum'] = 0
        sums[user][u'count'] = 0
    sums[user][u'sum'] += number
    sums[user][u'count'] += 1



def main():

    args = parse_args()
    bot_token = args.token

    # Create the slackclient instance
    sc = SlackClient(bot_token)

    # Saving sums and counter in order to be secured (do not save specific numbers)
    sums = {}

    last_update = time.time()

    # Connect to slack
    if sc.rtm_connect():
        while True:
            # Read latest messages
            for slack_message in sc.rtm_read():
                message = slack_message.get('text')
                user = slack_message.get('user')
                channel = slack_message.get('channel')
                if not message or not user:
                    continue
                # Assuming the only messages to get numbers from are with numbers only (no text)
                if is_float(message):
                    update_sums(sums, user, float(message))
                    average = sums[user].get('sum') / sums[user].get('count')
                    # Assuming it should write the user's average in the latest channel it got the message from
                    sc.rtm_send_message(channel, '<@{}> Average: {}'.format(user, str(average)))

                # Assuming it doesn't have to be exactly 60 seconds
                if time.time() - last_update > UPDATE_INTERVAL:
                    # Assuming general channel exists and public
                    sc.rtm_send_message('general', 'All users average: {}'.format(str(calc_all_average(sums))))
                    last_update = time.time()
            # Sleep for 1 second
            time.sleep(READ_WEBSOCKET_DELAY)

if __name__ == '__main__':
    main()

