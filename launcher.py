import subprocess
import sys
import os
import time
import webbrowser

if __name__ == "__main__":
    time.sleep(1)
    webbrowser.open("http://localhost:8501")
    subprocess.Popen(["streamlit", "run", "app.py"], shell=True)
