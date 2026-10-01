from datetime import datetime
import json
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for
)


def load_clubs():
    with open('clubs.json') as clubs_file:
        list_of_clubs = json.load(clubs_file)['clubs']
        return list_of_clubs


def load_competitions():
    with open('competitions.json') as competitions_file:
        list_of_competitions = json.load(competitions_file)['competitions']
        return list_of_competitions


def create_app(config=None, competitions=None, clubs=None):
    app = Flask(__name__)

    if config is not None:
        app.config.update(config)

    app.secret_key = 'something_special'

    if competitions is None:
        competitions = load_competitions()

    if clubs is None:
        clubs = load_clubs()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/showSummary', methods=['POST'])
    def show_summary():
        matching_clubs = [
            club
            for club in clubs
            if club['email'] == request.form['email']
        ]

        if not matching_clubs:
            flash('Club not found.')
            return render_template('index.html')

        club = matching_clubs[0]

        future_competitions = [
            competition
            for competition in competitions
            if datetime.strptime(
                competition['date'],
                "%Y-%m-%d %H:%M:%S",
                ) > datetime.now()
        ]

        return render_template(
            'welcome.html',
            club=club,
            competitions=future_competitions
        )

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        found_club = [
            c
            for c in clubs 
            if c['name'] == club
        ][0]

        found_competition = [
            c
            for c in competitions 
            if c['name'] == competition
        ][0]

        if found_club and found_competition:
            return render_template(
                'booking.html',
                club=found_club,
                competition=found_competition
            )
        else:
            flash("Something went wrong-please try again")
            return render_template(
                'welcome.html',
                club=club,
                competitions=competitions
            )

    @app.route('/purchasePlaces', methods=['POST'])
    def purchase_places():
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        places_required = int(request.form['places'])
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - places_required
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)

    # TODO: Add route for points display

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    return app


app = create_app()
