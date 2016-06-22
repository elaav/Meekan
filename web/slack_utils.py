
def get_users(slack_client):
    return slack_client.api_call('users.list')

def is_user(slack_client, user):
    #TODO
    return False

def get_channels(slack_client):
    channel_ids = []
    channels = slack_client.api_call("channels.list").get('channels')
    for channel in channels:
        channel_ids.append(channel.get('id'))
    return channel_ids

def get_user_messages(slack_client, user):
    #slack_client.api_call('search.messages')
    #TODO
    pass

#TODO move to relevant generic module
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