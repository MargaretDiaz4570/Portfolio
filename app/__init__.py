import os
from flask import Flask, render_template, request
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
    properties = ['name', 'email', 'content']
    receivedProperties = request.form.keys()
    emailRE = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$' # Check if is a valid email

    for key in properties:
        if key not in receivedProperties:
            return f'Invalid {key}', 400
        else:
            if request.form[key] == '':
                return f'Invalid {key}', 400
            if key == 'email' and re.search(emailRE, request.form['email']) == None:
                return 'Invalid email', 400
            
    try:
        name = request.form['name']
        email = request.form['email']
        content = request.form['content']
        timeline_post = TimelinePost.create(name=name, email=email, content=content)

        return model_to_dict(timeline_post)
    except Exception as e:
       print('\n\n--> ERROR: ', e, '\n\n')
       return 'An error happened while creating the post, please try again'

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in
            TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

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
    {"imgSource": "/static/img/podcast.jpg",
    "name": "True Crime Podcasts", 
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."},
    {"imgSource": "/static/img/soccer.jpg", 
    "name": "Soccer", 
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."},
    {"imgSource": "/static/img/travel.jpg", 
    "name": "Traveling", 
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."},
    {"imgSource": "/static/img/garden.jpg", 
    "name": "Gardening", 
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit."}
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
#if __name__ == "__main__":
#    app.run()