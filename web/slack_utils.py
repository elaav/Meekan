
# get all slack users
def get_users(slack_client):
    return slack_client.api_call('users.list')

# return true if user is an existing slack user (name or is)
def is_user(slack_client, user):
    users = slack_client.api_call('users.list').get(u'members')
    for u in users:
        if user == u.get(u'name') or user == u.get(u'id'):
            if u.get(u'is_bot') == True:
                return False
            return True
    return False

# return true if user is an existing slack user id
def is_user_id(slack_client, user):
    users = slack_client.api_call('users.list').get(u'members')
    for u in users:
        if user == u.get(u'id'):
            return True
    return False

# get all slack channels
def get_channels(slack_client):
    channel_ids = []
    channels = slack_client.api_call("channels.list").get('channels')
    for channel in channels:
        channel_ids.append(channel.get('id'))
    return channel_ids

# convert user name to user id
def get_user_id(slack_client ,username):
    users = slack_client.api_call('users.list').get(u'members')
    for u in users:
        if username == u.get(u'name'):
            return u.get(u'id')

# get all user messages from history
def get_user_messages(slack_client, user):
    user_messages = []
    if not is_user_id(slack_client, user):
        slack_user = get_user_id(slack_client, user)
    else:
        slack_user = user
    channel_ids = get_channels(slack_client)
    for c_id in channel_ids:
        messages = slack_client.api_call("channels.history", channel=c_id).get('messages')
        for m in messages:
            if m.has_key(u'user') and m.get(u'user') == slack_user:
                user_messages.append(m.get('text'))
    return user_messages

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