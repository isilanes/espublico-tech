"""
reto4.py: script de Python para resolver el Reto 4 de esPublico.tech (https://espublico.tech/reto/4).

# Uso

Desde la línea de comandos (en Linux), ejecutar:

$ python3 reto4.py

El script espera un fichero de input en el mismo directorio, llamado literalmente "input.txt",
y con el siguiente formato:

Bor[0]
Bestla[0]
Ve[0]=Bor+Bestla
Odin[1]=Bor+Bestla
Jord[0]
etc

El script produce el output requerido por pantalla, con el formato:

Bor=AA[0],Aa[1],aa[0]
Bestla=AA[0],Aa[1],aa[0]
Ve=AA[0.3333333333333333],Aa[0.6666666666666666],aa[0.0]
Odin=AA[0],Aa[0],aa[1]
Jord=AA[0],Aa[1],aa[0]
etc

# Requerimientos

Python 3.x
numpy

Realmente funciona también con Python 2.7 (necesitaría la línea '# -*- coding=utf-8 -*-' al principio), pero
se ha desarrollado con solo Python 3.x en mente.

El uso de numpy obedece únicamente a un interés por la sencillez y la comodidad, no a la eficiencia. Considero numpy
suficiente ubicuo como para no verme impulsado a prescindir de él en aras de la compatibilidad.

# Funcionamiento y algoritmo

Las relaciones entre familiares Asgardianos se han modelado con un grafo dirigido, en el que cada nodo es un
miembro, y cada relación una arista señalando de progenitor a descendiente.

Se ha procesado cada miembro asgardiano con el siguiente algoritmo para decidir sobre la probabilidad
de tener cada genotipo:

1. Si el asgardiano tiene el poder cósmico, tiene el genotipo aa.
2. Si el asgardiano no tiene el poder cósmico, puede tener el genotipo AA o Aa (pero no aa). En ese caso:
   2.1. Si el asgardiano es progenitor, o hijo/a de, un asgardiano con el poder (genotipo aa), entonces
        no puede tener el genotipo AA, luego tiene el genotipo Aa.
   2.2. Si no se cumple el punto 2.1., pero tiene progenitores, entonces se calcula la probabilidad de cada genotipo
        posible (es decir, AA y Aa), en función de las probabilidades de cada genotipo que tienen sus progenitores.
        Por ejemplo, un descendiente de dos asgardianos con genotipo Aa tendrá genotipos (AA, Aa, aa) con probabilidades
        (0.25, 0.5, 0.25) respectivamente. Como no tiene el poder, las probabilidades se renormalizan a (0.33, 0.66, 0).
   2.3. Si el asgardiano no tiene poder, ni progenitores, ni hijos con poder (tenga o no hijos sin poder), entonces
        se asume una probabilidad igual (0.5) para ambos genotipos posibles en dicha circunstancia (AA y Aa). En
        realidad la verdadera probabilidad dependería de la abundancia relativa de los 3 genotipos en la población
        general de Asgard, y, en el caso de tener descendencia conocida, el genotipo de dicha descendencia (muchos
        hijos sin el poder harían más probable que el progenitor tuviera genotipo AA y menos Aa, por ejemplo).

# Otras consideraciones

* Las probabilidades condicionadas de cada genotipo para un descendiente, en función del genotipo de los
  progenitores, se han precalculado a mano, e introducido fijas en una variable global (WEIGHTS). Se ha hecho
  esto por simplicidad y eficiencia.

* El formato (número de decimales) de las cifras del output se ha dejado por defecto. El enunciado parece insinuar
  que se desean los enteros sin decimales y los floats redondeados a 4 decimales, pero he considerado que si no
  es un requerimiento explícito mejor dejar el output como Python considere por defecto.

* El código (nombres de variables, funciones y clases), y los comentarios están en inglés. Lo primero lo considero
  innegociable. Los comentarios, por otro lado, podrían haber ido en castellano, dado el ámbito del reto, pero he
  cedido a lo que en general considero buena práctica, que es utilizar siempre el inglés.
"""

__author__ = "Iñaki Silanes Cristóbal"
__copyright__ = "Copyright 2019, Iñaki Silanes Cristóbal"
__email__ = "isilanes@gmail.com"

# Standard libs:
import numpy as np


# Globals:
INPUT_FILE = "input.txt"

# WEIGHTS[i, j] = [pAA, pAa, paa], where:
# i = either 0, 1 or 2, for parent A having genotype AA, Aa or aa, respectively
# j = either 0, 1 or 2, for parent B having genotype AA, Aa or aa, respectively
# pAA = probability of child having genotype AA
# pAa = probability of child having genotype Aa
# paa = probability of child having genotype aa
WEIGHTS = np.array([
    [
        [1, 0, 0],
        [0.5, 0.5, 0],
        [0, 1, 0]
    ],
    [
        [0.5, 0.5, 0],
        [0.25, 0.5, 0.25],
        [0, 0.5, 0.5]
    ],
    [
        [0, 1, 0],
        [0, 0.5, 0.5],
        [0, 0, 1]
    ],
])


# Functions:
def main():
    asgardian_family = get_family_from_input()
    asgardian_family.calculate_genotype_probabilities()
    print(asgardian_family)


def get_family_from_input(input_file=INPUT_FILE):
    """
    Parse input file 'input_file' and return list of Asgardians.

    :param input_file: full path of input file, as string
    :return: FamilyGraph object, populated with Asgardian objects
    """
    family = FamilyGraph()

    with open(input_file) as f:
        for line in f:

            # Parse line:
            pre, post = None, None
            line = line.strip()
            if "=" in line:
                pre, post = line.split("=")
            else:
                pre = line

            # Get Asgardian info:
            name = pre[:-3]
            has_power = pre[-3:] == "[1]"
            asgardian = Asgardian(name, has_power)

            # Get parents info, if any:
            parents = []
            if post is not None:
                parents = post.split("+")

            # Add to FamilyGraph:
            family.add_member(asgardian)
            for parent in parents:
                relationship = FamilyRelationship(parent, asgardian.name)
                family.add_relationship(relationship)

    return family


# Classes:
class FamilyGraph:
    """A directed graph representing an Asgardian family."""

    # Constructor:
    def __init__(self):
        self.members = {}
        self.relationships = {}

    # Public methods:
    def add_member(self, member):
        """
        Add a member to family graph.
        
        :param member: family member to add, as Asgardian object
        :return: None
        """
        self.members[member.name] = member
        self.relationships[member.name] = []

    def add_relationship(self, relationship):
        """
        Add a relationship object to family graph.
        
        :param relationship: a relationship between two members, as a Relationship object
        :return: None
        """
        self.relationships[relationship.parent].append(relationship)

    def children_of(self, member_name):
        """
        Return list of members one parent of whom is 'member_name'.

        :param member_name: name of parent whose children we seek, as string.
        :return: generator of Asgardian objects.
        """
        for relationship in self.relationships[member_name]:
            yield self.members[relationship.child]

    def children_names_of(self, member_name):
        """
        Return list of members one parent of whom is 'member_name'.

        :param member_name: name of parent whose children we seek, as string.
        :return: list of names, as strings.
        """
        return [c.name for c in self.children_of(member_name)]

    def parents_of(self, member_name):
        """
        Return list of parents of 'member_name', or empty list if none known.

        :param member_name: name of child whose parents we seek.
        :return: generator Asgardian objects (empty if none found).
        """
        for parent_name, parent in self.members.items():
            for relationship in self.relationships[parent_name]:
                if relationship.child == member_name:
                    yield parent

    def has_parents(self, member_name):
        for _ in self.parents_of(member_name):
            return True

        return False

    def genotype_probabilities_of(self, member_name):
        if self.members[member_name].is_already_processed:
            return self.members[member_name].genotype_probabilities

        # Any Asgardian w/o power, and with a parent w/ power must be genotype Aa.
        for parent in self.parents_of(self.members[member_name].name):
            if parent.has_power:
                self.members[member_name].genotype_probabilities = [0, 1, 0]
                return self.members[member_name].genotype_probabilities

        # Any Asgardian w/o power, and with a child w/ power must be genotype Aa.
        for child in self.children_of(self.members[member_name].name):
            if child.has_power:
                self.members[member_name].genotype_probabilities = [0, 1, 0]
                return self.members[member_name].genotype_probabilities

        # Any Asgardian with neither power, nor parents or children with power, has either genotype AA or Aa.
        # If he or she has parents, the probability will depend on genotype probabilities of parents.
        # If not, then 50/50 is assigned.
        if not self.has_parents(member_name):
            self.members[member_name].genotype_probabilities = [0.5, 0.5, 0]
            return self.members[member_name].genotype_probabilities

        parent_genotypes = []
        for parent in self.parents_of(member_name):
            parent_genotypes.append(self.genotype_probabilities_of(parent.name))
            
        probs = np.zeros((3,))
        for i in range(3):
            for j in range(3):
                p = parent_genotypes[0][i]*parent_genotypes[1][j]
                v = WEIGHTS[i, j]
                probs += p*v
        
        # Since we don't have the power, probability of aa is 0:
        probs[2] = 0
        
        # Renormalize:
        probs /= sum(probs)
        
        return probs
    
    def calculate_genotype_probabilities(self):
        """
        Process members one by one (and, implicitly, recursively), to calculate their
        genotype probabilities.
        
        :return: None
        """
        for name, member in self.members.items():
            member.genotype_probabilities = self.genotype_probabilities_of(name)

    # Special methods:
    def __str__(self):
        return "\n".join([m.output_line for m in self.members.values()])
        

class FamilyRelationship:
    """Family relationship (parent-child) between two Asgardians (i.e., graph edge)."""

    # Constructor:
    def __init__(self, parent, child):
        self.parent = parent
        self.child = child

    # Special methods:
    def __str__(self):
        return "{s.parent} is the parent of {s.child}".format(s=self)


class Asgardian:
    """A member of the FamilyGraph (i.e. graph node)."""

    # Constructor:
    def __init__(self, name, has_power):
        self.name = name
        self.has_power = has_power
        self.genotype_probabilities = None

        if has_power:
            self.genotype_probabilities = np.array([0, 0, 1])

    # Public properties:
    @property
    def output_line(self):
        """Return formatted output line, with required info and format."""
        
        if self.genotype_probabilities is None:
            return "{s.name}=None".format(s=self)

        return "{0}=AA[{1}],Aa[{2}],aa[{3}]".format(self.name, *self.genotype_probabilities)

    @property
    def is_already_processed(self):
        """Whether genotype probabilities have been already calculated or not."""

        return self.genotype_probabilities is not None

    # Special methods:
    def __str__(self):
        if self.has_power:
            return "{s.name}, who has THE POWAA".format(s=self)
        else:
            return "{s.name}, the powerless".format(s=self)


# Main:
if __name__ == "__main__":
    main()
