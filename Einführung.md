# Modellierung-einer-Population-w-hrend-des-Klimawandels

Ziel: Die Änderungen der Allel-Frequenzen einer ectothermen Population während des Klimawandels rechnerisch zu bestimmen; annehmend, dass eine selektion wegen die erhöhte Umgebungstemperatur staatfindet.

Methode: Eine der berühmteste Gleichungen der Populationsgenetik, das Hardy-Weinberg Gleichgewicht wurde verwendet. Für jede Generation wurde das Gesamtfitness berechnet und in die Gleichung eingesetzt, womit die Allel-Frequenzen der folgende Generation bestimmt wird. 

Verwenden: Den Code wurde für die Untersuchung von unterschiedlische Parameter für das Selektionsprozesses bzw. Selektionsgeschwindigkeit verwendet.
def compare(): Diese Funktion vergleicht 4 Populationen, die sich nur in dem eingegebene Parameter unterscheiden.

Die Eingaben für die Umgebung und die Population können durch den Terminal oder einfach innerhalb des Codes hingeführt werden. 
Durch den Terminal: ist gerade als Kommentar gesetzt (die Zeilen 506-562)
Innerhalb des Codes: Zeilen 563-575 für die Eingaben der Umgebung und Population 
                     Zeilen 578-586 für der untersuchte/geänderte Parameter und die Werte des Paremeters

Die Ausgaben/ Ergebnisse: Der Graph der Allel-Frequenzen abhängig von der Generation und der Graph der Fixierungsdauer. 

*
Detalierte Erklärung des Codes:
Als aller Erstes, wurde das class "Population" und "Environment" definiert. Beide enthalten die erforderliche Informationen und Funktionen, die die Rechnungen durchführen lassen.

Environment: (name, init_temp, climate_change) --> Mit Hilfe von "inir_temp" (der Anfangsfrequenz) und "climate-change" (die Temperaturänderung pro Jahr) und die Funktion temp kann die Temperatur des entsprechende Monats bestimmt werden.

Population: ( name, init_q, lifespan, w_graphname, dist_args, environment, time_span, selection_allel, new_pop)
init_q: die Anfangsfrequenz von q
lifespan: die Lebenserwartung (in Jahren)
w_graphname: der Name der Fitness-Graph-Datei
dist_args: die Parameter der Verteilung (als tuple) --> (a: "Quantilskoeffizient", scale: "Standardabweichung")
environmet: die Umgebung
time_span: die Zeitspanne der Veranschaulischung
selektion_allel: Gegen welchem Allel die Selektion staatfindet --> "d": Selektion gegen den dominaten Allel ,"r": Selektion gegen den recessiven Allel ,"h": Heterozygotenvorteil
new_pop: Wenn die Berechnung für eine population mit andere eigenschften gemacht wird

def W(): Gesamtfitness
Das Gesamtfitness lässt sich mit einer Integralrechnung der 2 Funktionen berechnen: 
def w(): Die Temperatur-Leistungskurve
def p(): Die Verteilung der Körpertemperaturen

Mit Hilfe des Selektionsgleichgewichts kann die Allel-Frequenzen der folgende Generation bestimmt werden. Das Gleichgewwicht hängt von dem Selektionsallel ab:
def p_val(): Selektion gegen den dominaten Allel
def q_val(): Selektion gegen den recessiven Allel
def p_val0(): Heterozygotenvorteil
Alle 3 Funktionen sind recursiv und berechnen für jede Generation n das Gesamtfitness W. W  und die Allel-Frequenz von n-1 wurde in die Gleichung eingesetz um die Allel-Frequenz von n zu bestimmen.


