from flask import Flask
import os

app = Flask(__name__)

print(f"Current Working Directory: {os.getcwd()}")
print(f"App Root Path: {app.root_path}")
print(f"Calculated Upload Path: {os.path.join(app.root_path, '../server/uploads')}")
print(f"Normalized Upload Path: {os.path.normpath(os.path.join(app.root_path, '../server/uploads'))}")
