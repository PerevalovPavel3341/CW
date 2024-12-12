"""Модуль, содержащий реализацию АВЛ-дерева с дополнительными классами"""


class Record:
    """Класс записи студента. Содержит необходимые поля и сравнения объектов"""

    def __init__(self, suspicion: int = None, student_name: str = None):
        """Инициализация данных"""
        self.suspicion = suspicion
        self.student_name = student_name

    def __eq__(self, other):
        """Проверка на равенство"""
        if self.suspicion is None or other.suspicion is None:
            return self.student_name == other.student_name
        elif self.student_name is None or other.student_name is None:
            return self.suspicion == other.suspicion
        return self.suspicion == other.suspicion and self.student_name == other.student_name

    def __gt__(self, other):
        """Проверка на >. В приоритете сравнение по подозрительности"""
        if self.suspicion != other.suspicion:
            return self.suspicion > other.suspicion
        return self.student_name > other.student_name

    def __lt__(self, other):
        """Проверка на <. В приоритете сравнение по подозрительности"""
        if self.suspicion != other.suspicion:
            return self.suspicion < other.suspicion
        return self.student_name < other.student_name


class AVLNode:
    """Класс узла АВЛ-древа"""

    def __init__(self, record: Record):
        """Инициализация данных"""
        self.record = record
        self.left = None
        self.right = None
        self.parent = None
        self.height = 1


class AVLTree:
    def __init__(self):
        """Инициализация данных. Корень и максмальный узел"""
        self.root = None
        self.max_node = None

    def _get_height(self, node):
        """Получение высоты"""
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        """Получение балансируемости узла"""
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _update_parent(self, child, parent):
        """Обновление родителя для узла"""
        if child:
            child.parent = parent

    def _rotate_right(self, y):
        """Правый малый поворот"""
        x = y.left
        t2 = x.right

        x.right = y
        y.left = t2

        self._update_parent(x, y.parent)
        self._update_parent(y, x)
        self._update_parent(t2, y)

        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))

        return x

    def _rotate_left(self, x):
        """Левый малых поворот"""
        y = x.right
        t2 = y.left

        y.left = x
        x.right = t2

        self._update_parent(y, x.parent)
        self._update_parent(x, y)
        self._update_parent(t2, x)

        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

    def insert(self, node, record: Record, parent=None):
        """Вставка записи в дерево. Рекурсивный обход и нахождение нужного места.
         При необходимости обновление максмального узла и проведение балансировки"""
        if not node:
            new_node = AVLNode(record)
            new_node.parent = parent

            if not self.max_node or record > self.max_node.record:
                self.max_node = new_node

            return new_node

        if record < node.record:
            node.left = self.insert(node.left, record, node)
        elif record > node.record:
            node.right = self.insert(node.right, record, node)
        else:
            return node

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        balance = self._get_balance(node)

        if balance > 1 and record < node.left.record:
            return self._rotate_right(node)

        if balance < -1 and record > node.right.record:
            return self._rotate_left(node)

        if balance > 1 and record > node.left.record:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance < -1 and record < node.right.record:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def delete(self, node, record: Record):
        """Удаление записи из дерева. Рекурсивный обход и нахождение переданной записи.
         При необходимости обновление максмального узла и проведение балансировки после удаления"""
        if not node:
            return node
        if record < node.record:
            node.left = self.delete(node.left, record)
        elif record > node.record:
            node.right = self.delete(node.right, record)
        else:
            if not node.left:
                if node.right:
                    node.right.parent = node.parent
                if node == self.max_node:
                    self.max_node = node.parent
                return node.right
            elif not node.right:
                if node.left:
                    node.left.parent = node.parent
                if node == self.max_node:
                    self.max_node = self._find_new_max(node.left)
                return node.left

            temp = self._get_min_value_node(node.right)
            node.record = temp.record
            node.right = self.delete(node.right, temp.record)

        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        balance = self._get_balance(node)

        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._rotate_right(node)

        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)

        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._rotate_left(node)

        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)

        return node

    def find_by_name(self, node, record: Record):
        """Нахождение записи в дереве по имени"""
        if not node:
            return None
        if node.record == record:
            return node.record

        left_result = self.find_by_name(node.left, record)
        if left_result:
            return left_result

        return self.find_by_name(node.right, record)

    def find_by_suspicion(self, node, record: Record, arr: list):
        """Нахождение записей в дереве по значению подозрительности.
        Добавление соответствующих запсйе в массив."""
        if not node:
            return
        if record == node.record:
            arr.append(node.record)
            self.find_by_suspicion(node.left, record, arr)
            self.find_by_suspicion(node.right, record, arr)
        elif record < node.record:
            self.find_by_suspicion(node.left, record, arr)
        elif record > node.record:
            self.find_by_suspicion(node.right, record, arr)

    def find_by_record(self, node, record: Record):
        """Нахождение записи в дереве по всей записи"""
        if not node:
            return None
        if record < node.record:
            return self.find_by_record(node.left, record)
        elif record > node.record:
            return self.find_by_record(node.right, record)
        else:
            return node.record

    def _get_min_value_node(self, node):
        """Получение минимального узла в поддереве"""
        current = node
        while current.left:
            current = current.left
        return current

    def _find_new_max(self, node):
        """Получение максмального узла в поддереве"""
        current = node
        while current and current.right:
            current = current.right
        return current

    def insert_record(self, record: Record):
        """Вставка записи"""
        self.root = self.insert(self.root, record)

    def delete_record(self, record: Record):
        """Удаление записи"""
        self.root = self.delete(self.root, record)

    def find_record(self, record: Record):
        """Нахождение записи. Вызов нужного метода нахождения"""
        if record.suspicion is None and record.student_name is None:
            return None
        if record.suspicion is None:
            return [self.find_by_name(self.root, record)]
        if record.student_name is None:
            arr = []
            self.find_by_suspicion(self.root, record, arr)
            return arr
        return [self.find_by_record(self.root, record)]

    def print_descending(self):
        """Вывод записей по убыванию"""
        arr = []
        self._print_descending(self.root, arr)
        return arr

    def _print_descending(self, node: AVLNode, arr):
        """Вспомогательная функция для вывода"""
        if node is not None:
            self._print_descending(node.right, arr)
            arr.append([node.record.student_name, node.record.suspicion])
            print(node.record.student_name, node.record.suspicion)
            self._print_descending(node.left, arr)

    def find_most_suspicion(self, number_of_most: int):
        """Вывод самых подозрительных записей через максимальный узел"""
        result = []
        current = self.max_node

        while current and len(result) < number_of_most:
            result.append([current.record.suspicion, current.record.student_name])
            current = self._find_next_smallest(current)

        return result

    def _find_next_smallest(self, node: AVLNode):
        """Вспомогательная функция для обхода по поддереву"""
        if node.left:
            current = node.left
            while current.right:
                current = current.right
            return current
        else:
            current = node
            while current.parent and current == current.parent.left:
                current = current.parent
            return current.parent
