# Импорт библиотек
import threading
from queue import Queue
import time
from random import randint


class Table:
    def __init__(self, number):
        self.number = number  # Номер стола
        self.guest = None  # Гость, сидящий за столом (изначально пусто)


class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name  # Имя гостя

    def run(self):
        # Симуляция времени, которое гость проводит за столом (3-10 секунд)
        time.sleep(randint(3, 10))


class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()  # Очередь гостей, ожидающих столик
        self.tables = list(tables)  # Список всех столов в кафе

    def guest_arrival(self, *guests):
        for guest in guests:
            free_table = None
            # Проверяем, есть ли свободный стол
            for table in self.tables:
                if table.guest is None:  # Стол свободен, можно посадить гостя
                    free_table = table
                    break

            if free_table:
                # Сажаем гостя за стол и запускаем его поток
                free_table.guest = guest
                guest.start()
                print(f"{guest.name} сел(-а) за стол номер {free_table.number}")
            else:
                # Если нет свободных столов, добавляем гостя в очередь
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        # Пока есть гости в очереди или за столами
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                # Если за столом сидит гость и он закончил приём пищи
                if table.guest and not table.guest.is_alive():
                    print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    table.guest = None  # Освобождаем стол

                # Если есть гости в очереди и стол свободен
                if table.guest is None and not self.queue.empty():
                    next_guest = self.queue.get()  # Берём следующего гостя из очереди
                    table.guest = next_guest  # Сажаем за стол
                    next_guest.start()  # Запускаем поток гостя
                    print(f"{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")

            time.sleep(1)  # Пауза перед следующей проверкой


# Создание столов
tables = [Table(number) for number in range(1, 6)]  # 5 столов с номерами 1-5
# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
