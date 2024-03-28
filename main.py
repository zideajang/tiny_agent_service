from multiagent.schema import Message
def test_message():
    message = Message(role='user', content='wtf')
    assert 'role' in message.to_dict()
    assert 'user' in str(message)
