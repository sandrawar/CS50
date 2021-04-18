from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # A is knight or knave and only one of them
    Biconditional(
        AKnight, 
        Not(AKnave)),
    # If A says true (is a knight), and only then, A is both - knight and knave
    Biconditional(
        AKnight, 
        And(
            AKnight,
            AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # A is knight or knave and only one of them
    Biconditional(
        AKnight, 
        Not(AKnave)),
    # B is knight or knave and only one of them
    Biconditional(
        BKnight, 
        Not(BKnave)),
    # If A says true (is a knight), and only then, A and B are both knaves
    Biconditional(
        AKnight, 
        And(
            AKnave, 
            BKnave)) 
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # A is knight or knave and only one of them
    Biconditional(
        AKnight, 
        Not(AKnave)),
    # B is knight or knave and only one of them
    Biconditional(
        BKnight, 
        Not(BKnave)),
    # If A says true (is a knight), and only then, A and B are the same kind (are both knaves or are both knights)
    Biconditional(
        AKnight, 
        Or(
            And(
                AKnight, 
                BKnight), 
            And(
                AKnave, 
                BKnave))),
    # If B says true (is a knight), and only then, A and B are different kinds
    Biconditional(
        BKnight, 
        Or(
            And(
                AKnight, 
                BKnave), 
            And(
                AKnave, 
                BKnight))),
    )

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # A is knight or knave and only one of them
    Biconditional(
        AKnight, 
        Not(AKnave)),
    # B is knight or knave and only one of them
    Biconditional(
        BKnight, 
        Not(BKnave)),
    # C is knight or knave and only one of them
    Biconditional(
        CKnight, 
        Not(CKnave)),
    # If A says true (is a knight), and only then, A is either knight or knave
    Biconditional(
        AKnight, 
        Biconditional(
            AKnight,
            Not(AKnave))),
    # If B says true (is a knight), and only then, we can deduce from what A said, that B is a Knave
    Biconditional(
        BKnight, 
        Implication(
            Biconditional(
                AKnight,
                Not(AKnave)), 
            AKnave)),
    # If B says true (is a knight), and only then, C is a knave
    Biconditional(
        BKnight, 
        CKnave),
    # If C says true (is a knight), and only then, A is a knight
    Biconditional(
        CKnight, 
        AKnight),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
