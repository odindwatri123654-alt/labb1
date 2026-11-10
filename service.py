"""Слой бизнес-логики: проверки, расчёт цены и отмена брони."""
from datetime import date

from models import Booking, Guest, Housing


class BookingService:
    def __init__(self, guests, housing, bookings):
        self.guests = guests
        self.housing = housing
        self.bookings = bookings

    def add_guest(self, name):
        name = name.strip()
        if not name:
            raise ValueError("Имя не должно быть пустым.")
        return self.guests.add(Guest(name))

    def add_housing(self, title, capacity, price):
        title = title.strip()
        if not title or capacity <= 0 or price <= 0:
            raise ValueError("Укажите название, положительную вместимость и цену.")
        return self.housing.add(Housing(title, capacity, price))

    def get_guests(self):
        return self.guests.get_all()

    def get_housing(self):
        return self.housing.get_all()

    def get_bookings(self):
        return self.bookings.get_all()

    def book(self, guest_id, housing_id, start, end, people):
        self.guests.get(guest_id)
        house = self.housing.get(housing_id)
        if start < date.today() or end <= start:
            raise ValueError("Заезд — не в прошлом, выезд — позже заезда.")
        if people <= 0 or people > house.capacity:
            raise ValueError("Число гостей должно быть от 1 до вместимости жилья.")

        for booking in self.bookings.get_all():
            # Выезд и следующий заезд в один день не считаются пересечением.
            if (booking.housing_id == housing_id and not booking.cancelled
                    and start < booking.end and booking.start < end):
                raise ValueError("Жильё занято на эти даты.")

        nights = (end - start).days
        total = nights * house.price
        return self.bookings.add(Booking(guest_id, housing_id, start, end, people, total))

    def cancel(self, booking_id):
        booking = self.bookings.get(booking_id)
        if booking.cancelled:
            raise ValueError("Бронирование уже отменено.")
        booking.cancelled = True
        self.bookings.update(booking)

    def delete_housing(self, housing_id):
        self.housing.get(housing_id)
        for booking in self.bookings.get_all():
            if booking.housing_id == housing_id:
                raise ValueError("Нельзя удалить жильё с историей бронирований.")
        self.housing.delete(housing_id)
