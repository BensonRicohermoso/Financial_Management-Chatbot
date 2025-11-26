from chatbot.message_parser import MessageParser

p = MessageParser()
msgs = ['weekly summary', 'show this week summary', 'show weekly summary', 'show this week']

for m in msgs:
    print('MSG ->', m)
    print(p.parse_message(m))
    print()
