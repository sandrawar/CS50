import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # Value of joint posibilities of given number of genes/ traits for everyone
    traitProbability = 1
    genesProbability = 1
    # Dictionary matching a number of parent's trait genes (keys) to posibility of his/her child inheriting it (values)
    childTraitGeneProbability = {0:0, 1:0.5, 2:1.0}
    
    # Iterate over people calculating posibility of given for then features
    for person in people.keys():
        
        # Find number of wanted genes for given person
        if person in one_gene:
            genes = 1
        elif person in two_genes:
            genes = 2
        else:
            genes = 0
        
        # Calculate a posibility of having or not having a trait according to given number of genes
        if person in have_trait:
            if people[person]["trait"] == False:
                return 0
            traitProbability *= PROBS["trait"][genes][True]
        else:
            if people[person]["trait"] == True:
                return 0
            traitProbability *= PROBS["trait"][genes][False]
        
        # Calculate a posibility of having given number of genes for person
        mother = people[person]["mother"]
        father = people[person]["father"]
        if mother == None and father == None:
            genesProbability *= PROBS["gene"][genes]
        else:
            if mother in one_gene:
                mumGenes = 1
            elif mother in two_genes:
                mumGenes = 2
            else:
                mumGenes = 0
            if father in one_gene:
                dadGenes = 1
            elif father in two_genes:
                dadGenes = 2
            else:
                dadGenes = 0
            traitFromMumPosibility = childTraitGeneProbability[mumGenes]
            traitFromDadPosibility = childTraitGeneProbability[dadGenes]
            if genes == 0:
                childGene1 = (1 - traitFromMumPosibility) * 0.99 + min(max(traitFromMumPosibility * 0.01, 0), 0.01)
                childGene2 = (1 - traitFromDadPosibility) * 0.99 + min(max(traitFromDadPosibility * 0.01, 0), 0.01)
                childGenes = childGene1 * childGene2
            elif genes == 2:
                childGene1 = traitFromMumPosibility * 0.99 + min(max((1 - traitFromMumPosibility) * 0.01, 0), 0.01)
                childGene2 = traitFromDadPosibility * 0.99 + min(max((1 - traitFromDadPosibility) * 0.01, 0), 0.01)
                childGenes = childGene1 * childGene2
            else:
                childGeneA = traitFromMumPosibility * 0.99 + min(max((1 - traitFromMumPosibility) * 0.01, 0), 0.01)
                childGeneB = (1 - traitFromDadPosibility) * 0.99 + min(max(traitFromDadPosibility * 0.01, 0), 0.01)
                childGeneC = (1 - traitFromMumPosibility) * 0.99 + min(max(traitFromMumPosibility * 0.01, 0), 0.01)
                childGeneD = traitFromDadPosibility * 0.99 + min(max((1 - traitFromDadPosibility) * 0.01, 0), 0.01)
                childGenes = childGeneA * childGeneB + childGeneC * childGeneD
            genesProbability *= childGenes
    
    #return joint posibility of givrn genes and traits for everyone
    return traitProbability * genesProbability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities.keys():
        if person in one_gene:
            genesNumber = 1
        elif person in two_genes:
            genesNumber = 2
        else:
            genesNumber = 0
        if person in have_trait:
            trait = True
        else:
            trait = False
        probabilities[person]["gene"][genesNumber] += p
        probabilities[person]["trait"][trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        genesSum = probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + probabilities[person]["gene"][2]
        traitSum = probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        for i in range(3):
            probabilities[person]["gene"][i] /= genesSum
        probabilities[person]["trait"][True] /= traitSum
        probabilities[person]["trait"][False] /= traitSum



if __name__ == "__main__":
    main()
