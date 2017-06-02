import numpy
import pandas as pd
import sys

if len(sys.argv) != 2:
    raise Exception('Insert file name')

FILE = sys.argv[1]

# We use the Pandas library to read the contents of the scraped data
# obtained by scrapy
df = pd.read_csv(FILE, encoding='utf-8')

scores = []

def get_star(stars):
    #scoring = stars.split()
    #print(scoring)
    try:
        scoring = float(stars)
    except ValueError:
        pass
    scores.append(scoring)


df['star'] = df['score'].apply(get_star)
print("mean: " + str(numpy.mean(scores)))
print("min: " + str(min(scores)))
print("max: " + str(max(scores)))

good = 0
bad = 0
for i in scores:
    if i >= 6:
        good += 1
    else:
        bad += 1

print("Good comments: " + str(good))
print("Bad comments: " + str(bad))
#print(len(scores))
