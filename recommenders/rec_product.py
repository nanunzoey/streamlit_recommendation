import pandas as pd
import numpy as np
import os
import glob
import random
from tqdm import tqdm
from PIL import Image
from IPython.display import display
from io import BytesIO

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances#유클리드 거리


# Data Loading
base_path = '/home/saveourfingers/guhada'
product_df = pd.read_csv(base_path + '/streamlit_recommendation/resources/data/products_sample.csv')


def rec_product(chosen_prod_id, prod_df=product_df, sim_func="cos"):
    '''Returns product_id of recommended products  
    
    Args
    - chosen_prod_id : input product id
    - prod_df : product_df
    - sim_func : euclidean/cosine_similarity
    '''
    # 전체 의류 제외하고 사용
    prod_df = prod_df.loc[prod_df['m_category_id'] == 5]
    prod_id_list = prod_df['product_id'].values

    dropped_prod_df = prod_df.drop(['deal_id', 'product_id', 'name', 'display_start_at', \
        'seller_id', 'product_status', 'is_parallel_import', 'created_at', 'updated_at'], axis=1)
    
    #euc based rec
    if sim_func == "euc":
        sim_df = pd.DataFrame(euclidean_distances(dropped_prod_df), columns=prod_id_list).set_index(prod_id_list)
        prod_id_rec = sim_df[chosen_prod_id].sort_values()[1:6].index
        # print(sim_df[chosen_prod_id].sort_values()[1:6])
        
    #cos based rec
    elif sim_func == "cos":
        sim_df = pd.DataFrame(cosine_similarity(dropped_prod_df), columns=prod_id_list).set_index(prod_id_list)
        prod_id_rec = sim_df[chosen_prod_id].sort_values(ascending=False)[1:6].index
        # print(sim_df[chosen_prod_id].sort_values(ascending=False)[1:6])
        
    # for i in prod_id_rec:
        # print(i,":",prod_df.loc[prod_df.product_id == i].cluster.values)
    
    return prod_id_rec

    #display imgs    
    # display_img(prod_id_rec)


# def display_img(chosen_prod_id, images_pil = images_pil,images_np = images_np):
#     '''display imgs  
    
#     Args
#     - prod_id : input product id
#     - images_pil : images_pil list
#     '''
#     for id in prod_id:
#         display(images_pil[id])
#         print(id_name_dict[id])
    

def dummy_scaler(prod_df, col, k, c):
    """Returns scaled dummies
    
    Args
    - prod_df : input DataFrame
    - col : col to dummies
    - k : num of dummies
    
    Return
    - df : scaled dummies df
    """
    dummy_list = []
    for i in range(k):
        dummy_list.append(col+"_"+str(i))
    
    prod_df = pd.get_dummies(prod_df, columns = [col])
    prod_df.loc[:, dummy_list] = prod_df.loc[:, dummy_list] * c
    
    return prod_df