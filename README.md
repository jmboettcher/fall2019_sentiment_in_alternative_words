# fall2019_sentiment_in_alternative_words
Final project for ling278. See finalproject_janeboettcher.ipynb jupyter notebook for more details

## Overview
For every word a writer chooses to use, there may be other alternative words they could have chosen to describe the very same concept. While these alternative words may have the same conceptual meanings, they could have different sentiments ratings for semantic dimensions such as valence, arousal, and dominance.

This projects allows a user to visually see the valence, arousal, and dominance ratings for words a writer chooses to use, compared to the ratings of these words' most frequent alternatives, across time within a paragraph. It also allows a user to see comparisons at the paragraph level across texts through rating means. The project also allows the user to access information about words with maximum semantic dimension distance from alternatives at both the word and paragraph levels

Bare semantic dimension ratings can give an idea of where on the spectrum of sentiment a word lies. Comparing the words a writer chooses to the words' alternatives could add another dimension of understanding to a writer's stance by helping identify where the word choice positions itself in relation to other words that could refer to the same concept.

In order to identify what alternatives should be looked at, I also implemented a rough way to try to determine word sense based on context words.
