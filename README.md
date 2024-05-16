# seminar_2
## Koraci za pokretanje igre
         
	 Instalacija Pythona na linuxu:
   ```sudo apt-get install python3.6```

    Instalacija TKintera:
```sudo apt-get install python3-tk```
    
    Preuzimanje koda s gita:
```git clone https://github.com/sandymany/seminar_2.git```

    Stvaranje i pokretanje virtualnog okruženja za Python:
```python3 -m venv .venv```
```source .venv/bin/activate```

    Instalacija potrebnih Python modula:
```pip3 install -r requirements.txt```

    Uštekati arduino u računalo i pokrenuti Arduino program

   Pomoću sljedeće naredbe možemo vidjeti listu spojenih uređaja:
```ls /dev/cu.*```

    Pokretanje igre:
```python3 scripts/sensor_game.py```
