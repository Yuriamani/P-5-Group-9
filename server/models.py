from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
import datetime

db = SQLAlchemy()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)  # New field for admin check
    is_active = db.Column(db.Boolean, default=True)  # Optional field for deactivating accounts

    user_events = db.relationship('UserEvent', backref='user')
    feedback = db.relationship('Feedback', backref='user')

    serialize_only = ('id', 'email', 'username', 'is_admin', 'is_active')
    exclude = ('user_events', 'feedback', 'password_hash')

    def __repr__(self):
        return f'<User {self.id}, {self.username}, is_admin={self.is_admin}, is_active={self.is_active}>'

class Event(db.Model, SerializerMixin):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    location = db.Column(db.Text, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    number_of_tickets = db.Column(db.Integer, nullable=False)  # New field

    user_events = db.relationship('UserEvent', backref='event')
    feedback = db.relationship('Feedback', backref='event')
    tickets = db.relationship('Ticket', backref='event')
    event_organizers = db.relationship('EventOrganizer', backref='event')

    serialize_only = ('id', 'image', 'name', 'datetime', 'location', 'capacity', 'description', 'number_of_tickets')
    exclude = ('user_events', 'feedback', 'tickets', 'event_organizers')

    def __repr__(self):
        return f'<Event {self.id}, {self.name}>'

class UserEvent(db.Model, SerializerMixin):
    __tablename__ = 'user_events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    serialize_only = ('id', 'user_id', 'event_id')
    exclude = ('user', 'event')

    def __repr__(self):
        return f'<UserEvent {self.id}, user_id={self.user_id}, event_id={self.event_id}>'

class Feedback(db.Model, SerializerMixin):
    __tablename__ = 'feedbacks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    feedback = db.Column(db.Text, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    serialize_only = ('id', 'feedback', 'event_id', 'user_id')
    exclude = ('user', 'event')

    def __repr__(self):
        return f'<Feedback {self.id}, feedback={self.feedback}, event_id={self.event_id}, user_id={self.user_id}>'

class Ticket(db.Model, SerializerMixin):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.Float, nullable=False)
    ticket_number = db.Column(db.String, unique=True, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    serialize_only = ('id', 'price', 'ticket_number', 'event_id')
    exclude = ('event',)

    def __repr__(self):
        return f'<Ticket {self.id}, price={self.price}, ticket_number={self.ticket_number}, event_id={self.event_id}>'

class EventOrganizer(db.Model, SerializerMixin):
    __tablename__ = 'event_organizers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    organizer_name = db.Column(db.String, nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    serialize_only = ('id', 'organizer_name', 'event_id')
    exclude = ('event',)

    def __repr__(self):
        return f'<EventOrganizer {self.id}, organizer_name={self.organizer_name}, event_id={self.event_id}>'