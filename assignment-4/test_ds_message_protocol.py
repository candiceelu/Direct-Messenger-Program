from ds_protocol4 import direct_message, extract_json_dm, DMTuple
import json
import unittest


class DirectMessageTest(unittest.TestCase):
    def test_new_messages(self):
        token = "user_token"
        dm = "new"
        msg = direct_message(token, dm=dm)
        assert msg == '{"token": "user_token", "directmessage": "new"}', 'UNEXPECTED OUTPUT'
    def test_all_messages(self):
        token = "user_token"
        dm = "all"
        msg = direct_message(token, dm=dm)
        assert msg == '{"token": "user_token", "directmessage": "all"}', 'UNEXPECTED OUTPUT'
    def test_sending_message(self):
        token = "user_token"
        entry = "Hello World!"
        recipient = "bob1234"
        msg = json.loads(direct_message(token, entry=entry, recipient=recipient))
        assert msg["token"] == token, f'EXPECTED: {token}, RECEIVED: {msg["token"]}'
        assert msg["directmessage"]["entry"] == entry, f'EXPECTED: {entry}, RECEIVED: {msg["entry"]}'
        assert msg["directmessage"]["recipient"] == recipient, f'EXPECTED: {entry}, RECEIVED: {msg["recipient"]}'

class ExtractJsonTest(unittest.TestCase):
    def test_extract_successful_send(self):
        json_msg = '{"response": {"type": "ok", "message": "Direct message sent"}}'
        resp = extract_json_dm(json_msg)
        assert resp == DMTuple(type='ok', message='Direct message sent'), 'UNEXPECTED OUTPUT'
    def test_extract_successful_request(self):
        json_msg = '{"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}]}}'
        resp = extract_json_dm(json_msg)
        assert resp.type == 'ok'
        assert resp.message == [{'message': 'Hello User 1!', 'from': 'markb', 'timestamp': '1603167689.3928561'}, {'message': 'Bzzzzz', 'from': 'thebeemoviescript', 'timestamp': '1603167689.3928561'}], 'UNEXPECTED OUTPUT'

if __name__ == "__main__":
    unittest.main()