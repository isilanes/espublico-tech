# Globals:
INPUT_FILE = "input.txt"


# Functions:
def main():
    asgardian_family = parse_input()
    asgardian_family.purge_according_to_powerful_offspring()
    asgardian_family.purge_according_to_powerful_parent()

    print(asgardian_family)

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
        self.members[member.name] = member
        self.relationships[member.name] = []

    def add_relationship(self, relationship):
        self.relationships[relationship.parent].append(relationship)

    def children_of(self, member_name):
        """
        Return list of members one parent of whom is 'member_name'.

        :param member_name: name of parent whose children we seek, as string.
        :return: list of Asgardian objects.
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
        :return: list of Asgardian objects (empty if none found).
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
        """Remove AA genotype from offspring whose parents do have the power."""

        for name, member in self.members.items():
            for parent in self.parents_of(name):
                if parent.has_power:
                    member.genotypes["AA"] = False

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
    """Family relationship (parent-offsprint) between two Asgardians."""

    # Constructor:
    def __init__(self, parent, offspring):
        self.parent = parent
        self.offspring = offspring

    # Special methods:
    def __str__(self):
        return "{s.parent} is the parent of {s.offspring}".format(s=self)

class Asgardian:
    """A member of the FamilyTree."""

    # Constructor:
    def __init__(self, name, has_power):
        self.name = name
        self.has_power = has_power

        if has_power:
            self.genotypes = {
                    "aa": True,
                    "Aa": False,
                    "AA": False
                    }
        else:
            self.genotypes = {
                    "aa": False,
                    "Aa": True,
                    "AA": True
                    }

    # Special methods:
    def __str__(self):
        if self.has_power:
            return "{s.name}, who has THE POWER".format(s=self)
        else:
            return "{s.name}, the powerless".format(s=self)



# Main:
if __name__ == "__main__":
    main()
