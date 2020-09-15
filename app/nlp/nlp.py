import nltk
import codecs
import os
import random
from nltk import word_tokenize
from nltk import NaiveBayesClassifier, classify
nltk.download('punkt')

# This is only experimental and currently not in use
# the classic nlp approach isnt suited to this project
# This project is concerned about words, whereas nlp is more about classifying sentences
# What I tried -just for fun - was to split each word into letters and try to classify that way
# As expected, nothing really fruitful. 
# Leaving this in, just in case I ever come back to it though

def read_in(filename):
    dirname = os.path.dirname(__file__)
    fullpath = os.path.join(dirname, filename)
    with open(fullpath) as f:
        lines = f.read().splitlines()
    return lines

def tokenize(input):
    word_list = []
    for word in word_tokenize(input):
        word_list.append(word)
    return word_list

def get_features(word):
    features = {}
    t_word = word_tokenize(word.lower())
    for letter in list(t_word[0]):
        features[letter] = True
    return features


# Read in the files
relevant_words = read_in("relevant.txt")
non_relevant_words = read_in("nonrelevant.txt")
# print(len(relevant))
# print(len(non_relevant))
# print(relevant[0])
# print(non_relevant[0])

# Join them in a data set 
all_words = [(word, "non") for word in non_relevant_words]
all_words += [(word, "relevant") for word in relevant_words]
random.seed(42)
random.shuffle(all_words)
print (f"Dataset size = {str(len(all_words))} words")

# Get features
all_features = [(get_features(word), label)
    for (word, label) in all_words]

#print(len(all_features))
print(all_features[0][0])
 
def train(features, proportion):
    train_size = int(len(features) * proportion)
    train_set, test_set = features[:train_size], features[train_size:]
    print (f"Training set size = {str(len(train_set))} words")
    print (f"Test set size = {str(len(test_set))} words")
    classifier = NaiveBayesClassifier.train(train_set)
    return train_set, test_set, classifier
 
train_set, test_set, classifier = train(all_features, 0.8)

def evaluate(train_set, test_set, classifier):
    print (f"Accuracy on the training set = {str(classify.accuracy(classifier, train_set))}")
    print (f"Accuracy of the test set = {str(classify.accuracy(classifier, test_set))}")
    classifier.show_most_informative_features(50)
 
evaluate(train_set, test_set, classifier)

t = get_features('ccc')
res = classifier.classify(t)
print(res)