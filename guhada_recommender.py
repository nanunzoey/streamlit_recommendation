"""
    Streamlit webserver-based Recommender Engine.
    Author: SaveFingers
"""
import sys
import pickle
import random

# Streamlit dependencies
import streamlit as st
# import SessionState

# Data handling dependencies
import pandas as pd
import numpy as np

# Custom Libraries
sys.path.append('/home/saveourfingers/guhada/streamlit_recommendation/utils')
from utils.data_loader import load_category_titles, load_user_ages
from recommenders.rec_product import rec_product


# SETTING CONFIG FOR STREAMLIT
st.set_page_config(layout='wide')


# Data Loading
base_path = '/home/saveourfingers/guhada'

# with open(base_path + '/streamlit_recommendation/new_valid_prod_info.pkl', 'rb') as f:
with open(base_path + '/streamlit_recommendation/total_product_info_final.pkl', 'rb') as f:
    # key: product_id, values: [seller_id(0), name(1), l_category_id(2), m_category_id(3), image_url(4)]
    total_products = pickle.load(f)

with open(base_path + '/streamlit_recommendation/m_category_to_product_id.pkl', 'rb') as f:
    # key: m_category+id, values: [product_id]
    m_category_to_pid = pickle.load(f)

category_list = load_category_titles(base_path + '/1110_copy/카테고리_브랜드/구하다 카테고리.csv')
age_list = load_user_ages(base_path + '/1110_copy/셀러/uid.csv')



# form with submit button to choose preferred product
def surprise_me():
    with st.form(key='submit_form'):
        st.session_state.chosen_prod = st.radio('Choose one of the above', st.session_state.prod_names)        
        submitted = st.form_submit_button('Surprise Me!')
    
    if submitted:
        for id in st.session_state.random_prod_ids:
            if total_products[id][1] == st.session_state.chosen_prod:
                st.session_state.chosen_prod_id = id

                with st.spinner('Searching for the best...'):
                    # display a warning if the user entered an existing name
                    try:
                        results = rec_product(st.session_state.chosen_prod_id)
                    except KeyError:
                        st.error("Oops! Looks like something went wrong.\
                            We'll need to fix it!")

                    st.balloons()
                    st.title("We think you'll like:")

                    # 각 컬럼에 이미지와 정보 출력
                    col1, col2, col3, col4, col5 = st.columns(5)
                    for i, rec_id in enumerate(results):
                        if i == 0:
                            with col1:
                                st.image(total_products[rec_id][4])
                                st.write(total_products[rec_id][1])
                        elif i == 1:
                            with col2:
                                st.image(total_products[rec_id][4])
                                st.write(total_products[rec_id][1])
                        elif i == 2:
                            with col3:
                                st.image(total_products[rec_id][4])
                                st.write(total_products[rec_id][1])
                        elif i == 3:
                            with col4:
                                st.image(total_products[rec_id][4])
                                st.write(total_products[rec_id][1])
                        elif i == 4:
                            with col5:
                                st.image(total_products[rec_id][4])
                                st.write(total_products[rec_id][1])
            

# Show images based on category_id
# 위에서 저장한 m_category_id를 바탕으로 랜덤으로 product 노출
# radio or like button으로 선호하는 product_id를 받아 return
def show_random_images(m_category_id):
    # random product id 4개 생성
    st.session_state.random_prod_ids = random.sample(m_category_to_pid[m_category_id], 4)

    img_urls = []
    st.session_state.prod_names = ['None']  # default value

    # KeyError 발생 시 함수 재호출 -> random_prod_ids 다시 받기
    try:
        for i, id in enumerate(st.session_state.random_prod_ids):
            img_urls.append(total_products[id][4])
            st.session_state.prod_names.append(total_products[id][1])
    except KeyError:
        return show_random_images(m_category_id)

    # User-based preferences
    st.write('### 💋 Choose What You Prefer')

    # 상품 정보 노출
    # 컬럼 나눠서 이미지 배치
    col1, col2, col3, col4 = st.columns(4)
    for i, id in enumerate(st.session_state.random_prod_ids):
        if i == 0:
            with col1:
                try:
                    st.image(img_urls[i], width=250)
                except FileNotFoundError:  # show default image
                    st.image('resources/imgs/default_image.png', use_column_width=True)
                st.write(st.session_state.prod_names[i+1])
        elif i == 1:
            with col2:
                try:
                    st.image(img_urls[i], width=250)
                except FileNotFoundError:  # show default image
                    st.image('resources/imgs/default_image.png', use_column_width=True)
                st.write(st.session_state.prod_names[i+1])
        elif i == 2:
            with col3:
                try:
                    st.image(img_urls[i], width=250)
                except FileNotFoundError:  # show default image
                    st.image('resources/imgs/default_image.png', use_column_width=True)
                st.write(st.session_state.prod_names[i+1])
        elif i == 3:
            with col4:
                try:
                    st.image(img_urls[i], width=250)
                except FileNotFoundError:  # show default image
                    st.image('resources/imgs/default_image.png', use_column_width=True)
                st.write(st.session_state.prod_names[i+1])

    return st.session_state.prod_names, st.session_state.random_prod_ids
      


# App declaration
def main():
    page_options = ["Recommender System", "Solution Overview"]
    page_selection = st.sidebar.selectbox("Menu", page_options)

    if page_selection == "Recommender System":
        # Header contents
        st.title('SaveFingers 추천 엔진')

        # LAYING OUT THE TOP SECTION OF THE APP
        row1_1, row1_2 = st.columns((2, 3))
        with row1_1:
            st.write('#### Save your fingers to search for the best!')

            # Recommender System algorithm selection
            st.write('### 👠 Recommendation Options')
            sys = st.radio("이용자 정보를 입력하면 맞춤 추천을 제안해 드려요!",
                        ('With your information', 'Only with your preferences'))
        with row1_2:
            st.image('resources/imgs/main_page.jpg', use_column_width=True)


        row2_1, row2_2 = st.columns(2)
        with row2_1:
            # User needs
            st.write('### 👜 Enter Your Needs')
            category_first = st.selectbox('1st Category', ['Select', 'Female', 'Male', 'Kids'])


            # Set user needs(category_id)
            if category_first == 'Select':
                pass
            elif category_first == 'Female':
                l_category_id = 1
                m_category_dict = {'의류': 4, '슈즈': 5, '가방': 6, '액세사리': 7, '지갑': 1315}

                # 선택한 1st category별 2nd category list 생성
                m_category_list = ['Select'] + list(m_category_dict.keys())
                st.selectbox('2nd Category', m_category_list, key='category_second')

            elif category_first == 'Male':
                l_category_id = 2
                m_category_dict = {'의류': 8, '슈즈': 9, '가방': 10, '액세사리': 11, '지갑': 1339}

                # 선택한 1st category별 2nd category list 생성
                m_category_list = ['Select'] + list(m_category_dict.keys())
                st.selectbox('2nd Category', m_category_list, key='category_second')

            elif category_first == 'Kids':
                l_category_id = 3
                m_category_dict = {'여아 베이비 (0-24m)': 12, '남아 베이비 (0-24m)': 13, '여아 키즈 (3-8)': 14, '남아 키즈 (3-8)': 15, '여아 주니어 (9-16)': 16, '남아 주니어 (9-16)': 17}

                # 선택한 1st category별 2nd category list 생성
                m_category_list = ['Select'] + list(m_category_dict.keys())
                st.selectbox('2nd Category', m_category_list, key='category_second')


        # 2nd category를 선택한 경우 & random 상품은 아직 선택하지 않은 경우, 랜덤 상품 이미지를 노출시킴
        if ('category_second' in st.session_state) & ('prod_names' not in st.session_state): 
            if st.session_state.category_second != 'Select':
                st.session_state.prod_names, st.session_state.random_prod_ids = show_random_images(m_category_dict[st.session_state.category_second])


        with row2_2:
            # Perform top-10 movie recommendation generation
            if sys == 'With your information':            
                # Basic user information (optional)
                st.write('### 💎 Enter Your Information')

                if 'gender_select' not in st.session_state:
                    st.selectbox('Gender', ['Select', 'Female', 'Male'], key='gender_select')
                    st.selectbox('Age', age_list, key='age_select')


            if sys == 'Only with your preferences':
                pass


        if ('category_second' in st.session_state) & ('prod_names' in st.session_state): 
            surprise_me()

    # -------------------------------------------------------------------

    # ------------- SAFE FOR ALTERING/EXTENSION -------------------
    if page_selection == "Solution Overview":
        st.title("Project Overview")
        st.write("Describe your winning approach on this page")

    # You may want to add more sections here for aspects such as an EDA,
    # or to provide your business pitch.


if __name__ == '__main__':
    main()

    # Delete all the items in Session state before rerun
    except_keys = ['random_prod_ids', 'chosen_prod_id', 'prod_names']

    for key in st.session_state.keys():
        if key not in except_keys:
            del st.session_state[key]
