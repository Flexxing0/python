import tkinter as tk
from tkinter import font
import random,construccionautomata


# ------------------------------------------------------------------
# PASO 4: LA CLASE DE LA INTERFAZ GRÁFICA (GUI) ¡MODIFICADA!
# ------------------------------------------------------------------

class SlotMachineGUI:
    def __init__(self, root, nfa, configuracion):
        self.root = root
        self.nfa = nfa
        self.configuracion = configuracion
        
        self.root.title("🎰 Tragamonedas Autómata (Animado) 🎰")
        self.root.geometry("600x450")
        self.root.configure(bg='#f0f0f0')

        # --- Variables de control ---
        self.simbolos_visuales = {k: v['visual'] for k, v in configuracion.items()}
        self.poblacion = list(configuracion.keys())
        self.pesos = [configuracion[k]['peso'] for k in self.poblacion]
        self.simbolos_disponibles = list(self.simbolos_visuales.values())
        self.esta_girando = False  # Bloquea el botón mientras gira
        self.tirada_final_claves = [] # Almacena el resultado real

        # --- Definir fuentes ---
        self.slot_font = font.Font(family="Arial", size=72, weight="bold")
        self.result_font = font.Font(family="Arial", size=18)
        self.lever_font = font.Font(family="Arial", size=22, weight="bold")

        # --- Frame para los símbolos ---
        slot_frame = tk.Frame(root, bg='#ffffff', relief='sunken', borderwidth=3)
        slot_frame.pack(pady=30, padx=20, fill='x')

        self.slot_vars = [tk.StringVar(value='-') for _ in range(3)]
        self.slot_labels = []
        
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
            self.slot_labels.append(lbl) # Guardamos las referencias a las etiquetas

        # --- Etiqueta para el resultado ---
        self.result_var = tk.StringVar(value="¡Presiona 'PALANCA' para jugar!")
        self.result_label = tk.Label(
            root, 
            textvariable=self.result_var, 
            font=self.result_font,
            bg='#f0f0f0'
        )
        self.result_label.pack(pady=10)

        # --- Botón de Palanca (Lever) ---
        self.lever_button = tk.Button(
            root, 
            text="P A L A N C A", 
            font=self.lever_font, 
            bg="#8B4513", # Color marrón de palanca
            fg="white",
            relief='raised',
            borderwidth=5,
            command=self.iniciar_juego
        )
        self.lever_button.pack(pady=20, ipadx=30, ipady=10)
    
    # ------------------------------------------------------------------
    # NUEVA LÓGICA DE ANIMACIÓN
    # ------------------------------------------------------------------

    def iniciar_juego(self):
        """Bloquea el botón e inicia la animación."""
        if self.esta_girando:
            return  # Evita tirones múltiples
        
        self.esta_girando = True
        self.lever_button.config(relief='sunken', state=tk.DISABLED, text="G I R A N D O")
        self.result_var.set("¡Buena suerte!")
        self.result_label.config(fg="#333333")
        
        # 1. Generar la tirada (el resultado real)
        self.tirada_final_claves = random.choices(self.poblacion, self.pesos, k=3)
        
        # 2. Iniciar la animación de los 3 rodillos
        # Rodillo 0 gira por 1.0 segundos
        self.animar_rodillos(0, 5, 1000) 
        # Rodillo 1 gira por 1.5 segundos
        self.animar_rodillos(1, 5, 1500)
        # Rodillo 2 gira por 2.0 segundos
        self.animar_rodillos(2, 5, 2000)

    def animar_rodillos(self, rodillo_idx, veces, duracion_total):
        """Cambia el símbolo aleatoriamente para simular el giro."""
        
        if veces > 0:
            # Símbolo aleatorio para la animación
            simbolo_anim = random.choice(self.simbolos_disponibles)
            self.slot_vars[rodillo_idx].set(simbolo_anim)
            
            # Repetir la animación
            tiempo_por_paso = duracion_total / (veces * 5) # Ajuste para velocidad
            self.root.after(int(tiempo_por_paso), 
                            lambda: self.animar_rodillos(rodillo_idx, veces - 1, duracion_total))
        else:
            # La animación ha terminado para este rodillo
            self.detener_rodillo(rodillo_idx)
    
    def detener_rodillo(self, rodillo_idx):
        """Muestra el símbolo final del rodillo."""
        
        clave_final = self.tirada_final_claves[rodillo_idx]
        visual_final = self.simbolos_visuales[clave_final]
        self.slot_vars[rodillo_idx].set(visual_final)
        
        # Si el último rodillo (índice 2) se detiene, evaluamos el juego
        if rodillo_idx == 2:
            self.root.after(300, self.verificar_premio)

    # ------------------------------------------------------------------
    # LÓGICA DE VERIFICACIÓN DE PREMIO (Igual a la versión anterior)
    # ------------------------------------------------------------------
    
    def verificar_premio(self):
        """Evalúa la tirada final y desbloquea el botón."""
        
        tirada_str = "".join(self.tirada_final_claves)
        simbolo1, simbolo2, simbolo3 = tirada_str[0], tirada_str[1], tirada_str[2]
        
        # Lógica de Ganancia por 3 o 2 símbolos iguales
        mensaje = ""
        
        # A) ¡VERIFICACIÓN DE 3 IGUALES!
        if self.nfa.accepts_input(tirada_str):
            recompensa = self.configuracion[simbolo1]['payout']
            visual_ganador = self.configuracion[simbolo1]['visual']
            mensaje = f"🎉 ¡JACKPOT DE {visual_ganador}! Ganas {recompensa} monedas"
            color = "#28a745"
            
        # C) PERDEDOR
        else:
            mensaje = "❌ ¡Oh no! Has perdido."
            color = "#dc3545"

        # Mostrar el resultado
        self.result_var.set(mensaje)
        self.result_label.config(fg=color)
        
        # Desbloquear el botón para el siguiente juego
        self.esta_girando = False
        self.lever_button.config(relief='raised', state=tk.NORMAL, text="P A L A N C A")


# ------------------------------------------------------------------
# PASO 5: EJECUCIÓN PRINCIPAL (Sin cambios)
# ------------------------------------------------------------------

if __name__ == "__main__":
    
    print("Creando el autómata (NFA) con estado final único...")
    nfa_tragamonedas = construccionautomata.crear_NFA_tragamonedas(construccionautomata.CONFIGURACION_SIMBOLOS)
    print("Autómata creado.")
    construccionautomata.generar_dot_automata(nfa_tragamonedas)
    root = tk.Tk()
    app = SlotMachineGUI(root, nfa_tragamonedas, construccionautomata.CONFIGURACION_SIMBOLOS)
    root.mainloop()