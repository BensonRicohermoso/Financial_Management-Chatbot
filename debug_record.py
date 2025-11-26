"""Diagnostic script: parse a message, insert transaction, and print DB rows."""
import traceback

def run():
    try:
        from chatbot.message_parser import MessageParser
        from models.transaction import Transaction
    except Exception:
        print('Import error when importing modules:')
        traceback.print_exc()
        return

    try:
        parser = MessageParser()
        txn_model = Transaction()

        message = 'I spent 50 pesos today'
        print('Parsing message:', message)
        parsed = parser.parse_message(message)
        print('Parsed result:', parsed)

        if parsed['intent'] == 'record_transaction':
            tid = txn_model.create_transaction(
                transaction_type=parsed['action'],
                amount=parsed['amount'],
                category_id=parsed['category_id'],
                description=parsed['description'],
                date=parsed['date']
            )
            print('Inserted transaction id:', tid)
        else:
            print('Message was not recognized as a transaction.')

        # Print recent transactions
        txns = txn_model.get_transactions(limit=10)
        print('\nRecent transactions:')
        for t in txns:
            print(dict(t))

    except Exception:
        print('Error during diagnostic run:')
        traceback.print_exc()

if __name__ == '__main__':
    run()
