# -*- coding: utf-8 -*-
"""
Erickson, Holly
Cuisine Study
"""

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('ggplot')

np.random.seed(123)

#%%
"""
Prep csv data
"""
# file_path = 'C://Master/Semester_6/Github/Cuisine/Code/RAW_recipes.csv'
# file_path = 'C://Master/Semester_6/Github/Cuisine/Code/srep00196-s2.csv' #skiprows=4
file_path = 'C://Master/Semester_6/Github/Cuisine/Code/srep00196-s3.csv'

df = pd.read_csv(file_path, skiprows = 4, names=["Cuisine", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32])


#%%
print(df.Cuisine.value_counts())

# Find n_ingredients for each recipe
n_ingredients = []
ing = list(df.columns)
ing.reverse()

for row in range(len(df)):
    for col in ing:
        if pd.isnull(df[col][row]):
            pass
        else:
            n_ingredients.append(col)
            break

#%%
df['n_ingredients'] = n_ingredients

#%%
ing_full = []
for row in range(len(df)):
    ing_list = []
    for col in range(1, 33):
        if pd.isnull(df[col][row]):
            pass
        else:
            n_ingredients.append(col)
            ing_list.append(df[col][row])
    ing_full.append(ing_list)
#%%
df['ingredients_list'] = ing_full
#%%
output = df.drop(range(1, 33), axis = 1)
output.to_csv('trans_srep00196-s3.csv', index = False)

#%%
"""
Prep kaggle data
"""
file_path1 = 'C://Master/Semester_6/Github/Cuisine/Code/test_kaggle.json'
file_path2 = 'C://Master/Semester_6/Github/Cuisine/Code/train_kaggle.json'


def read_dataset(path):
	return json.load(open(path)) 

train = read_dataset(file_path2)
test = read_dataset(file_path1)

#cuisine = [doc['cuisine'] for doc in test]
ing_full = [doc['ingredients'] for doc in test]
n_ingredients = [len(recipe) for recipe in ing_full]

#%%
output = pd.DataFrame()
output['ingredients_list'] = ing_full
output['n_ingredients'] = n_ingredients
#output['Cuisine'] = cuisine

output.to_csv('trans_kaggle_test.csv', index = False)

#%%
"""
Join DF's with Cuisine
"""
df1 = pd.read_csv('trans_kaggle_train.csv')
df2 = pd.read_csv('trans_srep00196-s3.csv')
print(df1.Cuisine.value_counts())
print(df2.Cuisine.value_counts())
#%%
plt.hist(df2['n_ingredients'],bins=max(df2['n_ingredients']),edgecolor='b')
plt.gcf().set_size_inches(16,8)
plt.title('Ingredients in a Dish Distribution')

#%%
all_ings = []
for row in range(len(df2)):
    ing_str = df2['ingredients_list'][row]
    rep = ing_str.replace('"', '')
    rep2 = rep.replace('[', '')
    rep3 = rep2.replace(']', '')
    rep4 = rep3.replace("'", "")
    ing_list = rep4.split(', ')
    #print(ing_list)
    for ing in ing_list:
        #print(ing)
        all_ings.append(ing)
#%%
ing_df = pd.DataFrame()
ing_df['ingredients'] = all_ings
ing_df.drop_duplicates(inplace = True)
#%%
ing_df.to_csv('ingredients_srep00196-s3.csv', index = False)
#%%
# Train
features_processed= [] # here we will store the preprocessed training features
for item in features:
    newitem = []
    for ingr in item:
        ingr.lower() # Case Normalization - convert all to lower case 
        ingr = re.sub("[^a-zA-Z]"," ",ingr) # Remove punctuation, digits or special characters 
        ingr = re.sub((r'\b(oz|ounc|ounce|pound|lb|inch|inches|kg|to)\b'), ' ', ingr) # Remove different units  
        newitem.append(ingr) 
    features_processed.append(newitem)

# Test 
features_test_processed= [] 
for item in features_test:
    newitem = []
    for ingr in item:
        ingr.lower() 
        ingr = re.sub("[^a-zA-Z]"," ",ingr)
        ingr = re.sub((r'\b(oz|ounc|ounce|pound|lb|inch|inches|kg|to)\b'), ' ', ingr) 
        newitem.append(ingr)
    features_test_processed.append(newitem) 
    
#%%
from sklearn.feature_extraction.text import CountVectorizer
vec = CountVectorizer(tokenizer=lambda x: [i.strip() for i in x.split(',')], lowercase=False)
counts = vec.fit_transform(df2['ingredients_list']) 
count=dict(zip(vec.get_feature_names(), counts.sum(axis=0).tolist()[0]))
count=pd.DataFrame(list(count.items()),columns=['Ingredient','Count'])
count.set_index('Ingredient').sort_values('Count',ascending=False)[:15].plot.barh(width=0.9)
plt.gcf().set_size_inches(10,10)
plt.gca().invert_yaxis()
plt.title('Top 15 Ingredients')