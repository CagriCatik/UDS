import socket

# Define UDS service identifiers
SERVICE_READ_VERSION = 0x22
SOFTWARE_VERSION_ID = 0xF190
HARDWARE_VERSION_ID = 0xF191

# Map identifier to a readable name
IDENTIFIERS = {
    SOFTWARE_VERSION_ID: "Software Version",
    HARDWARE_VERSION_ID: "Hardware Version",
}

def create_request(service_id, identifier):
    """Create a UDS request message."""
    # Service ID (1 byte) + Identifier (2 bytes)
    return bytes([service_id]) + identifier.to_bytes(2, byteorder='big')

def send_request(host='localhost', port=13400, request_data=None):
    """Send a UDS request to the ECU server and receive the response."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            # Send request to ECU
            client_socket.send(request_data)
            
            # Receive and print the response
            response = client_socket.recv(1024)
            print(f"Response from ECU: {response.decode()}")
    except Exception as e:
        print(f"Error while sending request: {e}")

def manual_input():
    """Handle manual input for requests."""
    while True:
        print("\nWelcome to the UDS Tester Client!")
        print("Available identifiers:")
        for identifier, name in IDENTIFIERS.items():
            print(f"ID: {hex(identifier)} - {name}")
        
        # Ask for the identifier (in hex format)
        identifier_input = input("Enter the identifier (in hex, e.g., F190 for software version): ")

        # Validate the identifier input
        if not identifier_input:
            print("Error: Input cannot be empty. Please enter a valid identifier.")
            continue
        
        try:
            identifier = int(identifier_input, 16)
        except ValueError:
            print("Error: Invalid hex format. Please enter a valid identifier (e.g., F190).")
            continue

        # Check if the identifier exists
        if identifier not in IDENTIFIERS:
            print(f"Error: Invalid identifier {hex(identifier)}. Please choose a valid identifier.")
            continue

        # Create the request for reading data by identifier
        request_data = create_request(SERVICE_READ_VERSION, identifier)
        
        # Send the request and print the response
        print(f"Sending request for identifier {hex(identifier)}...")
        send_request(request_data=request_data)

        # Ask if the user wants to send another request
        another = input("Do you want to send another request? (y/n): ").lower()
        if another != 'y':
            print("Exiting the tester client.")
            break

if __name__ == "__main__":
    try:
        manual_input()
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
