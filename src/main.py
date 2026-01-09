import subprocess
import sys

subprocess.run([sys.executable, "-m", "streamlit", "run", "src/streamlit_app.py"])
