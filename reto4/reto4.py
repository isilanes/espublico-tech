"""
reto4.py: script de Python para resolver el Reto 4 de esPublico.tech (https://espublico.tech/reto/4).

Desde la línea de comandos (en Linux), ejecutar:

$ python3 reto4.py

El script espera un fichero de input en el mismo directorio, llamado literalmente "input.txt". Si se desea
leer otro fichero de input, puede usarse la opción -i:

$ python3 reto4.py -i another_input.txt

Para mostrar una breve ayuda con todas las opciones disponibles:

$ python reto4.py -h
"""

__author__ = "Iñaki Silanes Cristóbal"
__copyright__ = "Copyright 2019, Iñaki Silanes Cristóbal"
__email__ = "isilanes@gmail.com"

# Standard libs:
import sys
import argparse
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
    opts = parse_arguments()
    asgardian_family = build_family_from_input(input_file=opts.input)
    asgardian_family.calculate_genotype_probabilities()
    print(asgardian_family)


def build_family_from_input(input_file):
    """
    Parse input file 'input_file' and return family of Asgardians.

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


def parse_arguments(args=sys.argv[1:]):
    """Parse command-line arguments, if any."""
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-i', '--input',
                        help="Path of input file to read. Default: {d}".format(d=INPUT_FILE),
                        default=INPUT_FILE)
    
    return parser.parse_args(args)


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
        Add a relationship to family graph.
        
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
        :return: generator of Asgardian objects.
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
        """
        Return probabilities of AA, Aa and aa genotypes for member named 'member_name'.
        
        :param member_name: name of Asgardian whose probabilities we seek, as string
        :return: numpy array (pAA, pAa, paa), with probabilities for AA, Aa and aa, respectively
        """
        # For members already calculated (including the ones with power, who automatically have an aa genotype):
        if self.members[member_name].is_already_processed:
            return self.members[member_name].genotype_probabilities

        # Any Asgardian w/o power, and with a parent OR child w/ power, must be genotype Aa.
        if self.any_parent_has_power(member_name) or self.any_child_has_power(member_name):
            return np.array([0, 1, 0])

        # Any Asgardian with neither power, nor parents or children with power, has either genotype AA or Aa.
        # If he or she has parents, the probability will depend on genotype probabilities of parents.
        # If not, then 50/50 is assigned.
        if not self.has_parents(member_name):
            return np.array([0.5, 0.5, 0])

        parent_genotypes = []
        for parent in self.parents_of(member_name):
            parent_genotypes.append(self.genotype_probabilities_of(parent.name))
            
        probs = np.zeros((3,))
        for i in range(3):
            for j in range(3):
                p = parent_genotypes[0][i]*parent_genotypes[1][j]
                w = WEIGHTS[i, j]
                probs += p * w
        
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
            
    def any_parent_has_power(self, member_name):
        """
        Return True if 'member_name' has one or both parents with the power, False otherwise.
        
        :param member_name: name of Asgardians whose parents we inquire about, as string.
        :return: boolean.
        """
        for parent in self.parents_of(member_name):
            if parent.has_power:
                return True
        
        return False
    
    def any_child_has_power(self, member_name):
        """
        Return True if 'member_name' has one or more children with the power, False otherwise.
        
        :param member_name: name of Asgardians whose children we inquire about, as string.
        :return: boolean.
        """
        for child in self.children_of(member_name):
            if child.has_power:
                return True
    
        return False

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
            return "{s.name}, who has the power".format(s=self)
        else:
            return "{s.name}, the powerless".format(s=self)


# Main:
if __name__ == "__main__":
    main()
