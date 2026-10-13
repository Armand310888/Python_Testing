from itertools import cycle
from random import randint
from locust import HttpUser, task, between

club_numbers = cycle(range(1, 11))


class GudlftUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        club_number = next(club_numbers)
        self.club_name = f'Performance Club {club_number}'
        self.club_email = f'club{club_number}@example.com'

        self.competition_numbers = cycle(range(1, 11))

    @task(1)
    def view_home(self):
        self.client.get('/')

    @task(3)
    def view_competitions(self):
        self.client.post(
            '/showSummary',
            data={'email': self.club_email}
        )

    @task(1)
    def view_booking(self):
        competition_number = randint(1, 10)
        competition_name = f'Performance Competition {competition_number}'

        self.client.get(
            f'/book/{competition_name}/{self.club_name}',
            name="/book/[competition]/[club]"
        )

    @task(3)
    def view_clubs_points(self):
        self.client.get('/clubs')

    @task(1)
    def purchase_places(self):
        competition_number = next(self.competition_numbers)
        competition_name = f'Performance Competition {competition_number}'

        with self.client.post(
            '/purchasePlaces',
            data={
                'club': self.club_name,
                'competition': competition_name,
                'places': 1
            },
            catch_response=True,
        ) as response:

            if 'Great-booking complete!' in response.text:
                response.success()
            else:
                response.failure('Booking rejected')
