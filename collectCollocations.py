'''
Originally created (mostly) in May 2023.
Organized and uploaded in July 2023.

To run script:
    python3 collectCollocations.py [corpus_file] {current_directory}
(The current_directory argument is optional.)

corpus_file can be a .txt OR .csv file
(A few examples: CaesarTexts.txt VergilTexts.txt DostoevskyTexts.txt)

Finds collocations that contain more than just a word plus a word that is a stop word (by default, a stop word is a word that is among the 20 most common words). 
Returns bigrams, trigrams, and tetragrams!
'''
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import os

import csv
import string
import re


# from sklearn.preprocessing import PolynomialFeatures
# from sklearn.model_selection import train_test_split

import string
import re


import pkg_resources
# pkg_resources.require("numpy==1.23.5") #https://stackoverflow.com/questions/6445167/force-python-to-use-an-older-version-of-module-than-what-i-have-installed-now
import numpy
import nltk
from nltk import word_tokenize
from nltk import ngrams
from collections import Counter
import random
from collections import Counter

'''
Step 1. Things you have to set.
'''

curr_dir = './'
corpus_file = str(sys.argv[1])
# .txt or .csv file
# the column you want from a csv file (won't matter if it is .txt)
which_column = 5

'''
Step 2. Functions.
'''

# f1


def normalize_text(text):
    full_stops = [".", "!", "?", ".", "•", "*", "*"]
    semi_stops = [",", ";", ":", "]",
                  "[", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    normalized_text = text.lower()
    for punct0 in full_stops:
        normalized_text = normalized_text.replace(punct0, " . ")
    for punct1 in semi_stops:
        normalized_text = normalized_text.replace(punct1, "")

    return normalized_text

# f2


def list_col_names(csv_file, col_list=True, fifth_element=True):
    with open(csv_file) as csv_f:
        # https://www.geeksforgeeks.org/get-column-names-from-csv-using-python/
        csv_reader = csv.reader(csv_f, delimiter=',')
        list_of_column_names = []
        for row in csv_reader:
            list_of_column_names.append(row)
            break
    if col_list == True:
        print("List of column names : ", list_of_column_names[0])
    if fifth_element == True:
        print(list_of_column_names[0][4])
    return list_of_column_names

# f3


def column_to_list(csv_file, column_name):
    column_list = []

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            normalized_row = normalize_text(row[column_name])
            column_list.append(normalized_row)

    return column_list

# f4


def combine_strings_from_list(string_list):
    combined_string = ''.join(string_list)
    return combined_string

# f5
# make obselete by find_ngram_frequencies
# (which makes nltk is an unnecessary import)

# def find_bigram_frequencies(sentence):
#    tokens = word_tokenize(sentence)
#    bigrams = list(nltk.bigrams(tokens))
#    frequency_dict = dict(Counter(bigrams))
#    return frequency_dict

# f6


def find_ngram_frequencies(sentence, n):
    tokens = word_tokenize(sentence)
    ngrams_list = list(ngrams(tokens, n))
    frequency_dict = dict(Counter(ngrams_list))
    return frequency_dict

# f7


def add_dictionaries(dict1, dict2, dict3):
    result = {}
    result.update(dict1)
    result.update(dict2)
    result.update(dict3)
    return result

# f8


def print_dict_sample(dictionary, sample_size):
    sample = random.sample(list(dictionary.items()), sample_size)
    for key, value in sample:
        print(f"Sample from the dictionary: {key}, {value}")

# f9


def print_list_sample(lst, sample_size):
    sample = random.sample(lst, sample_size)
    for i in sample:
        print(f"Sample from the list: {i}")

# f10


def extract_key_value_id(my_dict):
    keys = []
    values = []
    ids = []

    # Extract keys, values, and IDs
    for i, (key, value) in enumerate(my_dict.items(), 1):
        keys.append(key)
        values.append(value)
        ids.append(i)
    return keys, values, ids

# f11
# Combines list of tuples (bg_keys) with bg_values
# so that they can be sorted by the last element in the tuples later


def combine_tuples_with_values(bg_keys, bg_values):
    combined_list = [(*tup, val) for tup, val in zip(bg_keys, bg_values)]
    return combined_list
# Now, we'll use this to sort them by the last element
# (the bigrams will be arranged from most frequent to least frequent)

# f12


def sort_tuples_by_last_element(tuple_list):
    sorted_list = sorted(tuple_list, key=lambda x: x[-1], reverse=True)
    return sorted_list

# f13


def find_most_common_words(text, num_words):
    # Split the text into words using regular expressions
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    word_counts = Counter(words)

    # Get the most common words and their frequencies
    most_common = word_counts.most_common(num_words)
    most_common_words = [word for word, _ in most_common]

    return most_common_words

# f14


def is_only_punctuation(input_str):
    # Remove leading and trailing whitespace from the string
    input_str = input_str.strip()

    # Check if the string is empty after removing whitespace
    if not input_str:
        return False
    targeted_punctuation = string.punctuation+"`"+"-"

    # Check if all characters in the string are punctuation
    return all(char in targeted_punctuation for char in input_str)

# Returns True if the tuple_data is NOT only a tuple containing a stop word and one other word
# Returns False if it is found to be an unwanted ngram

# f15


def check_tuple(tuple_data, stop_words):
    # first, it breaks the condition if there is any punctuation
    for ele in tuple_data:
        if is_only_punctuation(ele):
            return False
    # second, it breaks the condition if either word of 2 is a stop word
    if len(tuple_data) == 2:
        word1, word2 = tuple_data
        if word1 in stop_words:
            return False
        elif word2 in stop_words:
            return False
        else:
            return True
    elif len(tuple_data) > 2:
        return True

# f16


def remove_last_tuple_item(tuple_list):
    new_tuple_list = [tuple[:-1] for tuple in tuple_list]
    return new_tuple_list

# Filters tuples that do not satisfy the check_tuple condition (they should return True)

# f17


def filter_tuples(tuple_list, stop_words):
    nontrivial_frequent_ngrams = []
    frequencies_as_list = []
    for tuple_val in tuple_list:
        if check_tuple(tuple_val, stop_words) == True:
            frequencies_as_list.append(ngram_freqs[tuple_val])
            nontrivial_frequent_ngrams.append(tuple_val)
    return nontrivial_frequent_ngrams, frequencies_as_list

# It's all right if the following function is not used.
# Use it when you need it to troubleshoot.

# f18


def troubleshoot_list(lst):
    items = []
    for item in lst:
        if len(item) > 3:
            if len(items) < 250:
                items.append(item)
    return items


'''
Step 3. Finding collocations.
'''

column_number = which_column-1

# Making list of paragraphs from corpus file
if corpus_file[-4:] == ".txt":
    print("|||||||||||| txt file ||||||||||||")
    with open(corpus_file, 'r') as text:
        text = text.read()
        # normalization: making all letters lowercase, and making periods be treated as separate words
        normalized_text = normalize_text(text)

        paras = normalized_text.split('\n\n')

    i = 0
    while i < 2:
        print(paras[i]+'\n')
        i += 1
elif corpus_file[-4:] == ".csv":
    print("|||||||||||| csv file ||||||||||||")

    list_of_column_names = list_col_names(
        corpus_file, col_list=False, fifth_element=False)
    paras = column_to_list(corpus_file, str(
        list_of_column_names[0][column_number]))

    # prints the first three paragraphs
    i = 0
    for doc in paras:
        if i < 2:
            print(doc, "\n")
        i += 1

    text = combine_strings_from_list(paras)
    normalized_text = normalize_text(text)

else:
    print("ERROR: file must be either csv or text file")

# Trivial words in text: "a", "the", etc.
stop_words = find_most_common_words(normalized_text, 20)

# This can be changed to include more than bigrams
# if the function find_bigram_frequencies is replaced by another function

# Combination of bigrams, trigrams, and quadrigrams
bigram_freqs = find_ngram_frequencies(normalized_text, 2)
trigram_freqs = find_ngram_frequencies(normalized_text, 3)
tetragram_freqs = find_ngram_frequencies(normalized_text, 4)
ngram_freqs = add_dictionaries(bigram_freqs, trigram_freqs, tetragram_freqs)
print_dict_sample(ngram_freqs, 10)

# Finds ngram words (keys), the frequency (values),
# and order as they originally appear in ngram_freqs (ids)
ng_keys, ng_values, ng_ids = extract_key_value_id(ngram_freqs)
print(ng_keys[0:100])
print(ng_values[0:100])
print(ng_ids[0:100])

# Now, we'll find arrange the ng_keys from most frequent to least frequent based on the value
combined_tuple_list = combine_tuples_with_values(
    ng_keys, ng_values)  # adds ng_values to the end of ng_keys tuples
# sorts the resultant ng tuples by last element
ordered_list = sort_tuples_by_last_element(combined_tuple_list)

# Time to get rid of stop words now from 'ordered_list' defined above
# makes list of tuples not containing last element (frequency)
just_ngrams = remove_last_tuple_item(ordered_list)
# 10,000 most frequent ngrams from most common to least
frequent_ngrams = just_ngrams[0:10001]

nontrivial_frequent_ngrams, frequencies_as_list = filter_tuples(
    frequent_ngrams, stop_words)
print(nontrivial_frequent_ngrams[0:100])

'''
Step 4. Saves all collocations to a text file (really a .tsv file).
'''

# Makes a sorted list of ALL the possible collocations I found


def sort_all_collocations(index_numbers, integer_numbers, list_of_tuples):
    combined_list = [(index, number, element) for index, number, element in zip(
        index_numbers, integer_numbers, list_of_tuples)]
    sorted_combined_list = sorted(
        combined_list, key=lambda x: x[1], reverse=True)
    return sorted_combined_list


# This variable is in this order: [(index_number, frequency_number, (collocation_tuples),...]
sorted_collocations = sort_all_collocations(ng_ids, ng_values, ng_keys)

more_than_bigrams = []
# for collocation in sorted_collocations:
#    if len(collocation[2]) > 2:
#        if not len(more_than_bigrams) > 250:
#            more_than_bigrams.append(collocation)
# print(more_than_bigrams)

# Write to a text file (this will look the same as output.txt for smaller datasets)
full_collocation_text = "NewOrder\tOriginalOrder\tFrequency\tCollocation\n"

i = 0
for line in sorted_collocations:
    full_collocation_text += f"{i}\t{line[0]}\t{line[1]}\t{line[2]}\n"
    # if i > 1000:
    #    print(f"{i}\t{line[0]}\t{line[1]}\t{line[2]}\n")
    # if len(tpl) > 2:
    #    more_than_bigrams.append(tpl)
    i += 1

text_file = open(f"{curr_dir}all_collocations.txt", "w")
text_file.write(full_collocation_text)
text_file.close()


# Now, we can also graph the two axes! (with the same code as the graphing script)
def power_law(x, a, b):
    return a * np.power(x, b)


def graph_lists(x_list, y_list):
    x = np.array(x_list)
    y = np.array(y_list)
    params, covariance = curve_fit(power_law, x, y)
    x_fit = np.linspace(min(x), max(x), 100)
    y_fit = power_law(x_fit, params[0], params[1])
    plt.scatter(x, y, label='Original Data')
    plt.plot(x_fit, y_fit, 'r-', label='Fitted Power Law Curve')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.title('Power Law Fit')
    plt.grid(True)
    plt.show()
    fitted_a, fitted_b = params
    print(f"Fitted parameters: a = {fitted_a}, b = {fitted_b}")


'''
Step 5. Saves "non-trivial" collocations to a text file called "output.txt" as well as a csv file called "output.csv"
'''

# Saves filtered n-grams from text to output files
final_text = ""
final_csv_text = ""

i = 0
for tupleitem in nontrivial_frequent_ngrams:
    line = str(frequencies_as_list[i])+","
    for number in range(0, len(tupleitem)):
        line += tupleitem[number]+","
    final_csv_text += f"{line}\n"
    i += 1

j = 0
for tupleitem in nontrivial_frequent_ngrams:
    line = str(frequencies_as_list[j])+" "
    for number in range(0, len(tupleitem)):
        if number == len(tupleitem)-1:  # prevents comma at the end of a line
            line += tupleitem[number]
        else:
            line += tupleitem[number]+","
    final_text += f"{line}\n"
    j += 1

text_file0 = open("output.txt", "w")
text_file0.write(final_text)
text_file0.close()

text_file1 = open("output.csv", "w")
text_file1.write(final_csv_text)
text_file1.close()
