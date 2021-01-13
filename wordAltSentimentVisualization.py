import pandas as pd
import re
import string
import numpy as np
import mywordtokenizer
from wordSenseByContext import SenseContextWordDict
from nltk.tokenize import sent_tokenize

def createSentimentDF(filename):
    sentiment_df = pd.read_csv(filename, index_col='Word')
    sentiment_df = sentiment_df[['V.Mean.Sum', 'A.Mean.Sum', 'D.Mean.Sum']]
    sentiment_df = sentiment_df.rename(columns={'V.Mean.Sum': 'Valence',
                                                'A.Mean.Sum': 'Arousal',
                                                'D.Mean.Sum': 'Dominance'})
    return sentiment_df

def gutenberg_iterator(filename):
    """Yields paragraphs (as defined simply by multiple
    newlines in a row).

    Parameters
    ----------
    filename : str
        Full path to the file.

    Yields
    ------
    multiline str

    """
    with open(filename) as f:
        contents = f.read()
    for para in re.split(r"[\n\s*]{2,}", contents):
        yield para

def comparison_table(paragraphstring, myDict, sentiment_df):
    """Create a table that represents arousal, valence, and dominance ratings for words and their most frequent
    alternatives across time within a paragraph.

    Parameters
    ----------
    paragraphstring : str
        The string representing the paragraph to convert into a table.

    Returns
    -------
    a dataframe with containing frequency, arousal, valence, and dominance ratings for words and their most
    frequent alternatives. The index numbers in this df represent the word's position in the sentence. Any number
    that is not available will be assigned np.nan.

    """
    paragraph = sent_tokenize(paragraphstring)

    comparison_table_df = pd.DataFrame(columns=['Word', 'WordA', 'WordV', 'WordD', 'MostFreqAlt',
                                                'AltA', 'AltV', 'AltD'])

    for sentstring in paragraph:
        sentence = mywordtokenizer.simple(sentstring)
        for word in sentence:
            newLine = {'Word': word}      # starts a line to be updated with all known information

            if sentiment_df.index.contains(word):
                newLine['WordA'] = sentiment_df.at[word, 'Arousal']
                newLine['WordV'] = sentiment_df.at[word, 'Valence']
                newLine['WordD'] = sentiment_df.at[word, 'Dominance']

            mostFreqAlt = myDict.mostFrequentAlternative(word, sentence)
            if word != mostFreqAlt and not mostFreqAlt is None:
                newLine['MostFreqAlt'] = mostFreqAlt
                if sentiment_df.index.contains(mostFreqAlt):
                    newLine['AltA'] = sentiment_df.at[mostFreqAlt, 'Arousal']
                    newLine['AltV'] = sentiment_df.at[mostFreqAlt, 'Valence']
                    newLine['AltD'] = sentiment_df.at[mostFreqAlt, 'Dominance']

            comparison_table_df = comparison_table_df.append(newLine, ignore_index=True) # add updated line to data frame

    return comparison_table_df

def comparison_table_available_values(table):
    """Update a table with arousal, valence, and dominance ratings for words and their most frequent
    alternatives across time within a paragraph to include only lines that have semantic dimension ratings for both
    the word and a known most frequent alternative.

    Parameters
    ----------
    table : a data frame
        The data frame representing arousal, valence, and dominance ratings for words and their most frequent
        alternatives across time within a paragraph

    Returns
    -------
    a dataframe without unknown ratings for semantic dimensions

    """
    table = table[table.WordA.notnull() &
                  table.WordV.notnull() &
                  table.WordD.notnull() &
                  table.AltA.notnull() &
                  table.AltV.notnull() &
                  table.AltD.notnull()]
    return table

def biggest_differences_words(prunedTable):
    """ Finds the words that are most different from their most frequent alternative across each semantic dimension

    Parameters
    ----------
    prunedTable : a data frame
        The data frame representing arousal, valence, and dominance ratings for words and their most frequent
        alternatives across time within a paragraph

    Returns
    -------
    a dictionary mapping from a semantic dimension to row indexing information about the word with the greatest
    difference for that dimension

    """
    prunedTable = prunedTable.assign(absADiff = (prunedTable['WordA'] - prunedTable['AltA']).abs(),
                                     absVDiff = (prunedTable['WordV'] - prunedTable['AltV']).abs(),
                                     absDDiff = (prunedTable['WordD'] - prunedTable['AltD']).abs())
    biggestDifferencesWords = {'Arousal': prunedTable.loc[prunedTable['absADiff'].idxmax()],
                               'Valence': prunedTable.loc[prunedTable['absVDiff'].idxmax()],
                               'Dominance': prunedTable.loc[prunedTable['absDDiff'].idxmax()]}
    return biggestDifferencesWords

def paragraphAverages(filename, myDict, sentiment_df, stop = -1):
    """Create a table that represents paragraphs' average arousal, valence, and dominance ratings for words and
    their most frequent alternatives across a given text.

    Parameters
    ----------
    filename : string
        The string representing the file name to be read

    (optional): int
        the number of paragraphs the user wants to be measured. Useful, if you don't want to look at the entire file
        but say the first 20 paragraphs. (reduces waiting time). the default is to process everything.

    Returns
    -------
    a dataframe with paragraphs' average arousal, valence, and dominance ratings for words and
    their most frequent alternatives across a given text

    """
    avgs = pd.DataFrame(columns=['WordAAvg', 'WordVAvg', 'WordDAvg', 'AltAAvg', 'AltVAvg','AltDAvg'])
    file_iterator = gutenberg_iterator(filename)
    paragraphNum = 0
    for paragraphstring in file_iterator:
        if stop != -1 and paragraphNum >= stop:
            return avgs
        table = comparison_table(paragraphstring, myDict, sentiment_df)
        availableValTable = comparison_table_available_values(table)
        newLine = {'WordAAvg': availableValTable['WordA'].mean(),
                   'WordVAvg': availableValTable['WordV'].mean(),
                   'WordDAvg': availableValTable['WordD'].mean(),
                   'AltAAvg': availableValTable['AltA'].mean(),
                   'AltVAvg': availableValTable['AltV'].mean(),
                   'AltDAvg': availableValTable['AltD'].mean()}
        avgs = avgs.append(newLine, ignore_index=True)
        paragraphNum+=1
    return avgs

def biggest_differences_paragraphs(table):
    """ Finds the paragraphs with greatest average differences between words and their most frequent alternative
        across each semantic dimension

    Parameters
    ----------
    table : a data frame
        The data frame representing average a paragraph's arousal, valence, and dominance ratings for words and
        their most frequent alternatives across time in a text

    Returns
    -------
    a dictionary mapping from a semantic dimension to a row indexing information about the paragraph with the greatest
    difference for that dimension

    """
    table = table.assign(absAAvgDiff = (table['WordAAvg'] - table['AltAAvg']).abs(),
                         absVAvgDiff = (table['WordVAvg'] - table['AltVAvg']).abs(),
                         absDAvgDiff = (table['WordDAvg'] - table['AltDAvg']).abs())
    biggestDifferencesParagraphs = {'Arousal': table.loc[table['absAAvgDiff'].idxmax()],
                                    'Valence': table.loc[table['absVAvgDiff'].idxmax()],
                                    'Dominance': table.loc[table['absDAvgDiff'].idxmax()]}
    return biggestDifferencesParagraphs

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
