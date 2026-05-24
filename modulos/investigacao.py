import hashlib


# ==================================================
# GERAR ASSINATURA
# ==================================================
def generate_signature(recipe):
    """Gera assinatura SHA256 da receita."""
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
        # Assinaturas salvas no momento da inserção: {recipe_id: signature}
        self._original_signatures = {}
        self._snapshot()

    # ==================================================
    # SNAPSHOT INICIAL
    # ==================================================
    def _snapshot(self):
        """Salva assinatura original de todas as receitas carregadas."""
        for recipe in self.book.all_recipes():
            self._original_signatures[recipe.id] = generate_signature(recipe)

    # ==================================================
    # 1. VERIFICAR ALTERAÇÕES
    # ==================================================
    def check_alterations(self):
        """
        Compara assinatura atual com a original.
        Detecta receitas que foram modificadas após a inserção.
        """
        altered = []

        for recipe in self.book.all_recipes():
            original_sig = self._original_signatures.get(recipe.id)

            if original_sig is None:
                altered.append({
                    "id": recipe.id,
                    "name": recipe.name,
                    "problem": "Sem assinatura original — inserida após snapshot."
                })
                continue

            current_sig = generate_signature(recipe)

            if current_sig != original_sig:
                altered.append({
                    "id": recipe.id,
                    "name": recipe.name,
                    "problem": "Receita alterada desde a inserção."
                })

        return altered

    # ==================================================
    # 2. VERIFICAR DUPLICATAS
    # ==================================================
    def check_duplicates(self):
        """
        Detecta receitas com conteúdo idêntico (mesma assinatura SHA256).
        """
        signatures = {}
        duplicates = []

        for recipe in self.book.all_recipes():
            sig = generate_signature(recipe)

            if sig not in signatures:
                signatures[sig] = recipe
            else:
                duplicates.append({
                    "id_a": signatures[sig].id,
                    "id_b": recipe.id,
                    "name": recipe.name,
                    "problem": "Conteúdo idêntico."
                })

        return duplicates

    # ==================================================
    # 3. DETECTAR CONFLITOS ENTRE VERSÕES
    # ==================================================
    def check_conflicts(self):
        """
        Detecta receitas com mesmo nome mas ingredientes diferentes
        — possíveis versões conflitantes.
        """
        by_name = {}
        conflicts = []

        for recipe in self.book.all_recipes():
            name_key = recipe.name.lower().strip()

            if name_key not in by_name:
                by_name[name_key] = recipe
            else:
                other = by_name[name_key]
                if sorted(recipe.ingredients) != sorted(other.ingredients):
                    conflicts.append({
                        "id_a": other.id,
                        "id_b": recipe.id,
                        "name": recipe.name,
                        "problem": "Mesmo nome, ingredientes diferentes."
                    })

        return conflicts

    # ==================================================
    # 4. VALIDAR INTEGRIDADE DOS CAMPOS
    # ==================================================
    def check_integrity(self):
        """
        Valida campos obrigatórios de cada receita:
        - Nome não vazio
        - Pelo menos 1 ingrediente
        - Custo positivo
        - Rating entre 0 e 100
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

    # ==================================================
    # 5. RELATÓRIO COMPLETO
    # ==================================================
    def full_report(self):
        """Roda todas as verificações e exibe um relatório."""
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
            print("[OK] Nenhum problema encontrado.")

    # ==================================================
    # MENU DE INVESTIGAÇÃO
    # ==================================================

    def menu_investigation(self):
        while True:
            print("\n Modo Investigação")
            print("1. Verificar receitas alteradas.")
            print("2. Verificar duplicatas.")
            print("3. Detectar conflitos de versão.")
            print("4. Validar integridade dos campos.")
            print("5. Relatório completo.")
            print("0. Sair")

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
                    print("Saindo do modo investigação...\n")
                    break

                case _:
                    print("[AVISO] Opção inválida.")
