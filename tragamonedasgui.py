import tkinter as tk
from tkinter import font
import random,construccionautomata


class SlotMachineGUI:
    def __init__(self, root, nfa, configuracion):
        self.root = root
        self.nfa = nfa
        self.configuracion = configuracion
        
        self.root.title("🎰 Tragamonedas Autómata (Animado) 🎰")
        self.root.geometry("600x450")
        self.root.configure(bg='#f0f0f0')

        self.simbolos_visuales = {k: v['visual'] for k, v in configuracion.items()}
        self.poblacion = list(configuracion.keys())
        self.pesos = [configuracion[k]['peso'] for k in self.poblacion]
        self.simbolos_disponibles = list(self.simbolos_visuales.values())
        self.esta_girando = False  # Bloquea el botón mientras gira
        self.tirada_final_claves = [] # Almacena el resultado real

        self.slot_font = font.Font(family="Arial", size=72, weight="bold")
        self.result_font = font.Font(family="Arial", size=18)
        self.lever_font = font.Font(family="Arial", size=22, weight="bold")

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
            self.slot_labels.append(lbl)

        self.result_var = tk.StringVar(value="¡Presiona 'PALANCA' para jugar!")
        self.result_label = tk.Label(
            root, 
            textvariable=self.result_var, 
            font=self.result_font,
            bg='#f0f0f0'
        )
        self.result_label.pack(pady=10)

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
    
    def iniciar_juego(self):
        """Bloquea el botón e inicia la animación."""
        if self.esta_girando:
            return  
        self.esta_girando = True
        self.lever_button.config(relief='sunken', state=tk.DISABLED, text="G I R A N D O")
        self.result_var.set("¡Buena suerte!")
        self.result_label.config(fg="#333333")
        
        self.tirada_final_claves = random.choices(self.poblacion, self.pesos, k=3)
        
        self.animar_rodillos(0, 5, 1000) 
        self.animar_rodillos(1, 5, 1500)
        self.animar_rodillos(2, 5, 2000)

    def animar_rodillos(self, rodillo_idx, veces, duracion_total):
        """Cambia el símbolo aleatoriamente para simular el giro."""
        
        if veces > 0:
            simbolo_anim = random.choice(self.simbolos_disponibles)
            self.slot_vars[rodillo_idx].set(simbolo_anim)
            
            tiempo_por_paso = duracion_total / (veces * 5) 
            self.root.after(int(tiempo_por_paso), 
                            lambda: self.animar_rodillos(rodillo_idx, veces - 1, duracion_total))
        else:
            self.detener_rodillo(rodillo_idx)
    
    def detener_rodillo(self, rodillo_idx):
        """Muestra el símbolo final del rodillo."""
        
        clave_final = self.tirada_final_claves[rodillo_idx]
        visual_final = self.simbolos_visuales[clave_final]
        self.slot_vars[rodillo_idx].set(visual_final)
        
        if rodillo_idx == 2:
            self.root.after(300, self.verificar_premio)

    def verificar_premio(self):
        """Evalúa la tirada final y desbloquea el botón."""
        
        tirada_str = "".join(self.tirada_final_claves)
        simbolo1, simbolo2, simbolo3 = tirada_str[0], tirada_str[1], tirada_str[2]
        
        mensaje = ""
        
        if self.nfa.accepts_input(tirada_str):
            recompensa = self.configuracion[simbolo1]['payout']
            visual_ganador = self.configuracion[simbolo1]['visual']
            mensaje = f"🎉 ¡JACKPOT DE {visual_ganador}! Ganas {recompensa} monedas"
            color = "#28a745"
            
        else:
            mensaje = "❌ ¡Oh no! Has perdido."
            color = "#dc3545"

        self.result_var.set(mensaje)
        self.result_label.config(fg=color)
        
        self.esta_girando = False
        self.lever_button.config(relief='raised', state=tk.NORMAL, text="P A L A N C A")

if __name__ == "__main__":
    
    print("Creando el autómata (NFA) con estado final único...")
    nfa_tragamonedas = construccionautomata.crear_NFA_tragamonedas(construccionautomata.CONFIGURACION_SIMBOLOS)
    print("Autómata creado.")
    construccionautomata.generar_dot_automata(nfa_tragamonedas)
    root = tk.Tk()
    app = SlotMachineGUI(root, nfa_tragamonedas, construccionautomata.CONFIGURACION_SIMBOLOS)
    root.mainloop()