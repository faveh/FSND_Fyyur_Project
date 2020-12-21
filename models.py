from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
import datetime

db = SQLAlchemy()


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    website = db.Column(db.String(120))
    genres = db.Column(db.String)
    venue = db.relationship('Show', backref=db.backref('venue', cascade='all, delete'), lazy=True)

    def __repr__(self):
        return '<Venue {}>'.format(self.name)

    @property
    def venue_details(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'address': self.address,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
            'genres': self.genres.split(','),
            'website': self.website
        }

    @property
    def get_venue_with_number_of_upcoming_show(self):
        num_shows = Show.query.filter(Show.start_time > datetime.datetime.now(), Show.venue_id == self.id)
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'address': self.address,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'website': self.website,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
            'num_shows': num_shows
        }

    @property
    def get_venue_with_show_details(self):
        upcoming_shows = Show.query.filter(Show.start_time > datetime.datetime.now(), Show.venue_id == self.id).all()
        upcoming_shows_with_artist_venue = [show.show_with_artist_venue for show in upcoming_shows]

        past_shows = Show.query.filter(Show.start_time < datetime.datetime.now(), Show.venue_id == self.id).all()
        past_shows_with_artist_venue = [show.show_with_artist_venue for show in past_shows]
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'address': self.address,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
            'website': self.website,
            'upcoming_shows': upcoming_shows_with_artist_venue,
            'past_shows': past_shows_with_artist_venue,
            'upcoming_shows_count': len(upcoming_shows),
            'past_shows_count': len(past_shows),
            'genres': self.genres.split(','),
        }

    @property
    def group_venue_by_city_state(self):
        venues = Venue.query.filter(Venue.city == self.city, Venue.state == self.state).all()
        grouped_venues = [venue.get_venue_with_number_of_upcoming_show for venue in venues]
        return {
            'city': self.city,
            'state': self.state,
            'venues': grouped_venues
        }

# ---------------- CRUD methods --------------#
    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    genres = db.Column(db.String(120))
    artist = db.relationship('Show', backref=db.backref('artist', cascade='all, delete'), lazy=True)

    def __repr__(self):
        return '<Artist {}>'.format(self.name)

    @property
    def artist_details(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'genres': self.genres.split(','),
            'website': self.website
        }

    @property
    def get_artist_with_show_details(self):
        upcoming_shows = Show.query.filter(Show.start_time > datetime.datetime.now(), Show.artist_id == self.id).all()
        upcoming_shows_with_artist_venue = [show.show_with_artist_venue for show in upcoming_shows]

        past_shows = Show.query.filter(Show.start_time < datetime.datetime.now(), Show.artist_id == self.id).all()
        past_shows_with_artist_venue = [show.show_with_artist_venue for show in past_shows]
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'genres': self.genres.split(','),
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'website': self.website,
            'upcoming_shows': upcoming_shows_with_artist_venue,
            'past_shows': past_shows_with_artist_venue,
            'upcoming_shows_count': len(upcoming_shows),
            'past_shows_count': len(past_shows)
        }

# ---------------- CRUD methods --------------#
    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime())
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)

    def __repr__(self):
        return '<Show {}{}>'.format(self.artist_id, self.venue_id)

# ---------------- CRUD methods --------------#
    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def show_details(self):
        return {
            'id': self.id,
            'start_time': self.start_time.strftime("%m/%d/%Y, %H:%M:%S"),
            'venue_id': self.venue_id,
            'artist_id': self.artist_id
        }

    @property
    def show_with_artist_venue(self):
        venues = Venue.query.filter(Venue.id == self.venue_id).one()
        venue = venues.venue_details

        artists = Artist.query.filter(Artist.id == self.artist_id).one()
        artist = artists.artist_details
        return {
            'id': self.id,
            'start_time': self.start_time.strftime("%m/%d/%Y, %H:%M:%S"),
            'venue': venue,
            'artist': artist,
        }