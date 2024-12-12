"""Модуль, содержащий систему по работе с системой прокторинга"""

from hash import HashTable, Record, AVLTree


class ProctoringSystem:
    def __init__(self):
        self.hash_groups = HashTable(20)  # хэш-таблица группа: авл-дерево группы
        self.top_records = AVLTree()  # авл-дерево всех записей

    def add_record(self, student: str, suspicion: int, group: int):
        """Добавление записи в группу"""
        record = Record(suspicion, student)
        self.hash_groups.insert_record(group, record)

        self.top_records.insert_record(record)

    def del_record(self, record: Record, group: int):
        """Удаление записи из группы. Если не найдена группа или неправильно передана
        запись - программа не выполняется"""
        if not record or not record.student_name or not record.suspicion:
            print("Incorrect record!")
            return
        tree = self.hash_groups.find(group)
        if not tree:
            print("Incorrect group!")
            return

        tree.delete_record(record)

        self.top_records.delete_record(record)

    def find_record(self, group, student: str = None, suspicion: int = None):
        """Нахождение записи в дереве группы. Если не найдена группа - программа не выполняется"""
        tree = self.hash_groups.find(group)
        if not tree:
            print("Incorrect group!")
            return
        record = Record(suspicion, student)
        return tree.find_record(record)

    def print_records_of_group(self, group: int):
        """Вывод записей переданной группы в убывающем порядке.
        Если группа не найдена - программа не выполняется"""
        print("Group:", group)
        tree = self.hash_groups.find(group)
        if not tree:
            print("Incorrect group!")
            return
        return tree.print_descending()

    def add_group(self, group: int):
        """Добавление группы в хэш-таблицу"""
        self.hash_groups.add_group(group)

    def remove_group(self, group: int):
        """Удаление группы из хэш-таблицы, если она найдется"""
        self.hash_groups.remove(group)

    def print_groups(self):
        """Вывод всех групп из таблицы"""
        print("All groups:")
        for i in self.hash_groups.get_all_keys():
            print(i)

    def find_group(self, group: int):
        """Нахождение авл-дерева переданной группы"""
        return self.hash_groups.find(group)

    def print_top10_records(self):
        """Вывод 10 самых подозрительных записей всех групп"""
        return self.top_records.find_most_suspicion(10)

    def find_most_suspicion(self, n: int, group: int):
        """Нахождение самых подозрительных записей группы"""
        res = self.hash_groups.find(group).find_most_suspicion(n)
        return res
