from flask import Flask, request
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv('.env')

# load env vars into app.config
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")

@app.get('/')
def index():
        return "hello world woasasrld"

@app.route('/test', methods=['GET', 'POST'])
def search():
       if request.method == 'POST':
             if 'username' in request.form:
                   return request.form['username']
             
             # check the parameters
             if request.args.get("username"):
                #    return "The user is:" + request.args.get("username")
                app.logger.debug('query params given')
                return {"hello": 1, "world": 2}
             return 'no user'
       else:
           return 'get method'
       
@app.post('/user/<path:user_id>')
def search2(user_id):
      return f"The user id: {user_id}"

@app.get('/env-vars')
def env_vars():
      return f"{app.config['SQLALCHEMY_DATABASE_URI']}"

if __name__ == "__main__":
      app.run(debug=True)  
