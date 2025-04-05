import pickle 
import shelve  
import json  

class InvalidShootData(Exception):
    pass


class Weapon:
    def __init__(self, name, hit_percentage):
        assert isinstance(name, str), ("Ім'я має бути рядком")
        assert 0 <= hit_percentage <= 100, ("Точність має бути від 0 до 100")
        self.name = name
        self.hit_percentage = hit_percentage

    def __str__(self):
        return f"{self.name} - {self.hit_percentage}%"

    def __repr__(self):
        return f"Weapon('{self.name}', {self.hit_percentage})"

class Shooting(Weapon):
    def __init__(self, name, hit_percentage, shot_count):
        super().__init__(name, hit_percentage)
        if shot_count < 0:
            raise InvalidShootData("Кількість пострілів не може бути від'ємною")
        self.shot_count = shot_count

    def hit_probability(self):
        return (self.hit_percentage / 100) * self.shot_count

    def __lt__(self, other):
        return self.shot_count < other.shot_count

    def __repr__(self):
        return f"Shooting('{self.name}', {self.hit_percentage}, {self.shot_count})"

class ShootingList:
    def __init__(self):
        self.shoot_list = []

    def add_shoot(self, shoot):
        if not isinstance(shoot, Shooting):
            raise TypeError("Можна додавати лише об'єкти класу Shooting")
        self.shoot_list.append(shoot)

    def save_pickle(self, filename):
        try:
            with open(filename, 'wb') as f:
                pickle.dump(self.shoot_list, f)
        except Exception as e:
            print(f"Помилка збереження у pickle: {e}")

    def load_pickle(self, filename):
        try:
            with open(filename, 'rb') as f:
                self.shoot_list = pickle.load(f)
        except FileNotFoundError:
            print("Файл pickle не знайдено.")
        except Exception as e:
            print(f"Помилка завантаження з pickle: {e}")

    def save_shelve(self, filename):
        try:
            with shelve.open(filename) as db:
                db['shoot_list'] = self.shoot_list
        except Exception as e:
            print(f"Помилка збереження у shelve: {e}")

    def load_shelve(self, filename):
        try:
            with shelve.open(filename) as db:
                self.shoot_list = db.get('shoot_list', [])
        except Exception as e:
            print(f"Помилка завантаження з shelve: {e}")

    def save_text(self, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for shoot in self.shoot_list:
                    f.write(repr(shoot) + '\n')
        except Exception as e:
            print(f"Помилка збереження у текстовий файл: {e}")

    def load_text(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.shoot_list = [eval(line.strip()) for line in f]
        except FileNotFoundError:
            print("Текстовий файл не знайдено.")
        except SyntaxError:
            print("Невірні дані у текстовому файлі.")
        except Exception as e:
            print(f"Помилка завантаження з тексту: {e}")

    def save_json(self, filename):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump([shoot.__dict__ for shoot in self.shoot_list], f)
        except Exception as e:
            print(f"Помилка збереження у JSON: {e}")

    def load_json(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.shoot_list = [Shooting(**item) for item in data]
        except FileNotFoundError:
            print("Файл JSON не знайдено.")
        except json.JSONDecodeError:
            print("Неправильний формат JSON.")
        except Exception as e:
            print(f"Помилка завантаження з JSON: {e}")

if __name__ == "__main__":
    shooting_list = ShootingList()

    try:
        shooting_list.add_shoot(Shooting("Pistol", 70, 10))
        shooting_list.add_shoot(Shooting("Sniper Rifle", 90, 5))
    except InvalidShootData as e:
        print(f"Спеціальна помилка: {e}")
    except Exception as e:
        print(f"Неочікувана помилка при додаванні стрільб: {e}")
    else:
        print("Стрільби успішно додані.")
    finally:
        print("Початкове налаштування завершено.")

    shooting_list.save_pickle("shooting.pkl")
    shooting_list.load_pickle("shooting.pkl")

    shooting_list.save_shelve("shooting_shelve")
    shooting_list.load_shelve("shooting_shelve")

    shooting_list.save_text("shooting.txt")
    shooting_list.load_text("shooting.txt")

    shooting_list.save_json("shooting.json")
    shooting_list.load_json("shooting.json")

    print("\nФінальний список стрільб:")
    for shoot in shooting_list.shoot_list:
        print(shoot)
