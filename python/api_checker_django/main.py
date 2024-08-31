import subprocess
import os

def start_django_server():
    """
    Starts the Django development server in a separate process.
    """
    # Run the Django server in a subprocess
    process = subprocess.Popen(
        ["python", "manage.py", "runserver "],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return process

def stop_django_server(process):
    """
    Stops the Django development server.
    """
    process.terminate()
    process.wait()

def main():
    # Start the Django server
    #os.chdir(path)
    print(os.getcwd())
    print("Starting Django server...")
    process = subprocess.Popen(
    ["python", "manage.py", "runserver "],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE)
    looper = True
    while looper is True:
        looper = input('Type False or use ctrl+c to exit: ')

if __name__ == '__main__':
    main()
