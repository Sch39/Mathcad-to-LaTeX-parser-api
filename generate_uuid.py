import uuid

def generate_uuid_to_file(filename):
    # Generate a random UUID
    random_uuid = uuid.uuid4()
    
    # Write the UUID to the specified file
    with open(filename, 'w') as file:
        file.write(f"CLIENT_API_KEY={random_uuid}")
    
    print(f"CLIENT_API_KEY={random_uuid}")

# Contoh penggunaan fungsi
generate_uuid_to_file('.env')
