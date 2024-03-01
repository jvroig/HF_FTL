import subprocess
import sys
import os
import webbrowser

def create_venv(python_version):
    # Create a virtual environment named 'venv' using the specified Python version
    subprocess.run([python_version, "-m", "venv", "venv"])

def install_dependencies():
    # Activate the virtual environment
    activate_script = "venv\\Scripts\\activate" if os.name == "nt" else "venv/bin/activate"
    subprocess.run([activate_script], shell=True)

    # Install dependencies from requirements.txt
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def start_server():
    # Start the API backend server
    subprocess.Popen([sys.executable, "train_api.py"])

def open_frontend():
    # Open the train HTML file in the user's default web browser
    webbrowser.open("trainui.html")

def main():
    if len(sys.argv) > 1:
        python_version = sys.argv[1]
    else:
        python_version = sys.executable
    
    create_venv(python_version)
    install_dependencies()
    print("Starting server...")
    start_server()
    open_frontend()

if __name__ == "__main__":
    main()
