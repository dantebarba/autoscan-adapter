# save this as app.py
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def ping():
  return "Ping successfull"
  
@app.route("/triggers/manual", method=["POST"])
def manual_trigger():
  directories = request.args.getlist('dir')
  if directories:
    print(directories)
  return "Processed"
  
 
