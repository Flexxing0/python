import random
# ¡Importación de automata-lib!
from automata.fa.dfa import DFA

def crear_dfa_tragamonedas():
    """
    Crea el DFA que acepta el lenguaje L = { sss | s es un dígito }.
    """
    
    # 1. Alfabeto
    alfabeto = {str(i) for i in range(10)}

    # 2. Estados
    estados = {'q0', 'q_win', 'q_lose'}
    for s in alfabeto:
        estados.add(f'q1_{s}') # Estado "vi un 's'"
        estados.add(f'q2_{s}') # Estado "vi dos 's'"

    # 3. Estado Inicial
    estado_inicial = 'q0'

    # 4. Estados Finales
    estados_finales = {'q_win'}

    # 5. Transiciones
    transiciones = {}
    transiciones['q0'] = {}
    for s in alfabeto:
        transiciones['q0'][s] = f'q1_{s}'

    for s in alfabeto:
        estado_q1 = f'q1_{s}'
        transiciones[estado_q1] = {}
        estado_q2 = f'q2_{s}'
        transiciones[estado_q2] = {}

        for simbolo_actual in alfabeto:
            if simbolo_actual == s:
                transiciones[estado_q1][simbolo_actual] = f'q2_{s}'
                transiciones[estado_q2][simbolo_actual] = 'q_win'
            else:
                transiciones[estado_q1][simbolo_actual] = 'q_lose'
                transiciones[estado_q2][simbolo_actual] = 'q_lose'

    transiciones['q_win'] = {}
    for s in alfabeto:
        transiciones['q_win'][s] = 'q_lose'

    transiciones['q_lose'] = {}
    for s in alfabeto:
        transiciones['q_lose'][s] = 'q_lose'

    # 6. Crear y devolver el DFA
    dfa = DFA(
        states=estados,
        input_symbols=alfabeto,
        transitions=transiciones,
        initial_state=estado_inicial,
        final_states=estados_finales
    )
    return dfa

def jugar_tragamonedas(dfa):
    """
    Simula el juego del tragamonedas usando el DFA creado.
    """
    simbolos = {
        '1': '🍒', '2': '🍋', '3': '🍊', '4': '🍉', '5': '🔔',
        '6': '⭐', '7': '🍀', '8': ' BAR ', '9': ' 7 ', '0': '💎',
    }
    opciones = list(simbolos.keys())

    print("--- 🎰 ¡Bienvenido al Tragamonedas con 'automata-lib'! 🎰 ---")
    print("Regla: Ganas si sacas 3 símbolos iguales (ej. 🍒🍒🍒 o 7 7 7).")

    while True:
        try:
            input("\nPresiona Enter para tirar de la palanca...")
        except EOFError:
            break
            
        tirada = [random.choice(opciones) for _ in range(3)]
        tirada_str = "".join(tirada)
        
        visuales = [simbolos[s] for s in tirada]
        print("\nGirando... | {} | {} | {} |".format(visuales[0], visuales[1], visuales[2]))
        
        if dfa.accepts_input(tirada_str):
            mensaje = "¡JACKPOT! ¡Has ganado!"
        else:
            mensaje = "¡Oh no! Has perdido."
        
        print(f"\nResultado del autómata: {mensaje}")
        print("-------------------------------------------------")
        
        respuesta = input("¿Quieres jugar de nuevo? (s/n): ")
        if respuesta.lower() != 's':
            print("¡Gracias por jugar!")
            break

# --- ¡NUEVA FUNCIÓN! ---
def generar_dot_tragamonedas(dfa):
    """
    Genera el string en formato DOT para Graphviz, leyendo el objeto DFA.
    ¡Esto evita usar pygraphviz por completo!
    """
    
    print("--- CÓDIGO GRAPHVIZ (DOT) ---")
    print("Copia todo el texto entre las líneas de guiones")
    print("y pégalo en un visor online como 'Graphviz Online'.")
    print("---------------------------------")
    
    # Inicio del grafo
    print("digraph DFA {")
    print("  rankdir=LR;") # De izquierda a derecha

    # 1. Definir nodos finales (doble círculo)
    print("  node [shape = doublecircle];")
    for estado_final in dfa.final_states:
        print(f'  "{estado_final}";')

    # 2. Definir nodos normales (círculo simple)
    print("  node [shape = circle];")
    
    # 3. Definir estado inicial (con una flecha de entrada)
    print(f'  "" [shape=plaintext];') # Nodo de inicio invisible
    print(f'  "" -> "{dfa.initial_state}" [label="Inicio"];')

    # 4. Imprimir todas las transiciones
    # (Esto será largo, ¡pero es lo que queremos!)
    for estado_origen, transiciones in dfa.transitions.items():
        for simbolo, estado_destino in transiciones.items():
            # Para agrupar transiciones, las juntaremos
            # (Lo haremos simple por ahora, una línea por transición)
            print(f'  "{estado_origen}" -> "{estado_destino}" [label="{simbolo}"];')
            
    # Fin del grafo
    print("}")
    
    print("---------------------------------")
    print("El juego comenzará ahora...")


# --- Función Principal ---
if __name__ == "__main__":
    
    # 1. Creamos la máquina tragamonedas (el DFA)
    dfa_tragamonedas = crear_dfa_tragamonedas()
    
    # 2. Generar el código DOT (Plan C)
    # ¡Esto no puede fallar, ya que solo usa "print"s!
    generar_dot_tragamonedas(dfa_tragamonedas)
    
    # 3. Iniciamos el juego
    jugar_tragamonedas(dfa_tragamonedas)