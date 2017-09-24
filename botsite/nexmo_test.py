import nexmo

api_key = "a103fb2f"
api_secret = "fb9dee4414f37c1a"
my_num = "12034869067"
test_num = "6590917707"

client = nexmo.Client(key=api_key, secret=api_secret)

msg1 = "please"

client.send_message({
    'from': my_num,
    'to': test_num,
    'text': msg1
})
