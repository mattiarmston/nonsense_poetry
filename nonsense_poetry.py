#!/usr/bin/env python

import random

# Markov Chain
# This is the transition matrix I am trying to represent
#
#              Adjective  Adverb  Noun  Preposition  Pronoun  Verb
# Adjective    0.5        0       0.5   0            0        0
# Adverb       0          0       0.4   0            0.3      0.3
# Noun         0          0.15    0     0.15         0        0.7
# Preposition  0.5        0       0.5   0            0        0
# Pronoun      0          0.25    0     0.25         0        0.5
# Verb         0.1        0.6     0.2   0            0.1      0

transition_matrix = [
    [0.5,  0,     0.5,  0,     0,    0],
    [0,    0,     0.4,  0,     0.3,  0.3],
    [0,    0.15,  0,    0.15,  0,    0.7],
    [0.5,  0,     0.5,  0,     0,    0],
    [0,    0.25,  0,    0.25,  0,    0.5],
    [0.1,  0.6,   0.2,  0,     0.1,  0],
]

states = [
    "adjective", "adverb", "noun", "preposition", "pronoun", "verb"
]

# This could be improved by moving the words into external files
words = {
    "adjective": ["tall", "quick", "slow", "great", "small", "impressive",
        "small", "withering", "growing", "flaming"],
    "adverb": ["quickly", "slowly", "tearfully", "hopefully", "coldly",
        "warmly"],
    "determiner": ["the", "a", "one", "the first", "the last"],
    "noun": ["mountain", "store", "village", "gold", "forest", "valley", "hero",
        "villain", "traveller"],
    "preposition": ["into", "through", "above", "past"],
    "pronoun": ["he", "she", "it"],
    "verb": ["runs", "laughs", "cries", "smiles", "moves", "walks", "lives",
        "withers", "grows", "sleeps", "wakes"],
}

def check_matrix(transition_matrix):
    for row in transition_matrix:
        total = 0
        for chance in row:
            total += chance
        # This is due to floating point precision errors in python
        if total < 0.99999:
            print("Error: incorrectly configured matrix (row {})"
                  .format(transition_matrix.index(row) + 1))
            quit()
    return

def get_start_state():
    while True:
        state = random.choice(states)
        if state not in ["verb"]:
            return state

def get_next_state(current):
    index = states.index(current)
    row = transition_matrix[index]
    # Returns random floating point 0 to 1
    num = random.random()
    i = 0
    while num > 0:
        num -= row[i]
        i += 1
    next_index = i - 1
    return states[next_index]

def get_word(state):
    word = random.choice(words[state])
    return word

def generate_states():
    states = []
    state = get_start_state()
    min_length = random.randint(3, 10)
    # Reformat into list comprehension?
    i = 0
    while True:
        states.append(state)
        i += 1
        # Sentences should not end with adjectives or prepositions
        if i >= min_length and state not in ["adjective", "preposition"]:
            break
        state = get_next_state(state)
    return states

def add_determiners(states):
    i = 0
    while i < len(states):
        if states[i] == "noun":
            j = i - 1
            # The determiner needs to be added before the first adjective
            # e.g. (One) small quick hero
            while states[j] == "adjective":
                j -= 1
            states.insert(j + 1, "determiner")
            # The sentence length has now increased by one and the index of the
            # noun, which was previously n, is now n + 1. If we do not increase
            # the index here, the next loop will detect the same noun we just
            # found and add another determiner creating an infinite loop.
            i += 1
        i += 1
    return states

def validate_states(states):
    # A sentence must have a verb and a subject
    if "noun" not in states and "pronoun" not in states:
        return False
    if "verb" not in states:
        return False
    # By default the number of verbs and nouns or pronouns should be equal but
    # in some cases there should be more nouns or verbs
    # A preposition requires a subject and object so 1 more noun must be present
    # for each preposition
    no_verbs = states.count("verb") + states.count("preposition")
    no_subjects = states.count("noun") + states.count("pronoun")
    if no_verbs != no_subjects:
        return False
    return True

def get_punctuation(states, i, sentence_start):
    # The purpose of this is to add full stops after sentences
    # As such this needs to detect when a sentence ends
    sentence = states[sentence_start:i]
    # A sentence must have a verb and subject
    if "verb" not in sentence:
        return " ", sentence_start
    if "noun" not in sentence and "pronoun" not in sentence:
        return " ", sentence_start
    # A preposition requires a subject and object so 1 more noun must be present
    # for each preposition
    no_verbs = sentence.count("verb") + sentence.count("preposition")
    no_subjects = sentence.count("noun") + sentence.count("pronoun")
    if no_verbs != no_subjects:
        return " ", sentence_start
    # If this is the final word it should have a full stop.
    try:
        next = states[i]
    except IndexError:
        return ".", i
    # If the last word is an adverb add it to the current sentence, since there
    # is no next one.
    if i == len(states) - 1 and next == "adverb":
        return " ", sentence_start
    # If the sentence has an adverb already it can be finished. Any trailing
    # adverbs will be part of the next sentence
    if "adverb" in sentence:
        return ". ", i
    # If an adverb or preposition is the next word, it should be included in
    # the current sentence, anything else should not
    if next not in ["adverb", "preposition"]:
        return ". ", i
    return " ", sentence_start

def caplitalise(line):
    original = line
    line = line[0].upper() + line[1:]
    i = 0
    for char in original:
        if char == ".":
            # This assumes that every sentence ends with ". "
            index = i + 2
            # In this case index is not a valid index and we have found the end
            # of the line, we could equally 'break' or 'continue' here
            if index > len(original) - 1:
                continue
            line = line[0:index] + line[index].upper() + line[index+1:]
        i += 1
    return line

def generate_line(states):
    line = ""
    sentence_start = 0
    i = 1
    for state in states:
        punctuation, sentence_start = get_punctuation(states, i, sentence_start)
        line += get_word(state) + punctuation
        i += 1
    line = caplitalise(line)
    return line

def get_line():
    states = []
    while not validate_states(states):
        states = generate_states()
    states = add_determiners(states)
    line = generate_line(states)
    return line

def main():
    check_matrix(transition_matrix)
    lines = [get_line() for _ in range(random.randint(1, 5))]
    for line in lines:
        print(line)

main()
