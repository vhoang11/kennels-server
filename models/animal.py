class Animal():

    def __init__(self, name, breed, status, location_id, customer_id):
        self.name = name
        self.breed = breed
        self.status = status
        self.location_id = location_id
        self.customer_id = customer_id
        self.location = None # <--- ADD THIS LINE
