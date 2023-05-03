import sqlite3
import json
from models import Location, Employee, Animal

LOCATIONS = [
    {
        "id": 1,
        "name": "Nashville North",
        "address": "8422 Johnson Pike"
    },
    {
        "id": 2,
        "name": "Nashville South",
        "address": "209 Emory Drive"
    }
]

# def get_all_locations():
# 		"""_summary_
# 		"""
# 		return LOCATIONS

# def get_single_location(id):
#  		# Variable to hold the found location, if it exists
#     requested_location = None

#     # Iterate the locationS list above. Very similar to the
#     # for..of loops you used in JavaScript.
#     for location in LOCATIONS:
#         # Dictionaries in Python use [] notation to find a key
#         # instead of the dot notation that JavaScript used.
#         if location["id"] == id:
#             requested_location = location

#     return requested_location
  

def create_location(location):
    # Get the id value of the last location in the list
    max_id = LOCATIONS[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the location dictionary
    location["id"] = new_id

    # Add the location dictionary to the list
    LOCATIONS.append(location)

    # Return the dictionary with `id` property added
    return location

def delete_location(id):
    # Initial -1 value for location index, in case one isn't found
    location_index = -1

    # Iterate the LOCATIONS list, but use enumerate() so that you
    # can access the index value of each item
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            # Found the location. Store the current index.
            location_index = index

    # If the location was found, use pop(int) to remove it from list
    if location_index >= 0:
        LOCATIONS.pop(location_index)

# def update_location(id, new_location):
#     # Iterate the LOCATIONS list, but use enumerate() so that
#     # you can access the index value of each item.
#     for index, location in enumerate(LOCATIONS):
#         if location["id"] == id:
#             # Found the location. Update the value.
#             LOCATIONS[index] = new_location
#             break

def update_location(id, new_location):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Location
            SET
                name = ?,
                address = ?
        WHERE id = ?
        """, (new_location['name'], new_location['address'], id, ))

        # Were any rows affected?
        # Did the client send an `id` that exists?
        rows_affected = db_cursor.rowcount

    # return value of this function
    if rows_affected == 0:
        # Forces 404 response by main module
        return False
    else:
        # Forces 204 response by main module
        return True

def get_all_locations():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address
        FROM location l
        """)

        # Initialize an empty list to hold all animal representations
        locations = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an location instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Location class above.
            location = Location(row['id'], row['name'], row['address'])
            
            locations.append(location.__dict__) # see the notes below for an explanation on this line of code.

    return locations

def get_single_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address,
            e.id employee_id,
            e.name employee_name,
            e.address employee_address,
            e.location_id employee_location_id,
            a.id animal_id,
            a.name animal_name,
            a.breed animal_breed,
            a.status animal_status,
            a.location_id animal_location_id,
            a.customer_id animal_customer_id
        FROM location l
        JOIN employee e
            ON l.id = e.location_id
        JOIN animal a
            ON l.id = a.location_id 
        WHERE l.id = ?
        """, ( id, ))

        # locations = []
        
        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create a location instance from the current row
        location = Location(data['id'], data['name'], data['address'])
        
        employee = Employee(data['employee_id'], data['employee_name'], data['employee_address'], data['employee_location_id'])
        
        animal = Animal(data['animal_id'], data['animal_name'], data['animal_breed'], data['animal_status'], data['animal_location_id'], data['animal_customer_id'])
        
        location.employee = employee.__dict__
        location.animal = animal.__dict__
        
        # locations.append(location.__dict__)

        return location.__dict__
