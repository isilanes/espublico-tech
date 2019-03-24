# Globals:
INPUT_FILE = "input.txt"
WEIGHTS = {
    "AAAA": {"AA": 1.0},
    "AAAa": {"AA": 0.5, "Aa": 0.5},
    "AaAA": {"AA": 0.5, "Aa": 0.5},
    "aaAA": {"Aa": 1.0},
    "AAaa": {"Aa": 1.0},
    "AaAa": {"AA": 0.25, "Aa": 0.5, "aa": 0.25},
    "Aaaa": {"Aa": 0.5, "aa": 0.5},
    "aaAa": {"Aa": 0.5, "aa": 0.5},
    "aaaa": {"aa": 1.0},
}


# Functions:
def main():
    asgardian_family = parse_input()
    asgardian_family.purge_according_to_powerful_offspring()
    asgardian_family.purge_according_to_powerful_parent()
    asgardian_family.print_genotype_probabilities()

    for name, member in asgardian_family.members.items():
        if member.is_already_processed:
            pass


def parse_input(input_file=INPUT_FILE):
    """
    Parse input file 'input_file' and return list of Asgardians.

    :param input_file: full path of input file, as string
    :return: FamilyTree object, populated with Asgardian objects
    """
    family = FamilyTree()

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

            # Add to FamilyTree:
            family.add_member(asgardian)
            for parent in parents:
                relationship = FamilyRelationship(parent, asgardian.name)
                family.add_relationship(relationship)

    return family


# Classes:
class FamilyTree:
    """A directed graph of the family."""

    # Constructor:
    def __init__(self):
        self.members = {}
        self.relationships = {}

    # Public methods:
    def add_member(self, member):
        """Add an Asgardian object to FamilyTree."""

        self.members[member.name] = member
        self.relationships[member.name] = []

    def add_relationship(self, relationship):
        """Add a FamilyRelationship object to FamilyTree."""

        self.relationships[relationship.parent].append(relationship)

    def children_of(self, member_name):
        """
        Return list of members one parent of whom is 'member_name'.

        :param member_name: name of parent whose children we seek, as string.
        :return: generator of Asgardian objects.
        """
        for relationship in self.relationships[member_name]:
            yield self.members[relationship.offspring]

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

        :param member_name: name of offspring whose parents we seek.
        :return: generator Asgardian objects (empty if none found).
        """
        for parent_name, parent in self.members.items():
            for relationship in self.relationships[parent_name]:
                if relationship.offspring == member_name:
                    yield parent

    def parent_names_of(self, member_name):
        """
        Return list of parents of 'member_name', or empty list if none known.

        :param member_name: name of offspring whose parents we seek.
        :return: list names, as strings (empty if none found).
        """
        return [p.name for p in self.parents_of(member_name)]

    def purge_according_to_powerful_offspring(self):
        """Remove AA genotype from parents whose children do have the power."""

        for name, member in self.members.items():
            for child in self.children_of(name):
                if child.has_power:
                    member.genotypes["AA"] = False
                    break

    def purge_according_to_powerful_parent(self):
        """Remove AA genotype from members one or both of whose parents do have the power."""

        for name, member in self.members.items():
            for parent in self.parents_of(name):
                if parent.has_power:
                    member.genotypes["AA"] = False
                    break

    def print_genotype_probabilities(self):
        """Calculate and print genotype probabilities for each member, based on parents and self."""

        for name, member in self.members.items():
            # Powerful Asgardians have 100% probability aa:
            if member.genotypes["aa"]:
                member.genotype_probabilities = [0, 0, 1]
                print(member.output_line)
                continue

            # Asgardians who have only one of AA and Aa:
            if member.genotypes["Aa"] and not member.genotypes["AA"]:
                member.genotype_probabilities = [0, 1, 0]
                print(member.output_line)
                continue

            if member.genotypes["AA"] and not member.genotypes["Aa"]:
                member.genotype_probabilities = [1, 0, 0]
                print(member.output_line)
                continue

            # Asgardians who have both AA and Aa, depend on genotype of parents:
            possibilities = []
            for parent in self.parents_of(name):
                genotypes = [g for g in ["AA", "Aa", "aa"] if parent.genotypes[g]]
                possibilities.append(genotypes)

            # Combinations only generated if parents exist above:
            if possibilities:
                accumulated = [0, 0, 0]
                firsts, seconds = possibilities
                for first in firsts:
                    for second in seconds:
                        combo = first+second
                        w = WEIGHTS[combo]
                        for g in w:
                            if not member.genotypes[g]:
                                w[g] = 0
                        norm = sum([x for x in w.values()])
                        if norm:
                            for k in w:
                                w[k] /= norm
                            accumulated[0] += w.get("AA", 0)
                            accumulated[1] += w.get("Aa", 0)
                            accumulated[2] += w.get("aa", 0)

                accumulated[0] /= len(firsts)*len(seconds)
                accumulated[1] /= len(firsts)*len(seconds)
                accumulated[2] /= len(firsts)*len(seconds)
                member.genotype_probabilities = accumulated
                print(member.output_line)
                continue

            # Asgardians with no parents are given 50/50 probability for AA/Aa:
            member.genotype_probabilities = [0.5, 0.5, 0]
            print(member.output_line)

    # Special methods:
    def __str__(self):
        output_lines = []
        for name, member in self.members.items():
            children = self.children_names_of(name)
            if children:
                line = "{m}, parent of {c}".format(m=member, c=", ".join(children))
            else:
                line = "{m}, with no children".format(m=member)
            line += " -> {G}".format(G=", ".join([g for g in member.genotypes if member.genotypes[g]]))
            output_lines.append(line)

        return "\n".join(output_lines)


class FamilyRelationship:
    """Family relationship (parent-offspring) between two Asgardians (i.e., graph edge)."""

    # Constructor:
    def __init__(self, parent, offspring):
        self.parent = parent
        self.offspring = offspring

    # Special methods:
    def __str__(self):
        return "{s.parent} is the parent of {s.offspring}".format(s=self)


class Asgardian:
    """A member of the FamilyTree (i.e. graph node)."""

    # Constructor:
    def __init__(self, name, has_power):
        self.name = name
        self.has_power = has_power
        self.is_already_processed = False
        self.genotype_probabilities = [None, None, None]

        if has_power:
            self.genotypes = {"aa": True, "Aa": False, "AA": False}
            self.is_already_processed = True
        else:
            self.genotypes = {"aa": False, "Aa": True, "AA": True}

    # Public properties:
    @property
    def output_line(self):
        """Return formatted output line, with required info and format."""

        AA, Aa, aa = self.genotype_probabilities

        return "{s.name}=AA[{AA}],Aa[{Aa}],aa[{aa}]".format(s=self, AA=AA, Aa=Aa, aa=aa)

    # Special methods:
    def __str__(self):
        if self.has_power:
            return "{s.name}, who has THE POWAA".format(s=self)
        else:
            return "{s.name}, the powerless".format(s=self)


# Main:
if __name__ == "__main__":
    main()
