import csv
import os
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np  # linear algebra
curr_dir = './'
corpus_file = ""  # csv or txt file

# how to read in a text file:
# https://learn.theprogrammingfoundation.org/programming/python/file-handling/?gclid=CjwKCAjw36GjBhAkEiwAKwIWySq9-2bHtWUFPuXBtYhP4wUpw0jmXOld-5uOs1vnaWeS9osHx2Xq8RoCKDgQAvD_BwE
corpus_file = '/kaggle/input/brown-corpus/brown.csv'


def normalize(text):
    full_stops = [".", "!", "?", ".", "•", "*", "*"]
    semi_stops = [",", ";", ":", "]", "[", "''", "0",
                  "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    normalized_text = text.lower()
    for punct0 in full_stops:
        normalized_text = normalized_text.replace(punct0, " . ")
    for punct1 in semi_stops:
        normalized_text = normalized_text.replace(punct1, "")

    return normalized_text


if corpus_file[-4:] == ".txt":
    print("|||||||||||| txt file ||||||||||||")
    with open(corpus_file, 'r') as text:
        text = text.read()
        # normalization: making all letters lowercase, and making periods be treated as separate words
        normalized_text = normalize(text)
        # normalized_text = final_text.lower()
        # for punct0 in full_stops:
        #    normalized_text = normalized_text.replace(punct0, " . ")
        # for punct1 in semi_stops:
        #    normalized_text = normalized_text.replace(punct1, "")

        paras = normalized_text.split('\n\n')

    i = 0
    while i < 3:
        print(paras[i]+'\n')
        i += 1
elif corpus_file[-4:] == ".csv":
    print("|||||||||||| csv file ||||||||||||")

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

    def column_to_list(csv_file, column_name):
        column_list = []

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                normalized_row = normalize(row[column_name])
                column_list.append(normalized_row)

        return column_list

    list_of_column_names = list_col_names(
        corpus_file, col_list=False, fifth_element=False)
    paras = column_to_list(corpus_file, str(list_of_column_names[0][4]))

    i = 0
    for doc in paras:
        if i < 3:
            print(doc, "\n")
        i += 1

else:
    print("ERROR: file must be either csv or text file")

'''
Getting features with scikit learn:
'''
print(f"Number of paragraphs: {len(paras)}")
vectorizer = CountVectorizer(analyzer='word', ngram_range=(1, 6), min_df=.01)
x_train = paras
cv_fit = vectorizer.fit_transform(x_train)  # where x_train is a list
feat_dict = vectorizer.vocabulary_.keys()
print(sorted(feat_dict)[100])

print(sorted(feat_dict)[0:10])

'''
Making dictionary with the words and their frequencies
'''
# https://stackoverflow.com/questions/27488446/how-do-i-get-word-frequency-in-a-corpus-using-scikit-learn-countvectorizer
word_list = vectorizer.get_feature_names_out()
count_list = cv_fit.toarray().sum(axis=0)

countdict = dict(zip(word_list, count_list))

'''
Replace variable andword value with the word for "and" in language you're looking at
'''
# sorts: https://stackoverflow.com/questions/10695139/sort-a-list-of-tuples-by-2nd-item-integer-value
# regexes: https://stackoverflow.com/questions/26985228/python-regular-expression-match-multiple-words-anywhere
w_and = 1
andword = 'and'

firstregex = r'\b\w+\s' + andword + '\b'
secondregex = r'\b' + andword + '\s\w+\b'


def sample_bigrams_no_and(word_list):
    coll_list = []
    for word in word_list:
        if not re.match(firstregex, word):
            if not re.match(secondregex, word):
                coll_list.append((word, countdict[word]))
    return coll_list[100:160]


def sample_bigrams_w_and(word_list):
    coll_list = []
    for word in word_list:
        coll_list.append((word, countdict[word]))
    return coll_list[100:160]


if w_and == 1:
    print(sample_bigrams_w_and(word_list))
elif w_and == 0:
    print(sample_bigrams_no_and(word_list))

'''
Sorts by frequency and returns result.
'''

input_range = 5000

sorted_coll_list = sorted(coll_list, key=lambda x: x[1], reverse=True)
# print(sorted_coll_list[0:int(input_range)])

for_output = sorted_coll_list[0:int(input_range)]

final_text = ""
for tupleitem in for_output:
    final_text += str(tupleitem[0])+","+str(tupleitem[1])+"\n"
# print(final_text[0:20])

text_file0 = open("output.txt", "w")
text_file0.write(final_text)
text_file0.close()

text_file1 = open("output.csv", "w")
text_file1.write(final_text)
text_file1.close()
