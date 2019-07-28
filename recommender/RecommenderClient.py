import turicreate as tc
import pandas as pd
import numpy as np
import random

class RecommenderClient:
    def __init__(self,data):
        # data is what is returned by Vishnu's client
        self.data = data;

        #the ref data is the raw data table
        ref_data = self.ref_data = pd.DataFrame.from_dict(data)
        self.num_of_choices = len(ref_data);

        #construct data frame that contains only the training categories
        model_data = self.model_data = ref_data[['category', 'tags']]
        model_data['index'] = model_data.index

        self.categories = self.model_data['category'].unique()

        #create turicreate SFrame
        tc_data = self.tc_data = tc.SFrame(model_data)

        #create model
        model = self.model = tc.recommender.item_content_recommender.create(tc_data, item_id = 'index', verbose=False)


    def cold_start(self,k=10):
        #k is the number of items to suggest.
        #randomly suggests k items
        # returns list of indices.

        suggestion_id = [random.randrange(self.num_of_choices) for _ in range(k)]

        return suggestion_id


    def suggest(self, k = 10, likes = [], dislikes = [], categories = []):
        #likes is the list of items that have been liked.
        #categories is either a string matching the category, or a list of strings matching the categories
        #returns pandas dataframe with index and the score


        #create list of allowed items
        if categories  == []:
            allowed_index = list(range(self.num_of_choices));
        else:
            allowed_index = [i for i in range(self.num_of_choices) if self.model_data['category'][i] in categories]
            #allowed_items = tc.SFrame(allowed_index)

        recommendations = self.model.recommend_from_interactions(observed_items = likes,
                                                                 k=k,
                                                                 exclude=None, #dislikes,#tc.SFrame(self.model_data.iloc[dislikes]),
                                                                 items=allowed_index,
                                                                 new_user_data=None,
                                                                 new_item_data=None,
                                                                 exclude_known=True,
                                                                 diversity=0,
                                                                 random_seed=None,
                                                                 verbose=False)

        return recommendations
