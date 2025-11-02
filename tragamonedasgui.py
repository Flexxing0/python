import tkinter as tk
from tkinter import font
import random
# ¡Importamos NFA!
from automata.fa.nfa import NFA

# ------------------------------------------------------------------
# PASO 1: CONFIGURACIÓN CENTRAL DEL JUEGO (Sin cambios)
# ------------------------------------------------------------------
# Sigue definiendo las recompensas y probabilidades
CONFIGURACION_SIMBOLOS = {
    '9': {'visual': ' 7 ', 'payout': 1000, 'peso': 10},
    '8': {'visual': 'BAR', 'payout': 500,  'peso': 1},
    '0': {'visual': '💎', 'payout': 250,  'peso': 10},
    '6': {'visual': '⭐', 'payout': 100,  'peso': 3},
    '5': {'visual': '🔔', 'payout': 75,   'peso': 4},
    '7': {'visual': '🍀', 'payout': 50,   'peso': 5},
    '4': {'visual': '🍉', 'payout': 20,   'peso': 5},
    '3': {'visual': '🍊', 'payout': 15,   'peso': 4},
    '2': {'visual': '🍋', 'payout': 10,   'peso': 3},
    '1': {'visual': '🍒', 'payout': 5,    'peso': 2},
}

# ------------------------------------------------------------------
# PASO 2: LÓGICA DEL AUTÓMATA (NFA) ¡MODIFICADO!
# ------------------------------------------------------------------

def crear_NFA_tragamonedas(configuracion):
    """
    Crea el NFA donde TODAS las combinaciones 'sss'
    van a un ÚNICO estado final 'q_win'.
    """
    
    # 1. Alfabeto
    alfabeto = set(configuracion.keys())

    # 2. Estados (¡Solo un estado final!)
    estados = {'q0', 'q_win'} # 'q_win' es el único estado final
    for s in alfabeto:
        estados.add(f'q1_{s}') # Estado "vi un 's'"
        estados.add(f'q2_{s}') # Estado "vi dos 's'"

    # 3. Estado Inicial
    estado_inicial = 'q0'

    # 4. Estados Finales (¡Solo uno!)
    estados_finales = {'q_win'}

    # 5. Transiciones
    transiciones = {}
    
    # Desde q0
    transiciones['q0'] = {}
    for s in alfabeto:
        transiciones['q0'][s] = {f'q1_{s}'}

    # Desde q1 y q2
    for s in alfabeto:
        estado_q1 = f'q1_{s}'
        estado_q2 = f'q2_{s}'
        
        # q1 -> q2
        transiciones[estado_q1] = { s: {f'q2_{s}'} }
        
        # q2 -> q_win (¡TODOS van al mismo 'q_win'!)
        transiciones[estado_q2] = { s: {'q_win'} }

    # El estado final no tiene transiciones de salida
    transiciones['q_win'] = {}

    # 6. Crear y devolver el NFA
    nfa = NFA(
        states=estados,
        input_symbols=alfabeto,
        transitions=transiciones,
        initial_state=estado_inicial,
        final_states=estados_finales
    )
    return nfa

# ------------------------------------------------------------------
# PASO 3: GENERADOR DE CÓDIGO GRAPHVIZ (DOT)
# ------------------------------------------------------------------

def generar_dot_automata(automata):
    """
    Genera el string en formato DOT para Graphviz.
    (Esta función no necesita cambios)
    """
    
    print("--- CÓDIGO GRAPHVIZ (DOT) ---")
    print("Copia todo el texto entre las líneas de guiones")
    print("y pégalo en un visor online como 'Graphviz Online'.")
    print("---------------------------------")
    
    print("digraph NFA {")
    print("  rankdir=LR;")

    # 1. Definir nodos finales (¡Solo 'q_win'!)
    print("  node [shape = doublecircle];")
    for estado_final in automata.final_states:
        print(f'  "{estado_final}";')

    # 2. Definir nodos normales
    print("  node [shape = circle];")
    
    # 3. Definir estado inicial
    print(f'  "" [shape=plaintext, label=""];')
    print(f'  "" -> "{automata.initial_state}" [label="Inicio"];')

    # 4. Imprimir todas las transiciones
    for estado_origen in sorted(list(automata.transitions.keys())):
        transiciones = automata.transitions[estado_origen]
        for simbolo, estados_destino in transiciones.items():
            for estado_destino in estados_destino:
                print(f'  "{estado_origen}" -> "{estado_destino}" [label="{simbolo}"];')
            
    print("}")
    print("---------------------------------")
    print("Iniciando interfaz gráfica...")

# ------------------------------------------------------------------
# PASO 4: LA CLASE DE LA INTERFAZ GRÁFICA (GUI) ¡MODIFICADA!
# ------------------------------------------------------------------

class SlotMachineGUI:
    def __init__(self, root, nfa, configuracion):
        self.root = root
        self.nfa = nfa
        self.configuracion = configuracion
        
        self.root.title("🎰 Tragamonedas Autómata (Estado Único) 🎰")
        self.root.geometry("600x450")
        self.root.configure(bg='#f0f0f0')

        # --- Preparar datos para el juego ---
        self.simbolos_visuales = {k: v['visual'] for k, v in configuracion.items()}
        self.poblacion = list(configuracion.keys())
        self.pesos = [configuracion[k]['peso'] for k in self.poblacion]
        
        # --- Definir fuentes ---
        self.slot_font = font.Font(family="Arial", size=72, weight="bold")
        self.result_font = font.Font(family="Arial", size=18)
        self.button_font = font.Font(family="Arial", size=22, weight="bold")

        # --- Frame para los símbolos ---
        slot_frame = tk.Frame(root, bg='#ffffff', relief='sunken', borderwidth=3)
        slot_frame.pack(pady=30, padx=20, fill='x')

        self.slot_vars = [tk.StringVar(value='-') for _ in range(3)]
        
        for i in range(3):
            lbl = tk.Label(
                slot_frame, 
                textvariable=self.slot_vars[i], 
                font=self.slot_font, 
                width=3, 
                bg='white',
                fg='#333333'
            )
            lbl.pack(side=tk.LEFT, expand=True, fill='x', padx=10, pady=20)

        # --- Etiqueta para el resultado ---
        self.result_var = tk.StringVar(value="¡Presiona 'TIRAR' para jugar!")
        self.result_label = tk.Label(
            root, 
            textvariable=self.result_var, 
            font=self.result_font,
            bg='#f0f0f0'
        )
        self.result_label.pack(pady=10)

        # --- Botón para "Tirar" ---
        self.pull_button = tk.Button(
            root, 
            text="TIRAR", 
            font=self.button_font, 
            bg="#28a745",
            fg="white",
            relief='raised',
            borderwidth=3,
            command=self.jugar # Llama a la función self.jugar
        )
        self.pull_button.pack(pady=20, ipadx=30, ipady=10)

    def jugar(self):
        """
        ¡Lógica de juego MODIFICADA!
        Usa .accepts_input() y luego mira la tirada.
        """
        # 1. Generar la tirada (con probabilidades)
        tirada = random.choices(self.poblacion, self.pesos, k=3)
        tirada_str = "".join(tirada)
        
        # 2. Obtener los símbolos visuales
        visuales = [self.simbolos_visuales[s] for s in tirada]
        
        # 3. Actualizar las etiquetas en la pantalla
        for i in range(3):
            self.slot_vars[i].set(visuales[i])
        
        # 4. ¡USAR EL AUTÓMATA PARA VALIDAR EL PATRÓN!
        # .accepts_input() solo devuelve True o False
        if self.nfa.accepts_input(tirada_str):
            # ¡Ganador! El autómata confirmó que son 3 iguales.
            
            # Ahora, la GUI debe averiguar QUÉ premio dar.
            # Como sabemos que son 3 iguales, solo miramos el primero.
            simbolo_ganador = tirada_str[0] # ej. '7'
            
            # Buscamos la recompensa en nuestra configuración
            recompensa = self.configuracion[simbolo_ganador]['payout']
            visual_ganador = self.configuracion[simbolo_ganador]['visual']
            
            # Mostramos el mensaje de victoria
            self.result_var.set(f"¡JACKPOT DE {visual_ganador}! Ganas {recompensa} monedas")
            self.result_label.config(fg="#28a745") # Color verde
        else:
            # Perdedor
            self.result_var.set("¡Oh no! Has perdido.")
            self.result_label.config(fg="#dc3545") # Color rojo

# ------------------------------------------------------------------
# PASO 5: EJECUCIÓN PRINCIPAL (Sin cambios)
# ------------------------------------------------------------------

if __name__ == "__main__":
    
    # 1. Creamos el "cerebro" (el NFA con un solo estado final)
    print("Creando el autómata (NFA) con estado final único...")
    nfa_tragamonedas = crear_NFA_tragamonedas(CONFIGURACION_SIMBOLOS)
    print("Autómata creado.")

    # 2. Generamos el código DOT para Graphviz
    generar_dot_automata(nfa_tragamonedas)

    # 3. Creamos la ventana principal de la GUI
    root = tk.Tk()

    # 4. Creamos nuestra aplicación
    app = SlotMachineGUI(root, nfa_tragamonedas, CONFIGURACION_SIMBOLOS)

    # 5. Iniciamos el bucle principal de la aplicación
    root.mainloop()