import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from peewee import * 
from playhouse.shortcuts import model_to_dict
from datetime import datetime
import re

load_dotenv()
app = Flask(__name__)

if os.getenv('TESTING') == 'true':
    print('Running in test mode')
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv('MYSQL_DATABASE'), 
        user=os.getenv('MYSQL_USER'), 
        password=os.getenv('MYSQL_PASSWORD'), 
        host=os.getenv('MYSQL_HOST'), 
        port=3306
    )

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])
print(mydb)

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    try:
        data = request.get_json()
        name = data['name']
        email = data['email']
        content = data['content']
            
        timeline_post = TimelinePost.create(name=name, email=email, content=content)

        return jsonify(model_to_dict(timeline_post))
    except Exception as e:
        print('\n\n--> ERROR: ', e, '\n\n')
        return 'An error happened while creating the post, please try again', 400
    
@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in
            TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

@app.route('/api/timeline_post', methods=['DELETE'])
def delete_time_line_post():
    try:

        post_id = request.args.get('post_id')
        if not post_id:
            return 'Missing post_id parameter', 400

        timeline_post = TimelinePost.get(TimelinePost.id == post_id)
        timeline_post.delete_instance()

        return 'Timeline post deleted successfully'
    except Exception as e:
        print('\n\n--> ERROR: ', e, '\n\n')
        return 'An error occurred while deleting the post', 500
    
#/work / experience / education / places we visited
# updated flask routes

@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

workData = [
    {
        "title": "Production Engineering Intern",
        "employer": "MHL Fellowship",
        "date": "June 2023 - Present",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    },
    {   
        "title": "Software Engineering Intern",
        "employer": "Meta",
        "date": "June 2022 - September 2022", 
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    },
    {   
        "title": "Participant",
        "employer": "MHL Hackaton",
        "date": "June 2022",
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    },
    {
        "title": "President",
        "employer": "The Club",
        "date": "Oct 2021 - May 2022", 
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
    }
]

@app.route('/Work')  # Define the route for /Work
def Work():
    context ={
        "workData": workData
    }
    return render_template('Work.html', title="Work", url=os.getenv("URL"), **context)

# Hobbies data
hobbyData = [
    {"imgSource": "/static/img/bitly.png",
    "name": "Bitly API Explorer Page", 
    "description": "Designed and developed an easier space for users to interact with HTTP Request Methods from the Bitly API."},
    {"imgSource": "/static/img/MLH-logo-2.png", 
    "name": "MLH Weather App", 
    "description": "Created a weather app using Opensource weather and Google Maps API"},
    {"imgSource": "/static/img/github.png", 
    "name": "Drawing with Turtles", 
    "description": "Created an interactive drawing pad using the python turtle library"}
]

@app.route('/Hobbies')  # Define the route for /Hobbies
def Hobbies():
    context = {
        "hobbyData": hobbyData
    }
    return render_template('Hobbies.html', title="Hobbies", url=os.getenv("URL"), **context)

@app.route('/Locations')  # Define the route for /Map
def Map():
    return render_template('Locations.html', title="Location", url=os.getenv("URL"))

@app.route('/Timeline')
def Timeline():
    return render_template('Timeline.html', title="Timeline", url=os.getenv("URL"))

@app.route('/ThankYou')  
def ThankYou():
    return render_template('ThankYou.html', title="ThankYou", url=os.getenv("URL"))

@app.route('/Post')  
def Post():
    return render_template('Post.html', title="Post", url=os.getenv("URL"))
