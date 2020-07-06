from CFG import Grammer

G = Grammer([
    5,
    "<START> -> <SUBJECT><DISTANCE><VERB><DISTANCE><OBJECTS>",
    "<SUBJECT> -> i|we",
    "<DISTANCE> ->  ",
    "<VERB> -> eat|drink|go|<OBJECTS><SUBJECT>",
    "<OBJECTS> -> food|water|lamda"
])
# print(G)

G1 = Grammer([
    4,
    "<S> -> a<S>|<A>|<C>",
    "<A> -> a",
    "<B> -> aa",
    "<C> -> a<C>b",
])

# print(G1.ChangeToGreibachForm())

G2 = Grammer([
    5,
    "<S> -> <A><B><C><D>",
    "<A> -> a",
    "<B> -> b",
    "<C> -> c",
    "<D> -> d"
])

# print(G2)
# print(G2.ChangeToChomskyForm())
# print(G2.IsGenerateByGrammer('a b c d'))
