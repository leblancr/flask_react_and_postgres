from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS, cross_origin
from flask_pymongo import PyMongo

app = Flask(__name__)

# Configure PostgreSQL (SQLAlchemy)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rich:admin@localhost/baby-tracker'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rich:reddpos@localhost/baby-tracker'  # must use '%40' to replace @ sign
db = SQLAlchemy(app)
# db.init_app(app)  # first time only
CORS(app)  #

# Configure MongoDB (Flask-PyMongo)
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/baby-tracker'
# app.config['MONGO_URI'] = 'mongodb://rich:reddmon@localhost:27017/baby-tracker'
app.config['MONGO_URI'] = 'mongodb+srv://rkba1:Hiu55xZe0buUedBd@cluster0.yymy7y6.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

mongo = PyMongo(app)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Event: {self.description}"
    
    def __init__(self, description):
        self.description = description
        
    # run just once to create event table
    # with app.app_context():
    #     db.create_all()
        
        
def format_event(event):
    return {
        "description": event.description,
        "id": event.id,
        "created_at": event.created_at
    }
        

@app.route('/')
def hello():
    return 'hello'


# create an event
@app.route('/events', methods=['POST'])
def create_event():
    description = request.json['description']

    # Save to SQLAlchemy (PostgreSQL)
    event_sql = Event(description)
    db.session.add(event_sql)
    db.session.commit()

    # Save to MongoDB (Flask-PyMongo)
    events_mongo = mongo.db.events
    inserted_event = events_mongo.insert_one({
        "description": description,
        "created_at": datetime.utcnow()
    })

    # Return response
    return jsonify({
        "description_sql": event_sql.description,
        "id_sql": event_sql.id,
        "created_at_sql": event_sql.created_at,
        "description_mongo": description,
        "id_mongo": str(inserted_event.inserted_id),  # Convert ObjectId to string
        "created_at_mongo": datetime.utcnow().isoformat()  # Or use the actual timestamp from MongoDB
    }), 201


# get all events
@app.route('/events', methods=['GET'])
@cross_origin(origin='http://localhost:3000', methods=['GET'])
def get_events():
    # Fetch events from PostgreSQL
    events_sql = Event.query.order_by(Event.id.asc()).all()
    event_list_sql = [format_event(event) for event in events_sql]

    # mongo doesnt do CORS
    # Fetch events from MongoDB
    #events_mongo = list(mongo.db.events.find())
    # event_list_mongo = [{
    #     "description": event['description'],
    #     "id": str(event['_id']),  # Convert ObjectId to string
    #     "created_at": event['created_at'].isoformat()  # Convert datetime to ISO format
    # } for event in events_mongo]

    # Combine both lists
    combined_event_list = event_list_sql  # + event_list_mongo

    return jsonify({"events": combined_event_list})
    #return {"events": event_list}
        

# get one event
@app.route('/events/<event_id>', methods=['GET'])
def get_event(event_id):
    event = Event.query.filter_by(id=event_id).one()
    return {'event': format_event(event)}
    
    
# delete event
@app.route('/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = Event.query.filter_by(id=event_id).one()
    db.session.delete(event)
    db.session.commit()
    return f"Event: (id: {id}) deleted"


# edit event (update)
@app.route('/events/<event_id>', methods=['PUT'])
def update_event(event_id):
    event = Event.query.filter_by(id=event_id)
    description = request.json['description']
    event.update(dict(description=description, created_at=datetime.utcnow()))
    db.session.commit()
    return {'event': format_event(event.one())}


if __name__ == '__main__':
    app.run(debug=True)
    