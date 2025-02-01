from ds_messenger import DirectMessenger
import unittest

test_user = DirectMessenger('168.235.86.101', 'testuser1234q', 'testpw132j')
recipient = DirectMessenger('168.235.86.101', 'testrecipient444', 'testpw132j')

class SendTest(unittest.TestCase):
    def test_no_token(self):
        test_user.token = None
        s = test_user.send('test message 1', 'testrecipient444')
        assert s is True, f'EXPECTED: True, RECEIVED: {s}'
    def test_with_token(self):
        assert test_user.token != None, 'ERROR'
        s = test_user.send('test message 2', 'testrecipient444')
        assert s is True, f'EXPECTED: True, RECEIVED: {s}'
    test_user.close_sock()

class RetrieveNewTest(unittest.TestCase):
    def test_no_token(self):
        recipient.token = None
        s = recipient.retrieve_new()
        assert type(s) is list, f'EXPECTED: list, RECEIVED: {type(s)}'
    def test_with_token(self):
        assert recipient.token != None, 'ERROR'
        s = recipient.retrieve_new()
        assert type(s) is list, f'EXPECTED: list, RECEIVED: {type(s)}'

class RetrieveAllTest(unittest.TestCase):
    def test_no_token(self):
        recipient.token = None
        s = recipient.retrieve_all()
        assert type(s) is list, f'EXPECTED: list, RECEIVED: {type(s)}'
    
    def test_with_token(self):
        assert recipient.token != None, 'ERROR'
        s = recipient.retrieve_all()
        assert type(s) is list, f'EXPECTED: list, RECEIVED: {type(s)}'
        recipient.close_sock()


if __name__ == '__main__':
    unittest.main()