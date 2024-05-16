# seminar_2
\section{Koraci za pokretanje igre}

        U ovom će poglavlju biti opisan postupak preuzimanja programskog koda i instalacija alata potrebnih za pokretanje igre.
        Budući da je programski kod igre napisan u Pythonu, prvo je potrebno instalirati Python i potrebne module koji su prema dobroj praksi nabrojani u datoteci.

         
    \begin{enumerate}

    \item Instalacija Pythona na linuxu:
    \begin{lstlisting}[language=python, frame=single]
sudo apt-get install python3.6
    \end{lstlisting}

    \item Instalacija TKintera:
    \begin{lstlisting}[language=python, frame=single]
sudo apt-get install python3-tk
    \end{lstlisting}
    
    \item Preuzimanje koda s gita:
    \begin{lstlisting}[language=python, frame=single]
git clone https://github.com/sandymany/seminar_2.git
    \end{lstlisting}

    \item Stvaranje i pokretanje virtualnog okruženja za Python:
    \begin{lstlisting}[language=python, frame=single]
python3 -m venv .venv
source .venv/bin/activate
    \end{lstlisting}

    \item Instalacija potrebnih Python modula:
    \begin{lstlisting}[language=python, frame=single]
pip3 install -r requirements.txt
    \end{lstlisting}

    \item Uštekati arduino u računalo i pokrenuti Arduino program

    \item Pomoću sljedeće naredbe možemo vidjeti listu spojenih uređaja:
    \begin{lstlisting}[language=python, frame=single]
ls /dev/cu.*
    \end{lstlisting}

    \item Pokretanje igre:
    \begin{lstlisting}[language=python, frame=single]
python3 scripts/sensor_game.py
    \end{lstlisting}
    
    \end{enumerate}

    Na slici ispod može se vidjeti demonstracija igre.

        \begin{figure}[H]
                \begin{center}
                    \includegraphics[width=10cm]{slike/game.png}
			         \caption{Demonstracija igre}
			         \label{fig:Prikaz rotacija propelera}
                 \end{center}
	    \end{figure}
