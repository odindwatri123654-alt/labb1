"""Точка входа: создание объектов и консольное меню."""
from datetime import datetime

from repository import Repository
from service import BookingService


def main():
    service = BookingService(Repository(), Repository(), Repository())
    print("Бронирование жилья. Данные хранятся до выхода из программы.")

    while True:
        print("\n1. Добавить гостя\n2. Список гостей\n3. Добавить жильё"
              "\n4. Список жилья\n5. Забронировать\n6. Список бронирований"
              "\n7. Отменить бронирование\n8. Удалить жильё\n0. Выход")
        try:
            action = input("Выберите действие: ").strip()
            if action == "0":
                break
            elif action == "1":
                guest = service.add_guest(input("Имя гостя: "))
                print("Гость добавлен. Номер:", guest.id)
            elif action == "2":
                guests = service.get_guests()
                if not guests:
                    print("Гостей пока нет.")
                for guest in guests:
                    print(f"{guest.id}. {guest.name}")
            elif action == "3":
                title = input("Название жилья: ")
                capacity = int(input("Количество мест: "))
                price = int(input("Цена за ночь (целые рубли): "))
                house = service.add_housing(title, capacity, price)
                print("Жильё добавлено. Номер:", house.id)
            elif action == "4":
                houses = service.get_housing()
                if not houses:
                    print("Жилья пока нет.")
                for house in houses:
                    print(f"{house.id}. {house.title}, мест: {house.capacity}, "
                          f"цена: {house.price} руб./ночь")
            elif action == "5":
                guest_id = int(input("Номер гостя: "))
                housing_id = int(input("Номер жилья: "))
                start = datetime.strptime(input("Заезд (ДД-ММ-ГГГГ): ").strip(), "%d-%m-%Y").date()
                end = datetime.strptime(input("Выезд (ДД-ММ-ГГГГ): ").strip(), "%d-%m-%Y").date()
                people = int(input("Количество гостей: "))
                booking = service.book(guest_id, housing_id, start, end, people)
                print(f"Бронь №{booking.id}. Стоимость: {booking.total} руб.")
            elif action == "6":
                bookings = service.get_bookings()
                if not bookings:
                    print("Бронирований пока нет.")
                for booking in bookings:
                    status = "отменено" if booking.cancelled else "забронировано"
                    print(f"№{booking.id}: гость №{booking.guest_id}, "
                          f"жильё №{booking.housing_id}, {booking.start:%d-%m-%Y} — {booking.end:%d-%m-%Y}, "
                          f"гостей: {booking.people}, {booking.total} руб., {status}")
            elif action == "7":
                service.cancel(int(input("Номер бронирования: ")))
                print("Бронирование отменено.")
            elif action == "8":
                service.delete_housing(int(input("Номер жилья: ")))
                print("Жильё удалено.")
            else:
                print("Такого пункта нет.")
        except ValueError as error:
            print("Ошибка:", error)
        except (KeyboardInterrupt, EOFError):
            print("\nВыход.")
            break


if __name__ == "__main__":
    main()
