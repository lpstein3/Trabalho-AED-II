class TrieNode:
    def __init__(self):
        self.children = {}  # Uso de dicionarios para otimização de memória
        self.end_of_word = False
        self.recipes = []  # Uma lista para armazenar os ID's, para checar duplicadas


class TrieTree:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str, recipe_id):
        """Insere na trie"""
        word = word.lower().strip()
        current = self.root

        for letter in word:
            if letter not in current.children:
                current.children[letter] = TrieNode()
            current = current.children[letter]

        current.end_of_word = True
        if recipe_id not in current.recipes:
            current.recipes.append(recipe_id)

    def prefix_search(self, prefix: str):
        """Faz a busca por prefixo"""
        prefix = prefix.lower().strip()
        current = self.root

        for letter in prefix:
            if letter not in current.children:
                return []
            current = current.children[letter]
        return self._recover_recipes(current)

    def _recover_recipes(self, node: TrieNode):
        """Funcao interna para a recuperacao da string da receita"""
        result = []

        if node.end_of_word:
            result.extend(node.recipes)

        for child in node.children.values():
            result.extend(self._recover_recipes(child))
        return result
