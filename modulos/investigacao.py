import hashlib


def generate_signature(recipe):
    """Gera uma assinatura SHA256 baseada no conteúdo da receita."""
    content = (
        recipe.name.lower().strip()
        + "".join(sorted(i.lower() for i in recipe.ingredients))
        + str(recipe.cost)
        + str(recipe.rating)
    )
    return hashlib.sha256(content.encode()).hexdigest()


class Investigation:
    def __init__(self, recipe_book):
        self.book = recipe_book
        self._original_signatures = {}
        self._snapshot()

    def _snapshot(self):
        """Registra a assinatura de cada receita no momento do carregamento."""
        for recipe in self.book.all_recipes():
            self._original_signatures[recipe.id] = generate_signature(recipe)

    def check_alterations(self):
        """Compara a assinatura atual de cada receita com a registrada no snapshot."""
        altered = []

        for recipe in self.book.all_recipes():
            original_sig = self._original_signatures.get(recipe.id)

            if original_sig is None:
                altered.append({
                    "id": recipe.id,
                    "name": recipe.name,
                    "problem": "Sem assinatura original — inserida após o snapshot."
                })
                continue

            if generate_signature(recipe) != original_sig:
                altered.append({
                    "id": recipe.id,
                    "name": recipe.name,
                    "problem": "Receita foi modificada após a inserção."
                })

        return altered

    def check_duplicates(self):
        """Detecta receitas com conteúdo idêntico pela assinatura SHA256."""
        seen = {}
        duplicates = []

        for recipe in self.book.all_recipes():
            sig = generate_signature(recipe)

            if sig not in seen:
                seen[sig] = recipe
            else:
                duplicates.append({
                    "id_a": seen[sig].id,
                    "id_b": recipe.id,
                    "name": recipe.name,
                    "problem": "Conteúdo idêntico."
                })

        return duplicates

    def check_conflicts(self):
        """Detecta receitas com o mesmo nome mas ingredientes diferentes."""
        by_name = {}
        conflicts = []

        for recipe in self.book.all_recipes():
            key = recipe.name.lower().strip()

            if key not in by_name:
                by_name[key] = recipe
            else:
                other = by_name[key]
                if sorted(recipe.ingredients) != sorted(other.ingredients):
                    conflicts.append({
                        "id_a": other.id,
                        "id_b": recipe.id,
                        "name": recipe.name,
                        "problem": "Mesmo nome, ingredientes diferentes."
                    })

        return conflicts

    def check_integrity(self):
        """
        Valida campos obrigatórios de cada receita:
        nome não vazio, pelo menos 1 ingrediente, custo positivo, rating entre 0 e 100.
        """
        invalid = []

        for recipe in self.book.all_recipes():
            problems = []

            if not recipe.name or not recipe.name.strip():
                problems.append("Nome vazio.")

            if not recipe.ingredients:
                problems.append("Sem ingredientes.")

            if recipe.cost <= 0:
                problems.append(f"Custo inválido: {recipe.cost}.")

            if not (0 <= recipe.rating <= 100):
                problems.append(f"Rating inválido: {recipe.rating}.")

            if problems:
                invalid.append({
                    "id": recipe.id,
                    "name": recipe.name,
                    "problem": " | ".join(problems)
                })

        return invalid

    def full_report(self):
        print(" RELATÓRIO DE INVESTIGAÇÃO\n")

        checks = [
            ("Receitas Alteradas",    self.check_alterations()),
            ("Duplicatas",            self.check_duplicates()),
            ("Conflitos de Versão",   self.check_conflicts()),
            ("Integridade de Campos", self.check_integrity()),
        ]

        all_clean = True

        for title, results in checks:
            print(f"[{title}] — {len(results)} problema(s) encontrado(s).")
            if results:
                all_clean = False
                for r in results:
                    print(
                        f"  • ID: {r.get('id', r.get('id_a'))} | {r['name']} → {r['problem']}")

        if all_clean:
            print("Nenhum problema encontrado.")

    def menu_investigation(self):
        while True:
            print("\n Investigação")
            print("1. Receitas alteradas")
            print("2. Duplicatas")
            print("3. Conflitos de versão")
            print("4. Integridade dos campos")
            print("5. Relatório completo")
            print("0. Voltar")

            op = input("Escolha uma opção: ")

            match op:
                case "1":
                    results = self.check_alterations()
                    print(f"\n{len(results)} receita(s) alterada(s).")
                    for r in results:
                        print(f"  • {r['id']} | {r['name']} → {r['problem']}")

                case "2":
                    results = self.check_duplicates()
                    print(f"\n{len(results)} duplicata(s) encontrada(s).")
                    for r in results:
                        print(
                            f"  • {r['id_a']} ↔ {r['id_b']} | {r['name']} → {r['problem']}")

                case "3":
                    results = self.check_conflicts()
                    print(f"\n{len(results)} conflito(s) encontrado(s).")
                    for r in results:
                        print(
                            f"  • {r['id_a']} ↔ {r['id_b']} | {r['name']} → {r['problem']}")

                case "4":
                    results = self.check_integrity()
                    print(
                        f"\n{len(results)} receita(s) com campo(s) inválido(s).")
                    for r in results:
                        print(f"  • {r['id']} | {r['name']} → {r['problem']}")

                case "5":
                    self.full_report()

                case "0":
                    break

                case _:
                    print("Opção inválida.")
