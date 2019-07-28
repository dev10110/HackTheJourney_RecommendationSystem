import turicreate as tc
import pandas as pd
import numpy as np
import random
import os


class RecommenderClient:
    def __init__(self):
        # data is what is returned by Vishnu's client
        self.data = [];
        self.cities_added = set();

    def add_data(self,newdata, city = '', create_model=True):

        city = city.lower()

        if city in self.cities_added:
            return

        self.data += newdata

        #the ref data is the raw data table
        ref_data = self.ref_data = pd.DataFrame.from_dict(self.data)
        self.num_of_choices = len(ref_data);

        #if city is not an empty string, add the name of the city to the list of cities.
        if not city:
            self.cities_added.add('city')

        if create_model:
            self.create_model()
        return


    def create_model(self):

        #construct data frame that contains only the training categories
        model_data = self.model_data = self.ref_data[['category', 'tags','city']]
        model_data['index'] = model_data.index

        #update list of categories
        self.categories = self.model_data['category'].unique()

        #create turicreate SFrame
        tc_data = self.tc_data = tc.SFrame(model_data)

        #create model
        self.model = tc.recommender.item_content_recommender.create(tc_data, item_id = 'index', verbose=False)

        return


    def cold_start(self,k=10):
        #k is the number of items to suggest.
        #randomly suggests k items
        # returns list of indices.

        suggestion_id = random.sample(list(range(self.num_of_choices)), k=k)

        return suggestion_id


    def suggest(self, k = 10, likes = [], dislikes = [], categories = [], cities = [], diversity=2):
        #likes is the list of items that have been liked.
        #categories is either a string matching the category, or a list of strings matching the categories
        #returns pandas dataframe with index and the score


        #create list of allowed items based on categories
        if categories  == []:
            allowed_index_cat = list(range(self.num_of_choices));
        else:
            allowed_index_cat = [i for i in range(self.num_of_choices) if self.model_data['category'][i] in categories]
            #allowed_items = tc.SFrame(allowed_index)

        #create list of allowed items based on city
        if cities == []:
            allowed_index_city = list(range(self.num_of_choices))
        else:
            allowed_index_city = [i for i in range(self.num_of_choices) if self.model_data['city'][i] in cities]

        #take intersection
        allowed_index = list(set(allowed_index_cat) & set(allowed_index_city))

        recommendations = self.model.recommend_from_interactions(observed_items = likes,
                                                                 k=k,
                                                                 exclude=None, #dislikes,#tc.SFrame(self.model_data.iloc[dislikes]),
                                                                 items=allowed_index,
                                                                 new_user_data=None,
                                                                 new_item_data=None,
                                                                 exclude_known=True,
                                                                 diversity=diversity,
                                                                 random_seed=None,
                                                                 verbose=False)

        return recommendations

    def recs2data(self,recommendations, df = True):
        #recommendations is a pandas frame including the indicies
        #returns the dictionary of data that is desired
        #if df is true, it returns the data frame, or else it returns the dictionary

        indices = list(recommendations['index'])
        recdf = self.ref_data.iloc[indices]
        recdf['score'] = recommendations['score']

        if df:

            return recdf

        else:
            return recdf.to_dict()

    def ind2data(self,index, df = True):
        #converts list of indices to recommdation data
        if df:
            return self.ref_data.iloc[index]
        else:
            return [self.data[i] for i in index]
