# #streamlit run app.py
# Word polarity: Assigning sentiment scores to individual words based on their meaning.
# Context: Analyzing the context in which words are used to understand sarcasm or nuanced expressions.
# Negations: Identifying negations that can reverse the sentiment of a statement
import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

# from io import BytesIO
st.sidebar.title("Whatsapp Chat Analzer")

import streamlit as st
import pandas as pd
from io import StringIO

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    # st.dataframe(df)
    #fetch unique user
    user_list=df['user'].unique().tolist()
    if 'group_notification' in df['message'].values:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show analysis wrt",user_list)
    if st.sidebar.button("Show Anaysis"):
        #stats area
        num_messages,words,num_media_messages,num_links=helper.fetch_stats(selected_user,df)
        st.title("Top statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links shared")
            st.title(num_links)
        #monthly timeline
        st.title("Monthly timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        #daily timeline
        st.title("Daily timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='red')
        plt.xticks(rotation='vertical')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title('Activity Map')
        col1,col2=st.columns(2)
        with col1:
            st.header("Most busy day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='red')
            st.pyplot(fig)
        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values, color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly activity map")
        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax= sns.heatmap(user_heatmap)
        st.pyplot(fig)
        #fining the busiest users in the group
        if selected_user=='Overall':
            st.title('Most Busy users')
            x,new_df=helper.most_busy_user(df)
            fig,ax=plt.subplots()

            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
        #WordCloud
        st.title("Wordcloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1],color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        st.dataframe(most_common_df)
        #emoji analysis
        emoji_df=helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        col1,col2=st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels= emoji_df[0].head(),autopct="%0.2f")
            ax.set_aspect('equal')
            st.pyplot(fig)

        # st.dataframe(emoji_df)
#sentiment analysis
    df['sentiment'] = df['message'].apply(helper.analyze_sentiment)

    # Display the sentiment analysis results
    st.subheader("Sentiment Analysis Results")
    # st.dataframe(df[['user', 'message', 'sentiment']])
    # Create a bar chart for sentiment distribution
    sentiment_counts = df['sentiment'].value_counts()
    # st.bar_chart(sentiment_counts)

    # Optionally, display a pie chart for sentiment distribution
    fig, ax = plt.subplots()
    ax.pie(sentiment_counts, labels=sentiment_counts.index, autopct="%0.2f%%", startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)




