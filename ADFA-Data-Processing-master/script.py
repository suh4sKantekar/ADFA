import math
import operator
from collections import OrderedDict, Counter
import glob
import os
from nltk import ngrams
# from nltk import Counter
import time


# method to get a word from a file
def get_word(fp):
    x = fp.read(1)
    z = fp.read(1)
    while z != " " and z != "":
        x = x + z
        z = fp.read(1)
    return x


# feature selection starts here
root, dirs, files = os.walk("./Attack_Data_Master").__next__()
temp_l = list()
hello = list()

# cataloguing the types of attacks given
for x in dirs:
    hello.append(str(x)[::-1])

for x in hello:
    i = 0
    for y in x:
        if x[i] == '_':
            temp = x[i:]
            temp = temp[::-1]

            if temp in temp_l:
                a = 1
            else:
                temp_l.append(temp)
            break

        else:
            i = i + 1

# initialising lists to hold the features generated
set_3 = set()
set_5 = set()
set_7 = set()

temp_l_d = OrderedDict()

for xx in temp_l:
    jj = 1
    while xx + str(jj) in dirs:
        temp_l_d[xx + str(jj)] = 0
        jj += 1

# traversing the folders
for xx in temp_l:
    jj = 1

    open("training_" + xx + ".txt", 'w').close()
    open("testing_" + xx + ".txt", 'w').close()

    choice = ""
    while choice != "y" and choice != "n":
        choice = input("Include attack \"" + xx[:-1] + "\" for feature selection? (y/n) : ")

    if (choice == "n"):
        jjj = 1
        while xx + str(jjj) in dirs:
            temp_l_d[xx + str(jjj)] = -1
            jjj += 1
        continue

    choice = ""
    while choice != "y" and choice != "n":
        choice = input("Include top 70% folders of the attack \"" + xx[:-1] + "\"? (y/n) : ")

    # setting a flag according to user input to include all folders or not
    flag = 0
    if (choice == "y"):
        flag = 1

    jjj = 1
    while xx + str(jjj) in dirs:
        temp_l_d[xx + str(jjj)] = 1
        jjj += 1

    # concatenating all the files of an attack type

    # use 70% loop
    no_temp_count = 0
    temp_count = 0
    rr = 1
    while xx + str(rr) in dirs:
        temp_count += 1
        rr += 1

    temp_count = int(math.ceil(0.7 * temp_count))

    no_temp_count = rr - 1 - temp_count

    while xx + str(jj) in dirs:

        if temp_count == 0:
            read_files = glob.glob("./Attack_Data_Master/" + xx + str(jj) + "/*.txt")
            with open("testing_" + xx + ".txt", "ab") as outfile:
                for f in read_files:
                    with open(f, "rb") as infile:
                        outfile.write(infile.read())
                    outfile.write(str.encode("% "))
            temp_l_d[xx + str(jj)] = 0
            jj += 1
            continue

        if no_temp_count == 0:
            read_files = glob.glob("./Attack_Data_Master/" + xx + str(jj) + "/*.txt")

            with open("training_" + xx + ".txt", "ab") as outfile:

                for f in read_files:
                    with open(f, "rb") as infile:
                        outfile.write(infile.read())
                    outfile.write(str.encode("% "))
            temp_l_d[xx + str(jj)] = 1
            jj += 1
            continue

        if flag == 0:
            choice = ""
            while choice != "y" and choice != "n":
                choice = input("Include folder \"" + xx + str(jj) + "\" for feature selection?(y/n) : ")

        if choice == "n":
            read_files = glob.glob("./Attack_Data_Master/" + xx + str(jj) + "/*.txt")
            with open("testing_" + xx + ".txt", "ab") as outfile:
                for f in read_files:
                    with open(f, "rb") as infile:
                        outfile.write(infile.read())
                    outfile.write(str.encode("% "))

            no_temp_count -= 1
            temp_l_d[xx + str(jj)] = 0
            jj += 1
            continue

        read_files = glob.glob("./Attack_Data_Master/" + xx + str(jj) + "/*.txt")

        with open("training_" + xx + ".txt", "ab") as outfile:

            for f in read_files:
                with open(f, "rb") as infile:
                    outfile.write(infile.read())
                outfile.write(str.encode("% "))

        jj += 1
        temp_count -= 1
        temp_l_d[xx + str(jj)] = 1

    # concatenation ends here

    fl = open("training_" + xx + ".txt", "r")  # open the file

    dict_7 = OrderedDict()  # dictionary to store 7 grams
    dict_5 = OrderedDict()  # dictionary to store 5 grams
    dict_3 = OrderedDict()  # dictionary to store 3 grams

    file = fl.read().split()

    sevengrams = ngrams(file, 7)
    fivegrams = ngrams(file, 5)
    threegrams = ngrams(file, 3)

    dict_5 = dict(Counter(fivegrams))
    dict_3 = dict(Counter(threegrams))
    dict_7 = dict(Counter(sevengrams))

    for i in list(dict_7.keys()):
        if '%' in str(i):
            del dict_7[i]

    for i in list(dict_3.keys()):
        if '%' in str(i):
            del dict_3[i]

    for i in list(dict_5.keys()):
        if '%' in str(i):
            del dict_5[i]

    # sorting the n-grams according to their counts
    dict_5 = (sorted(dict_5.items(), key=operator.itemgetter(1)))  # sort according to value
    dict_7 = (sorted(dict_7.items(), key=operator.itemgetter(1)))  # sort according to value
    dict_3 = (sorted(dict_3.items(), key=operator.itemgetter(1)))  # sort according to value

    # reversing the dictionaries to get them in descending order
    dict_3 = OrderedDict(dict_3[::-1])
    dict_5 = OrderedDict(dict_5[::-1])
    dict_7 = OrderedDict(dict_7[::-1])

    top_30_3 = int(math.ceil((len(dict_3) + 0.0) * 0.3))  # get top 30 % tuples and convert it to a int
    top_30_5 = int(math.ceil((len(dict_5) + 0.0) * 0.3))  # get top 30 % tuples and convert it to a int
    top_30_7 = int(math.ceil((len(dict_7) + 0.0) * 0.3))  # get top 30 % tuples and convert it to a int

    # for loop in top 30 % of tuples and add them to the list if they aren't already present in it

    set_3 = set_3.union(set(list(dict_3.keys())[0:top_30_3]))
    set_5 = set_5.union(set(list(dict_5.keys())[0:top_30_5]))
    set_7 = set_7.union(set(list(dict_7.keys())[0:top_30_7]))

#######################################################

# block1.py goes here

open("training_Normal_.txt", 'w').close()
open("testing_Normal_.txt", 'w').close()

read_files = glob.glob("./Training_Data_Master/*.txt")

with open("training_Normal_.txt", "ab") as outfile:
    for f in read_files:
        with open(f, "rb") as infile:
            outfile.write(infile.read())
        outfile.write(str.encode("% "))

read_files = glob.glob("./Validation_Data_Master/*.txt")

with open("testing_Normal_.txt", 'ab') as outfile:
    for f in read_files:
        with open(f, "rb") as infile:
            outfile.write(infile.read())
        outfile.write(str.encode("% "))

########################################################

# writing the lists into the final output files
c_file = open("3_features.txt", "w")
for key in set_3:
    c_file.write(str(key) + "\n")
c_file.close()

c_file = open("5_features.txt", "w")
for key in set_5:
    c_file.write(str(key) + "\n")
c_file.close()

c_file = open("7_features.txt", "w")
for key in set_7:
    c_file.write(str(key) + "\n")
c_file.close()

# feature selection ends here

input("Feature Selection completed.\n\nPress enter to continue with he training table generation...")

# Training Table Generation begins here
print("\nGenerating the training table...")

# Ordered dictionaries to hold count of the features selected
dict_3 = OrderedDict.fromkeys(open('3_features.txt', 'r').read().splitlines(), 0)
dict_5 = OrderedDict.fromkeys(open('5_features.txt', 'r').read().splitlines(), 0)
dict_7 = OrderedDict.fromkeys(open('7_features.txt', 'r').read().splitlines(), 0)

# opening the files
res_3 = open('3-gram-train.txt', 'w')
res_5 = open('5-gram-train.txt', 'w')
res_7 = open('7-gram-train.txt', 'w')
val_3 = open('3-gram-test.txt', 'w')
val_5 = open('5-gram-test.txt', 'w')
val_7 = open('7-gram-test.txt', 'w')

start_time_train = time.time()
read_files = glob.glob("./training_*.txt")
for f in read_files:

    infile = open(f, "r").read()
    if infile == "":
        continue

    print("Processing : " + f[11:len(f) - 5])

    str_3 = ""
    str_5 = ""
    str_7 = ""

    for infiles in infile.split('% '):

        grams_7 = dict(Counter(ngrams(infiles.split(), 7)))

        dict_3_temp = dict_3.copy()
        dict_5_temp = dict_5.copy()
        dict_7_temp = dict_7.copy()

        for i in grams_7.keys():

            try:
                dict_7_temp[str(i)] += grams_7[i]
            except KeyError:
                pass

            try:
                dict_5_temp[str(i[0:5])] += grams_7[i]
            except KeyError:
                pass

            try:
                dict_3_temp[str(i[0:3])] += grams_7[i]
            except KeyError:
                pass

        str_3 += (str(list(dict_3_temp.values())) + " " + f[11:len(f) - 5] + "\n")
        str_5 += (str(list(dict_5_temp.values())) + " " + f[11:len(f) - 5] + "\n")
        str_7 += (str(list(dict_7_temp.values())) + " " + f[11:len(f) - 5] + "\n")

    res_3.write(str_3)
    res_5.write(str_5)
    res_7.write(str_7)

print("Time Taken to Generate Training Table : " + str(time.time() - start_time_train))

start_time_test = time.time()

read_files = glob.glob("./testing_*.txt")
for f in read_files:

    infile = open(f, "r").read()
    if infile == "":
        continue

    print("Processing : " + f[10:len(f) - 5])

    str_3 = ""
    str_5 = ""
    str_7 = ""

    for infiles in infile.split('% '):

        grams_7 = dict(Counter(ngrams(infiles.split(), 7)))

        dict_3_temp = dict_3.copy()
        dict_5_temp = dict_5.copy()
        dict_7_temp = dict_7.copy()

        for i in grams_7.keys():

            try:
                dict_7_temp[str(i)] += grams_7[i]
            except KeyError:
                pass

            try:
                dict_5_temp[str(i[0:5])] += grams_7[i]
            except KeyError:
                pass

            try:
                dict_3_temp[str(i[0:3])] += grams_7[i]
            except KeyError:
                pass

        str_3 += (str(list(dict_3_temp.values())) + " " + f[10:len(f) - 5] + "\n")
        str_5 += (str(list(dict_5_temp.values())) + " " + f[10:len(f) - 5] + "\n")
        str_7 += (str(list(dict_7_temp.values())) + " " + f[10:len(f) - 5] + "\n")

    val_3.write(str_3)
    val_5.write(str_5)
    val_7.write(str_7)

print("Time Taken to Generate Testing Table : " + str(time.time() - start_time_test))