import re
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import TemplateView
import rake
import environ

# from .tfidf import get_nltk_keywords


class VisualizationView(TemplateView):
    """Visualization view of a user."""

    template_name = 'visualization.html'

    def get_context_data(self, **kwargs):
        root_dir = environ.Path(__file__) - 2
        file_path = str(root_dir.path('data.csv'))
        username = self.kwargs.get('username')
        data = pd.read_csv(file_path)
        grouped = data.groupby('username', as_index=False)['message_text'].count()
        data_count = grouped[grouped.username == username].message_text
        return {
            'user': username,
            'tweet_count': int(data_count)
        }


class UniqueUsersAPI(APIView):
    """ Api to get data unique users from csv."""

    def get(self, request, *args, **kwargs):
        root_dir = environ.Path(__file__) - 2
        file_path = str(root_dir.path('data.csv'))
        data = pd.read_csv(file_path)
        grouped = data.groupby('username')['message_text'].count()
        users = grouped.index.get_level_values('username')
        return Response(list(users))


class WordAPI(APIView):
    """ Api to get data from csv."""

    def get(self, request, username, *args, **kwargs):
        messages = get_user_msg(username=username)
        # data for word tree
        msgs = [[i] for i in messages[:2]]
        tree_data = [['Phrases']]
        tree_data.extend(msgs)

        # data for word cloud
        root_dir = environ.Path(__file__) - 2
        stopwords_file = str(root_dir.path('SmartStoplist.txt'))
        cloud_data = get_rake_keywords(stopwords_file, messages)
        # data = get_nltk_keywords(messages)
        data = {'word_tree': tree_data, 'word_cloud': cloud_data}
        return Response(data)


def get_user_msg(username, remove_stopword=False):
    root_dir = environ.Path(__file__) - 2
    file_path = str(root_dir.path('data.csv'))
    data = pd.read_csv(file_path)
    user_data = data[data.username == username]
    user_data = user_data.message_text
    user_data = user_data.apply(clean_text)
    if remove_stopword:
        # remove stop words
        root_dir = environ.Path(__file__) - 2
        stopwords_file = str(root_dir.path('SmartStoplist.txt'))
        f = open(stopwords_file)
        stop_words = [x.strip() for x in f.readlines()]
        # user_data.apply(remove_stopwords, args=(stop_words,))
        user_data = user_data.apply(
            lambda x: ' '.join([item for item in x if item.lower() not in stop_words]))
        print(user_data)
    return list(user_data)


def remove_stopwords(text, stop_words):
    word_list = text.split()
    for word in word_list:
        if word.lower() in stop_words:
            text = text.replace(word, '')
    return text


def clean_text(text):
    special_chars = ['.', '?', ',', ':', '*', '/', '\\']
    text = re.sub(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        '', text).strip()
    text = re.sub(
        '(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z0-9]+[A-Za-z0-9_]+)',
        '', text).strip()
    for char in special_chars:
        text = text.replace(char, '').strip()
    try:
        text = text.decode('utf-8')
    except:
        print('exception in decoding')
    return text


def get_rake_keywords(stopwords_file, messages, limit=100):
    cleaned_text = '. '.join(messages)
    rake_object = rake.Rake(stopwords_file, 3, 2, 1)
    keywords = rake_object.run(cleaned_text)
    data = [{'text': i[0], 'weight': i[1]} for i in keywords]
    return data
