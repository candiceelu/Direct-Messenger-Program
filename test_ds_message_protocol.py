from ds_protocol4 import direct_message, extract_json_dm, DMTuple
import json

def test_direct_message():
    token = "user_token"
    dm_n = "new"
    dm_a = "all"
    entry = "Hello World!"
    recipient = "bob1234"
    # Tests requesting unread messages from DS server
    msg = direct_message(token, dm=dm_n)
    assert msg == '{"token": "user_token", "directmessage": "new"}', 'UNEXPECTED OUTPUT'
    # Tests requesting all messages from DS server
    msg = direct_message(token, dm=dm_a)
    assert msg == '{"token": "user_token", "directmessage": "all"}', 'UNEXPECTED OUTPUT'
    # Tests sending a dm to another DS user
    msg = json.loads(direct_message(token, entry=entry, recipient=recipient))
    assert msg["token"] == token, f'EXPECTED: {token}, RECEIVED: {msg["token"]}'
    assert msg["directmessage"]["entry"] == entry, f'EXPECTED: {entry}, RECEIVED: {msg["entry"]}'
    assert msg["directmessage"]["recipient"] == recipient, f'EXPECTED: {entry}, RECEIVED: {msg["recipient"]}'

def test_extract_json_dm():
    json_msg1 = '{"response": {"type": "ok", "message": "Direct message sent"}}'
    json_msg2 = '{"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}]}}'
    # Tests proper processing of server message -- sending dm was successful
    resp = extract_json_dm(json_msg1)
    assert resp == DMTuple(type='ok', message='Direct message sent'), 'UNEXPECTED OUTPUT'
    # Tests proper processing of server message -- requesting all/new messages
    resp = extract_json_dm(json_msg2)
    assert resp == [{'message': 'Hello User 1!', 'from': 'markb', 'timestamp': '1603167689.3928561'}, {'message': 'Bzzzzz', 'from': 'thebeemoviescript', 'timestamp': '1603167689.3928561'}], 'UNEXPECTED OUTPUT'
    

if __name__ == "__main__":
    test_direct_message()
    test_extract_json_dm()