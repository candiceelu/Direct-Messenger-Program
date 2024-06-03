from ds_messenger import DirectMessenger

test_user = DirectMessenger('168.235.86.101', 'testuser1234q', 'testpw132j')
recipient = DirectMessenger('168.235.86.101', 'testrecipient444', 'testpw132j')
def test_send():
    # Test without a token
    test_user.token = None
    s = test_user.send('test message 1', 'testrecipient444')
    assert s is True, f'EXPECTED: True, RECEIVED: {s}'
    # Test with a token
    if test_user.token is not None:
        s = test_user.send('test message 2', 'testrecipient444')
        assert s is True, f'EXPECTED: True, RECEIVED: {s}'
    else:
        print('ERROR: Unable to conduct test with existing token')
def test_retrieve_new():
    # Test without a token
    recipient.token = None
    s = recipient.retrieve_new()
    assert type(s) is list, f'EXPECTED: list, RECEIVED: {type(s)}'
    # Test with a token
    if recipient.token is not None:
        s = recipient.retrieve_new()
        assert type(s) is list, f'EXPECTED: list, RECEIVED: {type(s)}'
    else:
        print('ERROR: Unable to conduct test with existing token')
def test_retrieve_all():
    # Test without a token
    recipient.token = None
    s = recipient.retrieve_all()
    assert type(s) is list, f'EXPECTED: list, RECEIVED: {type(s)}'
    # Test with a token
    if recipient.token is not None:
        s = recipient.retrieve_all()
        assert type(s) is list, f'EXPECTED: list, RECEIVED: {type(s)}'
    else:
        print('ERROR: Unable to conduct test with existing token')

if __name__ == '__main__':
    test_send()
    test_retrieve_new()
    test_retrieve_all()