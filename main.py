from mcp.server.fastmcp import FastMCP
import docker

mcp = FastMCP("container")

@mcp.tool()
async def send_sh_command(command: str):
    """Send an sh command to the Alpine linux container that was newly created at the beginning of this conversation. The output produced by the command will be returned.

    Args:
        command: the sh command to send to the Alpine container
    """
    if not container:
        print("Container not initialized yet during")
        exit(1)
    exec_result = container.exec_run(["/bin/sh", "-c", command])
    output = exec_result.output.decode("utf-8").strip()
    print(f"\nCommand: {command}")
    print(f"Output: {output}")
    print(f"Exit Code: {exec_result.exit_code}")
    return output

def initialize_container():
    # Initialize the Docker client
    client = docker.from_env()

    # Define container parameters for an Alpine container
    container_config = {
        "image": "alpine:latest",  # Use Alpine image
        "name": "my-alpine-container",  # Name the container
        "detach": True,  # Run in the background
        "auto_remove": True,  # Remove container when it stops
        "command": "tail -f /dev/null"
    }

    container = None

    try:
        # Start the container
        container = client.containers.run(**container_config)
        print(f"Container {container.name} started with ID {container.id}")
    except docker.errors.APIError as e:
        print(f"Error: {e}")
    except docker.errors.ImageNotFound:
        print("Error: Alpine image not found. Please pull it first using 'docker pull alpine:latest'.")
    
    return container

def stdio_command(container):
    command = input("Command: ")
    exec_result = container.exec_run(["/bin/sh", "-c", command])
    output = exec_result.output.decode("utf-8").strip()
    print(f"\nCommand: {command}")
    print(f"Output: {output}")
    print(f"Exit Code: {exec_result.exit_code}")

def test_commands(container):
    # Send a command to the container's shell (e.g., 'echo "Hello, Alpine!"')
    command = 'echo "Hello, Alpine!"'
    exec_result = container.exec_run(["/bin/sh", "-c", command])

    # Get the command output and exit code
    output = exec_result.output.decode("utf-8").strip()
    exit_code = exec_result.exit_code
    print(f"Command: {command}")
    print(f"Output: {output}")
    print(f"Exit Code: {exit_code}")

    # pwd = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
    # print(pwd.stdout)

    # Send another command (e.g., 'ls -l')
    command = "ls -l"
    exec_result = container.exec_run(["/bin/sh", "-c", command])
    output = exec_result.output.decode("utf-8").strip()
    print(f"\nCommand: {command}")
    print(f"Output: {output}")
    print(f"Exit Code: {exec_result.exit_code}")

def main():
    global container 
    container = initialize_container()
    if not container:
        print("Failed to initialize docker container.")
        exit(1)

    try:
        while True:
            # stdio_command(container)
            pass
    finally:
        container.kill()
        print(f"Container {container.name} stopped and will be auto-removed.")

if __name__ == "__main__":
    main()
