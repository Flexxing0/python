import random
# ¡Nota la importación! Esta es de 'automata-lib'
from automata.fa.dfa import DFA

def crear_dfa_tragamonedas():
    """
    Crea el DFA que acepta el lenguaje L = { sss | s es un dígito }.
    Ej. L = { "000", "111", "222", ..., "999" }
    """
    
    # 1. Alfabeto (los 10 símbolos posibles)
    alfabeto = {str(i) for i in range(10)}

    # 2. Estados
    # q0 = inicial
    # q_lose = estado trampa (no ganador)
    # q_win = estado final (ganador)
    # q1_s = vio un símbolo 's' (ej. 'q1_7')
    # q2_s = vio dos símbolos 's' (ej. 'q2_7')
    
    estados = {'q0', 'q_win', 'q_lose'}
    # Creamos estados intermedios para cada símbolo
    for s in alfabeto:
        estados.add(f'q1_{s}') # Estado "vi un 's'"
        estados.add(f'q2_{s}') # Estado "vi dos 's'"

    # 3. Estado Inicial
    estado_inicial = 'q0'

    # 4. Estados Finales (solo hay uno)
    estados_finales = {'q_win'}

    # 5. Transiciones (la parte más compleja)
    transiciones = {}

    # --- Transiciones desde el estado inicial q0 ---
    # Desde q0, cualquier símbolo 's' que leas te lleva a 'q1_s'
    # (recuerda el primer símbolo)
    transiciones['q0'] = {}
    for s in alfabeto:
        transiciones['q0'][s] = f'q1_{s}'

    # --- Transiciones desde los estados intermedios ---
    for s in alfabeto:
        # Estamos en el estado 'q1_s' (vimos un 's')
        estado_q1 = f'q1_{s}'
        transiciones[estado_q1] = {}
        
        # Estamos en el estado 'q2_s' (vimos dos 's')
        estado_q2 = f'q2_{s}'
        transiciones[estado_q2] = {}

        for simbolo_actual in alfabeto:
            # Si el símbolo actual coincide con 's', avanzamos
            if simbolo_actual == s:
                transiciones[estado_q1][simbolo_actual] = f'q2_{s}' # Vimos 'ss'
                transiciones[estado_q2][simbolo_actual] = 'q_win'   # Vimos 'sss', ¡ganamos!
            else:
                # Si el símbolo no coincide, vamos al estado trampa
                transiciones[estado_q1][simbolo_actual] = 'q_lose' # Vimos 'sx'
                transiciones[estado_q2][simbolo_actual] = 'q_lose' # Vimos 'ssx'

    # --- Transiciones desde los estados trampa/finales ---
    # (Para manejar palabras de longitud > 3)
    
    # Si estás en 'q_win' y lees algo más, pierdes
    transiciones['q_win'] = {}
    for s in alfabeto:
        transiciones['q_win'][s] = 'q_lose'

    # Si estás en 'q_lose', te quedas en 'q_lose'
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