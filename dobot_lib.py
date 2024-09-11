import socket

######################### PORT SETUP #########################

# Create a TCP/IP socket
def create_socket(host='192.168.5.1', port=29999):
    """Create a TCP/IP socket."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock

# Send a command to the robot and receive the response
def send_command(sock, command):
    """Send a command to the robot and receive the response."""
    try:
        # Send command
        sock.sendall(command.encode('utf-8'))

        # Receive response
        response = sock.recv(1024).decode('utf-8')
        return response
    except Exception as e:
        return f"Error: {e}"

def startup():
    global sock
    host = '192.168.5.1'
    # for real robot: 192.168.1.1
    port = 29999
    # Create socket and connect to the robot
    sock = create_socket(host, port)
    print(f"Connected to robot at {host}:{port}")

def shutdown():
    # prompt user for some key to exit
    input("Press Enter to exit...")
    sock.close()
    print("Socket closed.")

######################### DOBOT SETTINGS #########################

# Power on the robot
def power_on():
    command = "PowerOn()"
    send_command(sock, command)

# Enable the robot
def enable_robot():
    command = "EnableRobot()"
    send_command(sock, command)

# Disable the robot
def disable_robot():
    command = "DisableRobot()"
    send_command(sock, command)

# Clear error alarms
def clear_error():
    command = "ClearError()"
    print("Error detected, clearing error...\n")
    send_command(sock, command)

# Control the collision sensitivity level (yellow light), accept value: 0-5
def set_collision_sensitivity(level):
    # level: 0-5, 0: disable collision detection
    command = f"SetCollisionLevel({level})"
    send_command(sock, command)

# Set the joint speed factor in percentage, accept value: 0-100
def set_speed_factor(ratio):
    command = f"SpeedFactor({ratio})"
    send_command(sock, command)


######################### ROBOT STATE #########################

# Get the current position of the robot (x, y, z, rx, ry, rz)
def get_pose():
    command = "GetPose()"
    response = send_command(sock, command)
    parts = response.split(',')
    x = parts[1]
    y = parts[2]
    z = parts[3]
    rx = parts[4]
    ry = parts[5]
    rz = parts[6]
    return [x, y, z, rx, ry, rz]

# Check if an error has occurred and return the error ID
def get_error_id():
    command = "GetErrorID()"
    response = send_command(sock, command)
    parts = response.split(',')
    error_id = parts[0]  # Extract error ID

    if error_id != '0': 
        print(f"Error ID: {response}")
        return response
    else:
        return None

######################### MOVEMENT #########################

# Move the robot based on joint angles (J1, J2, J3, J4, J5, J6)
def joint_movj(J1, J2, J3, J4, J5, J6):
    input("Press Enter to move..")
    command = f"MovJ(joint={{ {J1}, {J2}, {J3}, {J4}, {J5}, {J6} }})"
    send_command(sock, command)


### TODO: Fix the implementation of x, y, z, rx, ry, rz

# Move the robot linearly based on position (x, y, z, rx, ry, rz)
def movl(x, y, z, rx, ry, rz, speed=100):
    command = f"MovL(pose={{ {x},{y},{z},{rx},{ry},{rz} }}, v={speed})"
    send_command(sock, command)

def pose_movj(x, y, z, rx, ry, rz):
    input("Press Enter to move..")
    command = f"MovJ(pose={{ {x},{y},{z},{rx},{ry},{rz} }})"
    send_command(sock, command)

# Move the robot based on joint pose (x, y, z, rx, ry, rz)
def pose_ik_movj(x, y, z, rx, ry, rz):
    input("Press Enter to solve ik and move..")
    joint_angle_list = inverse_k(x, y, z, rx, ry, rz)
    if joint_angle_list is False:
        print("Inverse kinematics calculation failed")
        return
    command = f"MovJ(joint={{ {joint_angle_list[0]},{joint_angle_list[1]},{joint_angle_list[2]},{joint_angle_list[3]},{joint_angle_list[4]},{joint_angle_list[5]} }})"
    send_command(sock, command)

# Calculate joint angles (J1, J2, J3, J4, J5, J6) from joint pose (x, y, z, rx, ry, rz)
def inverse_k(x, y, z, rx, ry, rz, user=None, tool=None, use_joint_near=None, joint_near=None):
    # TODO: Implement optional arguments
    # command = f"InverseKin({x},{y},{z},{rx},{ry},{rz}, {user}, {tool}, {use_joint_near}, {joint_near})"
    command = f"InverseKin({x},{y},{z},{rx},{ry},{rz})"

    response = send_command(sock, command)
    # Debugging: Print the response
    print(f"Response: {response}")
    
    # Split the response by commas
    parts = response.split(',')
    
    # Check if the response has the expected number of parts
    if len(parts) < 8:
        raise ValueError("Unexpected response format")
    
    # Extract the error ID and joint values
    error_id = parts[0]  # Extract error ID
    # Extract joint values string
    J1 = parts[1]
    J2 = parts[2]
    J3 = parts[3]
    J4 = parts[4]
    J5 = parts[5]
    J6 = parts[6]
    
    # Check for error ID
    if error_id != '0':
        print(f"Error in inverse kinematics calculation: {error_id}")
        return False

    print(f"Joint values: {J1}, {J2}, {J3}, {J4}, {J5}, {J6}")
    
    return [J1, J2, J3, J4, J5, J6]
