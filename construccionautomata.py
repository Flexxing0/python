from automata.fa.nfa import NFA


CONFIGURACION_SIMBOLOS = {
    '9': {'visual': ' 7 ', 'payout': 1000, 'peso': 5},   
    '8': {'visual': 'BAR', 'payout': 500,  'peso': 10},  
    '0': {'visual': '💎', 'payout': 250,  'peso': 5},   
    '6': {'visual': '⭐', 'payout': 100,  'peso': 15},  
    '5': {'visual': '🔔', 'payout': 75,   'peso': 25},  
    '7': {'visual': '🍀', 'payout': 50,   'peso': 40},  
    '4': {'visual': '🍉', 'payout': 20,   'peso': 50},  
    '3': {'visual': '🍊', 'payout': 15,   'peso': 70},  
    '2': {'visual': '🍋', 'payout': 10,   'peso': 380}, 
    '1': {'visual': '🍒', 'payout': 5,    'peso': 400}, 
}
def crear_NFA_tragamonedas(configuracion):
    alfabeto = set(configuracion.keys())
    estados = {'q0', 'q_win'} 
    for s in alfabeto:
        estados.add(f'q1_{s}')
        estados.add(f'q2_{s}')
    estado_inicial = 'q0'
    estados_finales = {'q_win'}
    transiciones = {}
    transiciones['q0'] = {s: {f'q1_{s}'} for s in alfabeto}
    for s in alfabeto:
        transiciones[f'q1_{s}'] = {s: {f'q2_{s}'}}
        transiciones[f'q2_{s}'] = {s: {'q_win'}}
    transiciones['q_win'] = {}
    return NFA(states=estados, input_symbols=alfabeto, transitions=transiciones, 
            initial_state=estado_inicial, final_states=estados_finales)

def generar_dot_automata(automata):

    print("--- CÓDIGO GRAPHVIZ (DOT) ---")#codigo que genera un grafo en graphviz online
    print("---------------------------------")
    print("digraph NFA {")
    print("  rankdir=LR;")
    print("  node [shape = doublecircle];")
    for estado_final in automata.final_states:
        print(f'  "{estado_final}";')
    print("  node [shape = circle];")
    print(f'  "" [shape=plaintext, label=""];')
    print(f'  "" -> "{automata.initial_state}" [label="Inicio"];')
    for estado_origen in sorted(list(automata.transitions.keys())):
        transiciones = automata.transitions[estado_origen]
        for simbolo, estados_destino in transiciones.items():
            for estado_destino in estados_destino:
                print(f'  "{estado_origen}" -> "{estado_destino}" [label="{simbolo}"];')
    print("}")
    print("---------------------------------")
    print("Iniciando interfaz gráfica...")
        
if __name__ == "__main__":
    nfa_tragamonedas = crear_NFA_tragamonedas(CONFIGURACION_SIMBOLOS)

    generar_dot_automata(nfa_tragamonedas)