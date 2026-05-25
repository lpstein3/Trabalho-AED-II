class HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.table = [None] * self.capacity
        self.size = 0
        self.limit_load_factor = 0.75

    def _hash_function(self, key):
        # soma dos valores ASCII de cada caractere, depois módulo pelo tamanho atual
        ascii_sum = sum(ord(char) for char in str(key))
        return ascii_sum % self.capacity

    def _rehash(self):
        # dobra a capacidade e reinserir tudo quando o fator de carga passa de 0.75
        old_table = self.table
        self.capacity *= 2
        self.table = [None] * self.capacity
        self.size = 0
        for node in old_table:
            current = node
            while current is not None:
                self._insert_no_rehash(current.key, current.value)
                current = current.next

    def _insert_no_rehash(self, key, value):
        # versão interna do insert, chamada durante o rehash para evitar loop infinito
        index = self._hash_function(key)
        new_node = HashNode(key, value)

        if self.table[index] is None:
            self.table[index] = new_node
            self.size += 1
            return

        current = self.table[index]
        while True:
            if current.key == key:
                current.value = value
                return
            if current.next is None:
                break
            current = current.next

        current.next = new_node
        self.size += 1

    def insert(self, key, value):
        index = self._hash_function(key)
        new_node = HashNode(key, value)

        if self.table[index] is None:
            self.table[index] = new_node
            self.size += 1
        else:
            current = self.table[index]
            while True:
                if current.key == key:
                    current.value = value
                    return
                if current.next is None:
                    break
                current = current.next
            current.next = new_node
            self.size += 1

        if self.size / self.capacity > self.limit_load_factor:
            self._rehash()

    def search(self, key):
        index = self._hash_function(key)
        current = self.table[index]

        while current is not None:
            if current.key == key:
                return current.value
            current = current.next

        return None
