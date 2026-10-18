
from dataclasses import dataclass

@dataclass
class Movie:

    movie_name : str
    total_seats : int
    ticket_price : float
    booked_seats : int = 0

    def book_ticket(self, requested_seats: int):
        if self.booked_seats + requested_seats > self.total_seats:
            raise Exception(f"Sorry, {requested_seats = } not available.")

        self.booked_seats += requested_seats

        bill_amount = self.ticket_price * requested_seats
        return f"Seats available, please pay {bill_amount} to confirm"

    def show_status(self):
        return f"""Movie: {self.movie_name}, 
        {self.booked_seats} out of {self.total_seats} available, 
        ticket price: {self.ticket_price}"""

movie = Movie("Street Fighter", 200, 400.0)

print(movie.show_status())

print(movie.book_ticket(2))
print(movie.show_status())

movie2 = Movie("Drishyam3", 2, 400.0)
movie2.book_ticket(3)