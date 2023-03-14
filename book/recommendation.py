import pandas as pd
import pickle
import os


cwd= os.getcwd()
rating_df= pd.read_pickle(f"{cwd}\\book\\ratings.pkl")

def get_estimated_rating_for(USER_ID, BOOK_ID):
    users_who_have_rated_book = rating_df[rating_df[BOOK_ID] != 0].index
    users_who_have_rated_book_ratings = rating_df.iloc[users_who_have_rated_book].copy(deep=True)
    user_rating = rating_df.iloc[USER_ID]
    users_who_have_rated_book_ratings.loc[USER_ID] = user_rating
    users_who_have_rated_book_ratings = users_who_have_rated_book_ratings.transpose()
    original_axes = users_who_have_rated_book_ratings.axes[1].to_list()


    def normalize_matrix(row, user_rating):
        return (row * user_rating / user_rating).fillna(0)
    r = users_who_have_rated_book_ratings.apply(lambda x: normalize_matrix(x, user_rating)).transpose()

    from sklearn.metrics.pairwise import cosine_similarity
    similarity_scores = cosine_similarity(r)
    similarity_scores = pd.DataFrame(similarity_scores)

    users_who_have_rated_book_ratings = rating_df.iloc[users_who_have_rated_book]

    similarity_scores = similarity_scores.set_axis(original_axes, axis="index")
    similarity_scores = similarity_scores.set_axis(original_axes, axis="columns")


    average_data = []
    for u in original_axes:
        if u != USER_ID:
            weight = similarity_scores[USER_ID][u]
            rating = users_who_have_rated_book_ratings[BOOK_ID][u]
            average_data.append((rating, weight))

    ratings, weights = zip(*average_data)
    estimated_rating = sum(map(lambda x: x[0] * x[1], average_data)) / sum(weights)
    return estimated_rating




def get_ratings(USER_ID):
    ratings = []
    for i in range(400):
        ratings.append((get_estimated_rating_for(USER_ID, i), i))
    return sorted(ratings,reverse=True)

