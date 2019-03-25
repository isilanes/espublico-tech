Script de Python para resolver el Reto 4 de esPublico.tech (https://espublico.tech/reto/4).

## Uso

Desde la línea de comandos (en Linux), ejecutar:

```bash
$ python3 reto4.py
```

El script espera un fichero de input en el mismo directorio, llamado literalmente `input.txt`. Si se desea
leer otro fichero de input, puede usarse la opción `-i`:

```bash
$ python3 reto4.py -i another_input.txt
```

Para mostrar una breve ayuda con todas las opciones disponibles:

```bash
$ python reto4.py -h
```

El fichero de entrada debe tener el siguiente formato:

```text
Bor[0]
Bestla[0]
Ve[0]=Bor+Bestla
Odin[1]=Bor+Bestla
Jord[0]
etc
```

El script produce el output requerido por pantalla, con el formato:

```text
Bor=AA[0],Aa[1],aa[0]
Bestla=AA[0],Aa[1],aa[0]
Ve=AA[0.3333333333333333],Aa[0.6666666666666666],aa[0.0]
Odin=AA[0],Aa[0],aa[1]
Jord=AA[0],Aa[1],aa[0]
etc
```

## Requerimientos

* Python 3.x
* numpy

Realmente funciona también con Python 2.7 (necesitaría la línea `# -*- coding=utf-8 -*-` al principio), pero
se ha desarrollado con solo Python 3.x en mente.

El uso de numpy obedece únicamente a un interés por la sencillez y la comodidad, no a la eficiencia. Considero numpy
suficiente ubicuo como para no verme impulsado a prescindir de él en aras de la compatibilidad.

## Funcionamiento y algoritmo

Las relaciones entre familiares asgardianos se han modelado con un grafo dirigido, en el que cada nodo es un
miembro, y cada relación una arista señalando de progenitor a descendiente.

Se ha procesado cada miembro asgardiano con el siguiente algoritmo para decidir sobre la probabilidad
de tener cada genotipo:

1. Si el asgardiano tiene el poder cósmico, tiene el genotipo **aa**.
2. Si el asgardiano no tiene el poder cósmico, puede tener el genotipo **AA** o **Aa** (pero no **aa**). En ese caso:
    1. Si el asgardiano es progenitor, o hijo/a de, un asgardiano con el poder (genotipo **aa**), entonces
       no puede tener el genotipo **AA**, luego tiene el genotipo **Aa**.
    2. Si no se cumple el punto 2.i., pero tiene progenitores, entonces se calcula la probabilidad de cada
       genotipo posible (es decir, **AA** y **Aa**), en función de las probabilidades de cada genotipo 
       que tienen sus progenitores. Por ejemplo, un descendiente de dos asgardianos con genotipo **Aa** tendrá 
       genotipos (**AA**, **Aa**, **aa**) con probabilidades (0.25, 0.5, 0.25) respectivamente. Como no tiene 
       el poder, las probabilidades se renormalizan a (0.33, 0.66, 0).
    3. Si el asgardiano no tiene poder, ni progenitores, ni hijos con poder (tenga o no hijos sin poder), 
       entonces se asume una probabilidad igual (0.5) para ambos genotipos posibles en dicha circunstancia 
       (**AA** y **Aa**). En realidad la verdadera probabilidad dependería de la abundancia relativa de 
       los 3 genotipos en la población general de Asgard, y, en el caso de tener descendencia conocida, 
       el genotipo de dicha descendencia (muchos hijos sin el poder harían más probable que el progenitor 
       tuviera genotipo **AA** y menos **Aa**, por ejemplo).

## Otros comentarios

* Las probabilidades condicionadas de cada genotipo para un descendiente, en función del genotipo de los
  progenitores, se han precalculado a mano, e introducido fijas en una variable global (WEIGHTS). Se ha hecho
  esto por simplicidad y eficiencia.

* El formato (número de decimales) de las cifras del output se ha dejado por defecto. El enunciado parece insinuar
  que se desean los enteros sin decimales y los floats redondeados a 4 decimales, pero he considerado que si no
  es un requerimiento explícito mejor dejar el output como Python considere por defecto.

* El código (nombres de variables, funciones y clases), y los comentarios están en inglés. Lo primero lo considero
  innegociable. Los comentarios, por otro lado, podrían haber ido en castellano, dado el ámbito del reto, pero he
  cedido a lo que en general considero buena práctica, que es utilizar siempre el inglés.

* El script está alojado en GitHub: https://github.com/isilanes/espublico-tech/tree/master/reto4
