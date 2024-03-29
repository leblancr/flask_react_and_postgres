from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rich:admin@localhost/baby-tracker'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rich:reddpos@localhost/baby-tracker'  # must use '%40' to replace @ sign
db = SQLAlchemy(app)
# db.init_app(app)  # first time only
CORS(app)  #


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
    event = Event(description)
    db.session.add(event)
    db.session.commit()
    # return format_event(event)
    return {
        "description": event.description,
        "id": event.id,
        "created_at": event.created_at
    }


# get all event
@app.route('/events', methods=['GET'])
def get_events():
    events = Event.query.order_by(Event.id.asc()).all()
    event_list = []
    for event in events:
        event_list.append(format_event(event))
    return {"events": event_list}
        

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
    