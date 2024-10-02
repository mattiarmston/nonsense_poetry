# Nonsense poetry

A poem generator inspired by JDH to create nonsense / surreal poetry.

Similar to his implementation it uses Markov Chains to randomly choose the
next word. However, the program will choose a random word class and then choose
a word from that word class in the hopes that it produces a more intelligible
poem.

##### Table of contents:

- [Goal](#goal)
- [Design](#design)
    - [Word classes](#word-classes)
    - [Markov Chains](#markov-chains)
- [Improvements](#improvements)

## Goal

The goal of the program is to generate comprehensible if meaningless sentences
that imitate nonsense and surreal poetry. The quality of the poetry generated is
not a large concern, in part due to the difficulty of judging this, only that it
is comprehensible. The major difficult in this comes from lines such as

> Conspiring with him how to load and bless \
> &nbsp; With fruit the vines ..
>
> -- John Keats *To Autumn*

which posses a certain poetic quality through breaking grammatical rules but are
still easy to understand. This is difficult to program since there are far more
ways of breaking the rules badly than creatively. I will permit some non
standard word ordering such as verb subject word order and flexibility in where
adverbs appear in sentences. However, I will mainly focus on using poetic
language and imagery to imitate poetry.

## Design

This program relies on a few assumptions:

1. Every word is member of a word class (e.g. 'the' is a determiner, 'run' is a
   verb)
2. A sentence can be abstracted to a sequence of word classes (e.g. 'The cat sat
   on the mat' would be 'determiner noun verb preposition determiner noun'
3. Replacing a word with another from the same word class still produces a
   grammatically correct, if nonsensical, sentence (e.g. 'The cat sat on the
   mat' would be equivalent to 'An athlete jumped over the bar')
4. There are rules about which word classes can follow each other and these can
   be used to construct grammatically correct, if nonsensical, sentences.

The program then seeks to use these rules to construct sequences of word
classes, then for each word class, a random word is picked – to imitate poetry.

### Word classes

The 6 main word classes in English are:

- Adjectives
- Adverbs
- Nouns
- Prepositions
- Pronouns
- Verbs
- Conjunctions (unused)
- Determiners (unused)

Determiners and conjunctions are removed to reduce complexity. Determiners are
omitted since coherent sentences can still be generated without them and
conjunctions can be replaced with full stops and new sentences so they can also
be removed. 

### Markov Chains

Markov Chains are used to randomly pick the next word class based on the
previous one. Each word class is connected to every other with a weighting,
which can be from 0 to 1, but the sum of all weightings for a word class should
be 1 (an example is below). To choose the next state, it is randomly chosen
using the weighting of the previous state. For example, if the previous word was
a pronoun then the next word has a 50% chance of being a verb, 25% for an adverb
and 25% for a preposition.

This is an example Markov Chain for each state; the probabilities have changed
for the final version, but are similar. Probabilities that are 0 have been
omitted. The initial state can be any but the final state should not be an
adjective or preposition (since these would not generate coherent sentences).

Adjective:
- noun - 1

Adverb:
- pronoun - 0.4
- noun - 0.3
- verb - 0.3

Noun:
- verb - 0.5
- adverb - 0.25
- preposition - 0.25

Preposition:
- noun - 0.5
- adjective - 0.5

Pronoun:
- verb - 0.5
- adverb - 0.25
- preposition - 0.25

Verb:
- adverb - 0.6
- noun - 0.2
- pronoun - 0.1
- adjective - 0.1

## Improvements

One of the main issues the program has is generating trailing adverbs. Some
sentences end with an adverb, which is valid in some circumstances. The current
punctuation algorithm decides that the trailing adverb should be the first word
in the next sentence. However this sentence does not exist so the adverb ends up
as a solitary word, this could be fixed by improving the punctuation algorithm
to include it as part of the final sentence.

The quality of the program's output is also inconsistent. Whilst it is usually
comprehensible, it is often meaningless and uninteresting. This could be
improved with a better word choice algorithm, for example comparing which nouns
would be appropriate for which verbs, and an improved word list.

The world lists are currently part of the source code, this could be improved by
moving them into external files which are then read from. Even further,
configuration options could be added to change which files are read from.

