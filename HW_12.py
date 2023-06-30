""" ДЗ12
"""
from collections import UserDict
from typing import List
from datetime import datetime
import re
import pickle
import json

class AdressBook(UserDict):

    def __init__(self):
        self.current_value = 0
        super().__init__()  
    def __iter__(self):
        return self

    def __next__(self):
        if self.current_value < len(self.data):
            self.current_value += 1
            l1 = []
            for i in self.data:
                l1.append(i)
            return f'{self.current_value}: \
{l1[self.current_value-1]} - {self.data[l1[self.current_value-1]]}'
        raise StopIteration

    def first(self):
        self.current_value = 0
        
    def iterator(self, items = 2):
        
        while True:
            print("Нова страниця")
            j = 0
            for i in self:
                yield(i)
                j += 1
                if j == items:
                    break
            if self.current_value == len(self.data) :
                print("Кінець книги")
                break

    def find_info(self, fs:"строка для пошуку не менше 3 символів" = ""):

        if len(fs) >= 3:
            print("Результат вашого пошуку")
            cnt = 0
            for key, rec in self.data.items():
                if fs in key:
                    cnt += 1
                    print(f'№{cnt}: ', key, rec)
                for it in rec.phones:
                    if fs in it.phone:
                        cnt += 1
                        print(f'№{cnt}: ', key, rec)
                        break
        else:
            print('Пошук по одному або двум символа - дурниця. Задайте 3 та більше')
    
    def add_record(self,  rec):
        if isinstance(rec, Record):
            self.data.update({rec.name.value:rec})
        else:
            print("Додати можно тільки об'єкт класу Record")

    def del_record(self, rec):

            if isinstance(rec, Record):
                l1 = self.data.keys() 
                if rec.name.value in l1:
                    self.data.pop(rec.name.value)
                else:
                    print("Запис з таким ім'ям відсутній")
            else:
                print("Метод приймає тільки об'єкти класа Record")
        
    def save_to_file(self, choise:'pickle - p json - j' = 'p',
                     filename = "rezerv.dat"):
        if (choise == 'p') or (choise == 'j'):
            if choise == 'j':
                filename = "reserv.json"          
                with open(filename, "wb") as file:
                    json.dump(self, file)         
            else:
                with open(filename, "wb") as file:
                    pickle.dump(self, file)
        else:
            print("Оберіть p для pickle або json")

    def restore_from_file(self, filename = "rezerv.dat"):

        with open(filename, "rb") as file:
            unpd = pickle.load(file)
            return unpd



class Field:  
                   
    __VAL = ''     
                   
    def __init__(self):
        self.__fvalue = Field.__VAL

    @property
    def fvalue(self):
        return self.__fvalue

    @fvalue.setter
    def fvalue(self, n_value):
        self.__fvalue = n_value


class Name(Field):

    def __init__(self, name):
        self.value = name


class Phone(Field):
    def __init__(self, phone):
        self.__phone = None
        self.phone = phone

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone):
        if re.search(r"^\+\([0-9]{3}\)[0-9]{9}$", phone) != None:
            self.__phone = phone
            print("Номер коректен")
        else:
            self.__phone = ""
            print("Задайте номер телефону у вигляди строки +(xxx)xxxxxxxxх   ")

    def __eq__(self, __o: object) -> bool:
        if self.phone == __o.phone:
            return True
        return False


class Birthday:

    def __init__(self):
        self.__value = ''

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if type(new_value) == str: 
            try:
                brt = datetime.strptime(new_value, '%d.%m.%Y')
                self.__value = new_value
                print("Дата дня народження коректна")
            except:
                print("Задайте дату ДР у вигляді строки  dd.mm.YYYY")
        else:
            print("Дата ДР не задана")
            

class Record:
    def __init__(self, name: Name, phones: List[Phone] = [], birthday: Birthday = Birthday()):
        self.name = name
        self.phones = phones
        self.birthday = birthday

    def add_phone(self, p:Phone) -> bool:

        if isinstance(p, Phone) and (p.phone != None):
            self.phones.append(p)
            print("Об'єкт з телефоном додано")
            return True
        else:
            print("Створіть номер как об'єкт класу Phone(телефон)")

    def del_phone(self, p:Phone):

        if len(self.phones) >= 1:
            if isinstance(p, Phone) and (p.phone != None):
                for i in self.phones:
                    del_nmb = False       
                    if i.phone == p.phone:
                        self.phones.remove(i)
                        del_nmb = True
                        break
                if del_nmb == True:
                    print("Номер виделено")
                else:
                    print("Співпадіння з заданим номером не знайдено")
            else:
                print("Метод приймає об'єкт класа Phone")

        else:
            print("Список номерів пуст")

    def change_phone(self, p:Phone, pn:Phone):

        if (isinstance(p, Phone) and isinstance(pn, Phone) and
           (p.phone != None) and (pn.phone != None)):
            for i in self.phones:
                if i.phone == p.phone:
                    i.phone = pn.phone
                    print("Обраний номер змінено")
                    break
                else:
                    print("Обраний номер не найдено, додайте номер через метод add_phone")
        else:
            print("Створіть номер як об'єкт класа Phone")

    def days_to_birthday(self):

        if self.birthday.value != None:
            current_datetime = datetime.now()  # текущая дата
            current_year = current_datetime.year # текущий год
            brt = self.birthday.value[0:6]  # день и месяц ДР
            brt = brt + str(current_year)  # ДР в текущем году
            brt_this_year = datetime.strptime(brt, '%d.%m.%Y')
            dif_day = brt_this_year - current_datetime
            if dif_day.days > 0 :
                print(f"До дня народження {self.name.value} залишилось {dif_day.days} дней")
            else:
                print(f"ДР у цьому році вже було {abs(dif_day.days)} дней назад")
        else:
            print("Задайте ДР")

    def __str__(self) -> str:
        return (
            f"{self.name.value} : {', '.join([phone.phone for phone in self.phones])}"
        )


def main():
    print("Домашка")
    Ivan = Record(Name("Gena"))
    phone1 = Phone("+(380)975158711")
    phone2 = Phone("+(380)962331122")
    phone3 = Phone("+(380)734343222")
    Ivan.add_phone(phone1)
    Ivan.add_phone(phone2) 
    Ivan.add_phone(phone3)
    bd_Voli = Birthday()
    bd_Voli.value = "31.03.1983"
    Voli = Record(Name("Voli"), [Phone("+(380)449094422"), Phone("+(380)735158711")], bd_Voli)
    print(Ivan)
    print(Voli)
    Voli.days_to_birthday()
    Boris1 = Record(Name("Boris1"), [Phone("+(380)505987322")])
    Boris2 = Record(Name("Boris2"), [Phone("+(380)935552233")])
    Boris3 = Record(Name("Boris3"), [Phone("+(380)329890333")])
    tlf = AdressBook()
    tlf.add_record(Ivan)
    tlf.add_record(Voli)
    tlf.add_record(Boris1)
    tlf.add_record(Boris2)
    tlf.add_record(Boris3)
    for page in tlf.iterator(2):
        print(page)
    tlf.save_to_file()
    rez_tlf = AdressBook()
    rez_tlf = rez_tlf.restore_from_file()
    print("Ісходнік - ", tlf)
    print("Відновленний об'єкт - ", rez_tlf)
    
    print("Однакові ли вони -  ", tlf == rez_tlf)
    tlf.find_info('0')
    tlf.find_info('Bil')
    tlf.find_info('515')


if __name__ == "__main__":
    main()
