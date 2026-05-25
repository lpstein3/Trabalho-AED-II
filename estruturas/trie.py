class TrieNode:
    def __init__(self):
        # dicionário para economizar memória (só aloca os filhos que existem)
        self.children = {}
        self.end_of_word = False
        self.recipes = []   # IDs das receitas que terminam neste nó


class TrieTree:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str, recipe_id):
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
        prefix = prefix.lower().strip()
        current = self.root

        for letter in prefix:
            if letter not in current.children:
                return []
            current = current.children[letter]

        return self._collect_recipes(current)

    def _collect_recipes(self, node: TrieNode):
        result = []

        if node.end_of_word:
            result.extend(node.recipes)

        for child in node.children.values():
            result.extend(self._collect_recipes(child))

        return result
