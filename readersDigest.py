from flask import Flask,request,jsonify
from flask_restful import Api,Resource
from pymongo import MongoClient
import re
import bcrypt
from dotenv import load_dotenv
import os
from scraper import Scraper
from prompts import input_promts
from openai import OpenAI
from flask import render_template





# getting llm api key
load_dotenv(override=True)
api_key = os.getenv("GROQ_API_KEY")

#initializing flask app
app = Flask(__name__)

api = Api(app)

# client = MongoClient("mongodb://db:27017")
# client = MongoClient('localhost', 27017)

# db = client.scrapper

# users = db["users"]

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri)

db = client.scrapper
users = db["users"]

#helper functions

# scrap = Scraper()

def generate_message(status_code,message):
    retjson = {
        "Status_Code" : status_code,
        "Message" : message
    }
    return retjson

def existUser(username):
    if users.count_documents({
        "Username" : username
    }) == 0:
        return False
    else:
        return True

def countTokens(username):
    if existUser(username):
        return users.find_one({"Username":username})["Token"]
    return 0

def verifyPw(username, password):
    if not existUser(username):
        return False

    hashed_pw = users.find_one({
        "Username":username
    })["Password"]

    if bcrypt.checkpw(password.encode('utf8'), hashed_pw):
        return True
    else:
        return False


def verifyCredentials(username, password):
    if not existUser(username):
        return generate_message(301, "Invalid Username"), True

    correct_pw = verifyPw(username, password)

    if not correct_pw:
        return generate_message(302, "Incorrect Password"), True

    return None, False





    



def check_password(password):

    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

    if re.match(pattern, password):
        return True, 'valid password'
    else:
        return False, 'invalid password'



# groq api setup 
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
groq = OpenAI(base_url=GROQ_BASE_URL, api_key=api_key)

# functions used by scraper class

user_prompt_prefix,system_prompt = input_promts() 

def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_prefix + str(website['data'])}
    ]

def summarize(url):
    scrap = Scraper(url)
    website = scrap.fetch_website_contents()
    response = groq.chat.completions.create(
        model = "openai/gpt-oss-20b",
        messages = messages_for(website)
    )
    return response.choices[0].message.content

def display_summary(url):
    summary = summarize(url)
    return summary








class Register(Resource):
    def post(self):

        posted_data = request.get_json()

        username = posted_data["Username"]
        password = posted_data["Password"]


        if existUser(username):
            return jsonify(generate_message(301,"Username already taken!"))

        flag , mssg =  check_password(password)
        if flag:
            

            hashpw = bcrypt.hashpw(password.encode('utf8'),salt=bcrypt.gensalt())

            users.insert_one({
            "Username" : username,
            "Password" : hashpw,
            "Token" : 5
            })

            return jsonify(generate_message(200,"You have successfully registered!"))
        else:
    
            return jsonify(generate_message(301,f"{mssg}+password should match the rules"))

class Summary(Resource):

    def post(self):
            posted_data = request.get_json()
        

            username = posted_data["Username"]
            password = posted_data["Password"]
            url = posted_data["Url"]
            retJson, error = verifyCredentials(username, password)
            if error:
                return jsonify(retJson)
            

             # check tokens
            if countTokens(username) == 0:
                return generate_message(303, "Not enough tokens! please refill")

            if not url:
                return generate_message(400, 'Url not provided')

            try:
             

                token_left = countTokens(username)
                users.update_one(
                {"Username": username},
                {"$set": {"Token": token_left - 1}})
                result = display_summary(url)

                return jsonify(generate_message(200,f'Successfully generated website summary {result}'))

            except:
                return generate_message(400, "Invalid website URL")

                


            


            
    

class Refill(Resource):

    def post(self):

        posted_data = request.get_json()
        username = posted_data["Username"]
        password = posted_data["Admin_Password"]
        amount = posted_data["amount"]

        admin_pw = "123abc"

        if not existUser(username):
            return generate_message(301, 'Invalid Username')

        if password != admin_pw:
            return generate_message(302, 'Incorrect admin password')

        users.update_one(
            {"Username": username},
            {"$set": {"Token": amount}}
        )

        return generate_message(200, 'Refilled')


            




@app.route("/")
def register_page():
    return render_template("register.html")

@app.route("/summary_page")
def summary_page():
    return render_template("summary.html")



api.add_resource(Register,'/register')
api.add_resource(Summary,'/summary')
api.add_resource(Refill,'/refill')

if __name__ == '__main__':
    app.run(debug= True,host='0.0.0.0', port = 5010)

    



        
