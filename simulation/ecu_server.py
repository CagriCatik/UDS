import socket

# Define UDS service identifiers
SERVICE_READ_VERSION = 0x22
SOFTWARE_VERSION_ID = 0xF190
HARDWARE_VERSION_ID = 0xF191

# Simulated ECU data
ecu_data = {
    SOFTWARE_VERSION_ID: b"Software Version: 1.2.3",
    HARDWARE_VERSION_ID: b"Hardware Version: A1B2C3"
}

def handle_client_request(data):
    """Handle the request from the client and return a response."""
    # Extract service ID and identifier from the request
    service_id = data[0]
    identifier = int.from_bytes(data[1:3], byteorder='big')
    
    # Check if the service ID is valid
    if service_id == SERVICE_READ_VERSION:
        if identifier in ecu_data:
            # Return the corresponding data
            return ecu_data[identifier]
        else:
            return b"Error: Invalid Identifier"
    else:
        return b"Error: Invalid Service"

def start_ecu_server(host='localhost', port=13400):
    """Start the ECU server to simulate UDS communication."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"ECU Server started on {host}:{port}")

        while True:
            # Accept client connection
            client_socket, client_address = server_socket.accept()
            with client_socket:
                print(f"Connected to {client_address}")
                
                # Receive client request (assuming 4 bytes for service and identifier)
                data = client_socket.recv(4)
                if not data:
                    break

                # Handle the request and send a response
                response = handle_client_request(data)
                print(f"ECU Response: {response.decode()}")
                client_socket.send(response)

if __name__ == "__main__":
    start_ecu_server()
