def jugar_tragamonedas(dfa):
    """
    Simula el juego del tragamonedas usando el DFA creado.
    """
    # Definimos los símbolos (los mismos que el alfabeto del DFA)
    simbolos = {
        '1': '🍒',  # Cereza
        '2': '🍋',  # Limón
        '3': '🍊',  # Naranja
        '4': '🍉',  # Sandía
        '5': '🔔',  # Campana
        '6': '⭐',  # Estrella
        '7': '🍀',  # Trébol
        '8': ' BAR ',
        '9': ' 7 ',
        '0': '💎',  # Diamante
    }
    opciones = list(simbolos.keys()) # ['1', '2', '3', ..., '0']

    print("--- 🎰 ¡Bienvenido al Tragamonedas con 'automata-lib'! 🎰 ---")
    print("Regla: Ganas si sacas 3 símbolos iguales (ej. 🍒🍒🍒 o 7 7 7).")

    while True:
        try:
            input("\nPresiona Enter para tirar de la palanca...")
        except EOFError:
            break
            
        # 1. Generar la tirada (3 símbolos aleatorios)
        tirada = [random.choice(opciones) for _ in range(3)]
        tirada_str = "".join(tirada)
        
        # Mapear los dígitos a símbolos visuales
        visuales = [simbolos[s] for s in tirada]
        
        print("\nGirando... | {} | {} | {} |".format(visuales[0], visuales[1], visuales[2]))
        
        # 2. Validar la tirada con el autómata
        # Usamos el método .accepts_input() que devuelve True si
        # la palabra es aceptada (termina en un estado final)
        if dfa.accepts_input(tirada_str):
            mensaje = "¡JACKPOT! ¡Has ganado!"
        else:
            mensaje = "¡Oh no! Has perdido."
        
        # 3. Mostrar resultado
        print(f"\nResultado del autómata: {mensaje}")
        
        print("-------------------------------------------------")
        
        respuesta = input("¿Quieres jugar de nuevo? (s/n): ")
        if respuesta.lower() != 's':
            print("¡Gracias por jugar!")
            break