"""Слой данных: классы гостя, жилья и бронирования."""


class Guest:
    def __init__(self, name):
        self.id = None
        self.name = name


class Housing:
    def __init__(self, title, capacity, price):
        self.id = None
        self.title = title
        self.capacity = capacity
        self.price = price  # Цена за ночь в целых рублях.


class Booking:
    def __init__(self, guest_id, housing_id, start, end, people, total):
        self.id = None
        self.guest_id = guest_id
        self.housing_id = housing_id
        self.start = start
        self.end = end
        self.people = people
        self.total = total
        self.cancelled = False
