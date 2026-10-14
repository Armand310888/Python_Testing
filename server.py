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


def find_club(club_identifier, search_field, clubs):
    return next(
        (
            club
            for club in clubs
            if club[search_field] == club_identifier
        ),
        None
    )


def find_competition(competition_name, competitions):
    return next(
        (
            competition
            for competition in competitions
            if competition['name'] == competition_name
        ),
        None
    )


def get_future_competitions(competitions):
    return [
        competition
        for competition in competitions
        if (
            datetime.strptime(
                competition['date'],
                "%Y-%m-%d %H:%M:%S",
            )
            > datetime.now()
        )
    ]


def get_booking(
    club,
    competition,
    bookings
):
    for booking in bookings:
        if (
            booking['club'] == club['name']
            and booking['competition'] == competition['name']
        ):
            return booking

    return None


def get_places_booked_for_competition(
    club,
    competition,
    bookings
):
    booking = get_booking(club, competition, bookings)

    if booking is None:
        return 0

    return booking['places']


def validate_booking(
    places_required,
    club_points,
    competition_places,
    bookings,
    club,
    competition,
):
    if places_required <= 0:
        return 'Error-Number of Places must be positive!'
    
    if places_required > club_points:
        return 'Error-Club does not have enough points!'

    places_already_booked = get_places_booked_for_competition(
        club,
        competition,
        bookings,
    )

    if places_required + places_already_booked > 12:
        return 'Error-Cannot book more than 12 places for one competition!'

    if places_required > competition_places:
        return 'Error-Competition does not have enough available places!'

    return None


def update_booking(
    club,
    competition,
    places_required,
    bookings,
):
    booking = get_booking(club, competition, bookings)

    if booking:
        booking['places'] += places_required
    else:
        booking = {
            'club': club['name'],
            'competition': competition['name'],
            'places': places_required
        }
        bookings.append(booking)


def update_competition_places(competition, purchased_places):
    competition['number_of_places'] = (
        int(competition['number_of_places'])
        - purchased_places
    )


def update_club_points(club, purchased_places):
    club['points'] = (
        int(club['points'])
        - purchased_places
    )


def create_app(
        config=None,
        competitions=None,
        clubs=None,
        bookings=None
):
    app = Flask(__name__)

    if config is not None:
        app.config.update(config)

    app.secret_key = 'something_special'

    if competitions is None:
        competitions = load_competitions()

    if clubs is None:
        clubs = load_clubs()

    if bookings is None:
        bookings = []

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/show-summary', methods=['POST'])
    def show_summary():
        club = find_club(request.form.get('email'), 'email', clubs)

        if not club:
            flash('Error-Club not found.')
            return render_template('index.html')

        future_competitions = get_future_competitions(competitions)

        return render_template(
            'welcome.html',
            club=club,
            competitions=future_competitions
        )

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        matching_club = find_club(club, 'name', clubs)

        if not matching_club:
            flash('Error-Club not found.')
            return render_template(
                'index.html'
            )

        future_competitions = get_future_competitions(
            competitions
        )

        matching_competition = find_competition(
            competition,
            future_competitions
        )

        if not matching_competition:
            flash('Error-Competition not found.')
            return render_template(
                'welcome.html',
                club=matching_club,
                competitions=future_competitions
            )

        return render_template(
            'booking.html',
            club=matching_club,
            competition=matching_competition
        )

    @app.route('/purchase-places', methods=['POST'])
    def purchase_places():
        future_competitions = get_future_competitions(competitions)

        competition = find_competition(
            request.form.get('competition'), future_competitions
        )

        club = find_club(request.form.get('club'), 'name', clubs)

        if not club:
            flash('Error-Club not found.')
            return render_template('index.html')

        if not competition:
            flash('Error-Competition not found.')
            return render_template(
                'welcome.html',
                club=club,
                competitions=future_competitions
            )

        try:
            places_required = int(request.form.get('places'))
        except (ValueError, TypeError):
            flash('Error-Invalid number of places!')
            return render_template(
                'welcome.html',
                club=club,
                competitions=future_competitions
            )

        club_points = int(club['points'])
        competition_places = int(competition['number_of_places'])

        validation_message = validate_booking(
            places_required,
            club_points,
            competition_places,
            bookings,
            club,
            competition
        )

        if validation_message:
            flash(validation_message)
            return render_template(
                'welcome.html',
                club=club,
                competitions=future_competitions
            )

        update_booking(club, competition, places_required, bookings)

        update_competition_places(competition, places_required)

        update_club_points(club, places_required)

        flash('Success-Booking complete!')
        return render_template(
            'welcome.html',
            club=club,
            competitions=future_competitions
        )

    @app.route('/clubs')
    def display_clubs_points():
        return render_template(
            'clubs.html',
            clubs=clubs
        )

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    return app


app = create_app()
