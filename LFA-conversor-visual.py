import collections


class NFA:
    """Classe que representa um Autômato Finito Não Determinístico (AFN)."""
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.transitions = collections.defaultdict(list)
        self.start_state = None
        self.final_states = set()

class DFA:
    """Classe que representa um Autômato Finito Determinístico (AFD)."""
    def __init__(self):
        self.states = set()
        self.alphabet = set()
        self.transitions = {}
        self.start_state = None
        self.final_states = set()
    
def read_nfa_input():
    """Lê os dados do AFN a partir da entrada do usuário."""
   
    nfa = NFA()
    # Lê e valida estados
    while True:
        estados_input = input("Informe os estados do autômato (máximo 4, separados por vírgula): ").replace(' ', '').split(',')
        if len(estados_input) > 4:
            print("Erro: número máximo de estados é 4. Tente novamente.")
        else:
            nfa.states = set(estados_input)
            break

    # Lê e valida estado inicial
    while True:
        nfa.start_state = input("Informe o estado inicial: ").strip()
        if nfa.start_state not in nfa.states:
            print("Erro: estado inicial não está entre os estados definidos. Tente novamente.")
        else:
            break

    # Lê as transições
    print("Informe a função programa (ex: 0a1). Digite 'exit' para terminar:")
    trans_count = 0
    while True:
        if trans_count >= 8:
            print("Número máximo de transições (8) atingido.")
            break

        transition_str = input().strip()
        if transition_str.lower() == 'exit':
            break

        if len(transition_str) < 3:
            print("Formato inválido. Use algo como: 0a1")
            continue

        source, symbol, target = transition_str[0], transition_str[1], transition_str[2:]

        if source not in nfa.states or target not in nfa.states:
            print("Erro: estado de origem ou destino inválido.")
            continue

        if symbol not in nfa.alphabet and len(nfa.alphabet) >= 3:
            print("Erro: número máximo de símbolos no alfabeto é 3.")
            continue

        nfa.alphabet.add(symbol)
        nfa.transitions[(source, symbol)].append(target)
        trans_count += 1

    # Lê os estados finais
    while True:
        finais_input = input("Informe os estados finais (separados por vírgula): ").replace(' ', '').split(',')
        finais_set = set(finais_input)
        if not finais_set.issubset(nfa.states):
            print("Erro: um ou mais estados finais não estão entre os estados definidos. Tente novamente.")
        else:
            nfa.final_states = finais_set
            break

    return nfa

def format_state(state):
    """Formata conjuntos de estados para exibição legível."""
    if isinstance(state, (set, frozenset)):
        return "{" + ",".join(sorted(state)) + "}"
    return str(state)

def nfa_to_dfa_conversion(nfa):
    """Converte o AFN em um AFD equivalente."""
    dfa = DFA()
    dfa.alphabet = nfa.alphabet.copy()

    initial_state = frozenset([nfa.start_state])
    dfa.start_state = initial_state
    dfa.states.add(initial_state)

    queue = [initial_state]
    visited = set()

    while queue:
        current = queue.pop(0)
        visited.add(current)

        for symbol in dfa.alphabet:
            next_states = set()
            for state in current:
                next_states.update(nfa.transitions.get((state, symbol), []))

            if not next_states:
                continue

            frozen_next = frozenset(next_states)

            if frozen_next not in dfa.states:
                dfa.states.add(frozen_next)
                queue.append(frozen_next)

            dfa.transitions[(current, symbol)] = frozen_next

    for state in dfa.states:
        if any(final_state in state for final_state in nfa.final_states):
            dfa.final_states.add(state)

    return dfa

def print_nfa(nfa):
    print("\n--- AFN Lido ---")
    print(f"Estados: {sorted(nfa.states)}")
    print(f"Alfabeto: {sorted(nfa.alphabet)}")
    print("Transições:")
    for (src, sym), targets in nfa.transitions.items():
        print(f"  {src} --{sym}--> {targets}")
    print(f"Estado Inicial: {nfa.start_state}")
    print(f"Estados Finais: {sorted(nfa.final_states)}")

def print_dfa(dfa):
    print("\n--- AFD Gerado ---")
    print(f"Estados: {[format_state(s) for s in dfa.states]}")
    print(f"Alfabeto: {sorted(dfa.alphabet)}")
    print("Transições:")
    for (state, symbol), target in dfa.transitions.items():
        print(f"  {format_state(state)} --{symbol}--> {format_state(target)}")
    print(f"Estado Inicial: {format_state(dfa.start_state)}")
    print(f"Estados Finais: {[format_state(s) for s in dfa.final_states]}")

def test_auto_afn_para_afd(estados, estado_inicial, transicoes, estados_finais, nome_diagrama='afd_diagrama'):
    nfa = NFA()
    nfa.states = set(estados)
    nfa.start_state = estado_inicial
    nfa.final_states = set(estados_finais)
    
    for (origem, simbolo, destino) in transicoes:
        if simbolo not in nfa.alphabet and len(nfa.alphabet) < 3:
            nfa.alphabet.add(simbolo)
        nfa.transitions[(origem, simbolo)].append(destino)
    
    dfa = nfa_to_dfa_conversion(nfa)

    # Exibe os resultados
    print("\n--- Teste AFN -> AFD ---")
    print(f"AFN Estados: {nfa.states}")
    print(f"AFN Transições: {nfa.transitions}")
    print(f"AFN Estado Inicial: {nfa.start_state}")
    print(f"AFN Finais: {nfa.final_states}")

    print("\nAFD Estados:", [format_state(s) for s in dfa.states])
    print("AFD Transições:")
    for (state, symbol), target in dfa.transitions.items():
        print(f"  {format_state(state)} --{symbol}--> {format_state(target)}")
    print("AFD Estado Inicial:", format_state(dfa.start_state))
    print("AFD Finais:", [format_state(s) for s in dfa.final_states])

    # Gera o diagrama visual
    write_dot_file(dfa, nome_arquivo=nome_diagrama)

def run_suite_tests():
    print("\n### Teste 1: AFN simples ###")
    test_auto_afn_para_afd(
        estados=['0', '1'],
        estado_inicial='0',
        transicoes=[('0', 'a', '1')],
        estados_finais=['1'],
        nome_diagrama='afd_teste1'
    )

    print("\n### Teste 2: Máximo de símbolos (3) ###")
    test_auto_afn_para_afd(
        estados=['0', '1', '2'],
        estado_inicial='0',
        transicoes=[
            ('0', 'a', '1'),
            ('1', 'b', '2'),
            ('2', 'c', '0')
        ],
        estados_finais=['0'],
        nome_diagrama='afd_teste2'
    )

def write_dot_file(dfa, nome_arquivo='afd_output'):
    with open(nome_arquivo + '.dot', 'w') as f:
        f.write('digraph DFA {\n')
        f.write('  rankdir=LR;\n')
        f.write('  "" [shape=none];\n')
        f.write(f'  "" -> "{format_state(dfa.start_state)}";\n\n')

        # Estados
        for state in dfa.states:
            shape = 'doublecircle' if state in dfa.final_states else 'circle'
            f.write(f'  "{format_state(state)}" [shape={shape}];\n')

        f.write('\n')
        # Transições
        for (origem, simbolo), destino in dfa.transitions.items():
            f.write(f'  "{format_state(origem)}" -> "{format_state(destino)}" [label="{simbolo}"];\n')

        f.write('}\n')

    print(f"\nArquivo .dot gerado: {nome_arquivo}.dot")
    print("Use o visualizador online: https://dreampuf.github.io/GraphvizOnline/\n")


if __name__ == '__main__':
    
    run_suite_tests()
    
    '''
    nfa = read_nfa_input()
    print_nfa(nfa)

    dfa = nfa_to_dfa_conversion(nfa)
    print_dfa(dfa)
    
    # Gera o diagrama visual
    write_dot_file(dfa, nome_arquivo='afd_diagrama')
    '''
