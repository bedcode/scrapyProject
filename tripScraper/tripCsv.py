import numpy
import pandas as pd
import sys

if len(sys.argv) != 2:
    raise Exception('Insert file name')

FILE = sys.argv[1]

# We use the Pandas library to read the contents of the scraped data
# obtained by scrapy
df = pd.read_csv(FILE, encoding='utf-8')

# Now we remove duplicate rows (reviews)
#df.drop_duplicates(inplace=True)

scores = []

def get_star(stars):
    scoring = stars.split()
    #print(scoring)
    try:
        scoring = float(scoring[0])
    except ValueError:
        pass
    scores.append(scoring)

df['star'] = df['stars'].apply(get_star)
print("mean: " + str(numpy.mean(scores)))
print("min: " + str(numpy.min(scores)))
print("max: " + str(numpy.max(scores)))

# Drop the reviews with 3 stars, since we're doing Positive/Negative
# sentiment analysis.
#df = df[df['stars'] != '3 of 5 stars']

# We want to use both the title and content of the review to
# classify, so we merge them both into a new column.
df['full_content'] = df['title'] + '. ' + df['content']

def get_class(stars):
    score = int(stars[0])
    #print(score)
    if score >= 3:
        return 'Good'
    else:
        return 'Bad'

# Transform the number of stars into Good and Bad tags.
df['true_category'] = df['stars'].apply(get_class)

df = df[['full_content', 'true_category']]

# Write the data into a CSV file
df.to_csv('itemsHotel_MonkeyLearn2.csv', header=False, index=False, encoding='utf-8')

print(df['true_category'].value_counts())
