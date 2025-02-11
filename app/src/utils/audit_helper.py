import uuid


def generate_transaction_id():
    return str(uuid.uuid4())