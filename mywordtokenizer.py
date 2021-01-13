"""
Linguist 278: Programming for Linguists
Stanford Linguistics, Fall 2019
Christopher Potts

Assignment 2

Distributed 2019-10-07
Due 2019-10-14

NOTES:

Please submit a modified version of this file, including all the
comments it currently contains.

Your file should not execute any functions when imported as a module
-- all function calls must be placed in the scope of
`if __name__ == '__main__'` at the bottom of this file.

Please name the file ling278_assign02_NAME.py

where NAME is a version of your name containing only letters and/or
underscores. (This will allow me to import your file as a Python
module; more about that later.)
"""

"""===================================================================
1.  [3 points]

Tokenizing. This is one of the most common (and vexing) operations
when processing text data. There is no single correct way to do it; the
correct method will depend on the task at hand.

This problem is designed to give you a sense for the challenges and the
possibilities, but the design of the tokenizer is scoped very tightly,
as described in the documentation for the function.

If the function `test_simple_tokenize` runs with no errors (i.e., it
gives no output when called), then your tokenizer is correct.
"""

def simple(s):
    """Break str `s` into a list of str.

    1. `s` has all of its peripheral whitespace removed.
    1. `s` is downcased with `lower`.
    2. `s` is split on whitespace.
    3. For each token, any peripheral punctuation on it is stripped
       off. Punctuation is here defined by `string.punctuation`.

    Parameters
    ----------
    s : str
        The string to tokenize.

    Returns
    -------
    list of str

    """
    import string
    punct = string.punctuation
    final_toks = []
    toks = s.lower().strip().split()
    for w in toks:
        final_toks.append(w.strip(punct))
    return final_toks


"""===================================================================
Place all function calls below the following conditional so that they
are called only if this module is called with

`python ling278_assign02.py`

No functions should execute if it is instead imported with

import ling278_assign02

in the interactive shell.
"""

if __name__ == '__main__':
    pass
