from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        db = connection.cursor().db_conn.client[settings.DATABASES['default']['NAME']]
        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Insert test users
        users = [
            {"name": "Superman", "email": "superman@dc.com", "team": "DC"},
            {"name": "Batman", "email": "batman@dc.com", "team": "DC"},
            {"name": "Wonder Woman", "email": "wonderwoman@dc.com", "team": "DC"},
            {"name": "Iron Man", "email": "ironman@marvel.com", "team": "Marvel"},
            {"name": "Captain America", "email": "cap@marvel.com", "team": "Marvel"},
            {"name": "Black Widow", "email": "widow@marvel.com", "team": "Marvel"},
        ]
        db.users.insert_many(users)

        # Insert teams
        teams = [
            {"name": "Marvel", "members": ["ironman@marvel.com", "cap@marvel.com", "widow@marvel.com"]},
            {"name": "DC", "members": ["superman@dc.com", "batman@dc.com", "wonderwoman@dc.com"]},
        ]
        db.teams.insert_many(teams)

        # Insert activities
        activities = [
            {"user": "superman@dc.com", "activity": "Flight", "duration": 60},
            {"user": "batman@dc.com", "activity": "Martial Arts", "duration": 45},
            {"user": "ironman@marvel.com", "activity": "Suit Training", "duration": 50},
        ]
        db.activities.insert_many(activities)

        # Insert leaderboard
        leaderboard = [
            {"user": "superman@dc.com", "points": 100},
            {"user": "ironman@marvel.com", "points": 90},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Insert workouts
        workouts = [
            {"name": "Strength Training", "suggested_for": ["superman@dc.com", "cap@marvel.com"]},
            {"name": "Agility Drills", "suggested_for": ["batman@dc.com", "widow@marvel.com"]},
        ]
        db.workouts.insert_many(workouts)

        # Ensure unique index on email
        db.users.create_index("email", unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))
