from collections import defaultdict
from nltk.tokenize import sent_tokenize
from nltk.corpus import wordnet as wn
from nltk.corpus import semcor as sc
from nltk.corpus import stopwords
import mywordtokenizer

class SenseContextWordDict:

    def __init__(self):
        self.dictionary = self._create_dictionary()

    def _create_dictionary(self):
        dictionary = defaultdict(lambda: defaultdict(int))
        myStopWords = stopwords.words('english')
        for sentence in sc.tagged_sents(tag='sem'):
            plainWordSent = []
            taggedWordSent = []
            self._make_word_lists(plainWordSent, taggedWordSent, sentence)
            for taggedItemTuple in taggedWordSent:
                self._update_tagged_item_entry(myStopWords, dictionary, plainWordSent, taggedItemTuple[0],taggedItemTuple[1])
        return dictionary

    def _make_word_lists(self, plainWordSent, taggedWordSent, sentence):
        for i in range(0,len(sentence)):
            item = sentence[i]
            if(type(item)) == list:
                plainWordSent.append(item[0])
            else:
                if type(item.label()) == str:
                    plainWordSent.append(item.leaves()[0])
                else:
                    plainWordSent.append(item.label().name())
                    taggedWordSent.append([item, i])

    def _update_tagged_item_entry(self, myStopWords,dictionary,plainWordSent,taggedItem,taggedItemPosition):
        for j in range(0,len(plainWordSent)):
            word = plainWordSent[j]
            if taggedItem.label().name() != word:
                taggedSynset = taggedItem.label().synset()
                splitUp = word.split("_")
                for thisword in splitUp:
                    wordTokened = mywordtokenizer.simple(thisword)
                    if len(wordTokened) > 0:
                        word = wordTokened[0]
                        if word not in myStopWords:
                            dictionary[taggedSynset][word]+=1
                            dictionary[taggedSynset][".total."]+=1
                            dictionary[taggedSynset][".totalNoStops."]+=1
                        elif abs(j - taggedItemPosition) == 1:
                            dictionary[taggedSynset][word]+=1
                            dictionary[taggedSynset][".total."]+=1

    def getMostLikelySynset(self, word, sentence):
        """Find the set of a word's synonyms.

        Parameters
        ----------
        word : str
        The string representing a given word.

        Returns
        -------
        a set pf the given word's synonyms.

        """
        myStopWords = stopwords.words('english')
        highestCoverageSyn = self._synset_search(".totalNoStops.", myStopWords, word, sentence)
        if highestCoverageSyn is None:
            highestCoverageSyn = self._synset_search(".total.", [], word, sentence)
        return highestCoverageSyn

    def _synset_search(self, totalToUse, exclusionSet, word, sentence):
        """Find the set of a word's synonyms.

        Parameters
        ----------
        word : str
            The string representing a given word.

        Returns
        -------
        a set pf the given word's synonyms.

        """
        myMap = self.dictionary
        highestCoverage = 0
        highestCoverageSyn = None
        for syn in wn.synsets(word):
            totalContextWordMatches = 0
            totalSet = myMap[syn][totalToUse]
            if totalSet > 0:
                for contextWord in sentence:
                    if contextWord != word and contextWord not in exclusionSet:
                        totalContextWordMatches += myMap[syn][contextWord]
                coverage = totalContextWordMatches / totalSet
                if coverage > highestCoverage:
                    highestCoverage = coverage
                    highestCoverageSyn = syn
        return highestCoverageSyn

    def listAlternatives(self, word, sentence):
        synonyms = set([])
        mostLikelySynset = self.getMostLikelySynset(word, sentence)
        if not mostLikelySynset is None:
            for synonym in mostLikelySynset.lemmas():
                synonyms.add(synonym.name())
        return synonyms

    def mostFrequentAlternative(self, word, sentence):
        mostLikelySynset = self.getMostLikelySynset(word, sentence)
        highestCount = 0
        mostFrequentAlternative = None
        if not mostLikelySynset is None:
            for synonym in mostLikelySynset.lemmas():
                count = synonym.count()
                if count > highestCount:
                    mostFrequentAlternative = synonym.name()
                    highestCount = count
        return mostFrequentAlternative


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
