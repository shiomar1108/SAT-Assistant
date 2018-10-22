import uuid

def get_ticket_id():
	value = uuid.uuid4()
	print value
	return value