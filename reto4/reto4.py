# Standard libs:
import numpy as np


# Globals:
INPUT_FILE = "input.txt"
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
    asgardian_family = parse_input()
    asgardian_family.calculate_genotype_probabilities()
    
    print(asgardian_family)


def parse_input(input_file=INPUT_FILE):
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
    """A directed graph of the family."""

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
