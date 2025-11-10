## Tragamonedas
Este proyecto consiste en un juego de tragamonedas en el que un jugador apreta un boton "Palanca" que simula una tirada, y el programa tira una combinacion de simbolos, si son simbolos iguales, correspondera un premio.  
Dependiendo de la combinacion habra una recompensa determinada, asi como si no sale ninguna combinacion no habra ninguna recompensa.  
Se uso python y la libreria automata-lib, a continuacion se mostrara como se realiza la instalacion de la libreria.

## Instalacion [`automata-lib`](https://pypi.org/project/automata-lib/)  
Primero hay que instalar [`python`](https://www.python.org/downloads/) de la pagina oficial, instala para tu sistema operativo correspondiente. 
En la instalacion, selecciona la instalacion personalizada y marca todas las casillas. La razon principal es porque se necesitara el paquete completo de python para instalar la librerias.
Una vez instalado, verifica que esta instalado con el siguiente comando
```bash
python --version
```
Ahora procederemos a instalar automata-lib, usando el siguiente comando. Antes de hacerlo, puedes crear un entorno virtual de python para instalar la libreria solo en ese entorno.
```bash
python3 -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```
Hayas creado o no el entorno, usa el siguiente comando para instalar automata-lib
```bash
pip install automata-lib
```
Para verificar que este instalado, usa:
```bash
pip show automata-lib
```
Una vez verificaste que esta todo ok, puedes descargar el programa del tragamonedas:  
1. SSH
```bash
git clone git@github.com:Flexxing0/python.git
cd FTI
```
2. Si tenes token personal:
```bash
git clone https://<usuario>:<token>@github.com/Flexxing0/python.git
cd FTI
```
