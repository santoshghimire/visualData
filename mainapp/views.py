import re
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic import TemplateView
import rake


class VisualizationView(TemplateView):
    """Visualization view of a user."""

    template_name = 'visualization.html'

    def get_context_data(self, **kwargs):
        username = self.kwargs.get('username')
        data = pd.read_csv('data.csv')
        grouped = data.groupby('username', as_index=False)['message_text'].count()
        data_count = grouped[grouped.username == username].message_text
        return {
            'user': username,
            'tweet_count': int(data_count)
        }


class UniqueUsersAPI(APIView):
    """ Api to get data unique users from csv."""

    def get(self, request, *args, **kwargs):
        data = pd.read_csv('data.csv')
        grouped = data.groupby('username')['message_text'].count()
        users = grouped.index.get_level_values('username')
        return Response(list(users))


class WordCloudAPI(APIView):
    """ Api to get data from csv."""

    def get(self, request, username, *args, **kwargs):
        messages = get_user_msg(username)
        cleaned_text = '. '.join(messages)

        rake_object = rake.Rake("SmartStoplist.txt", 3, 3, 1)
        keywords = rake_object.run(cleaned_text)
        data = [{'text': i[0], 'weight': i[1]} for i in keywords[:100]]
        # data = [
        #     {'text': "Lorem", 'weight': 13},
        #     {'text': "Ipsum", 'weight': 10.5},
        #     {'text': "Dolor", 'weight': 9.4},
        #     {'text': "Sit Down", 'weight': 8},
        #     {'text': "Amet", 'weight': 6.2},
        #     {'text': "Consectetur", 'weight': 5},
        #     {'text': "Adipiscing", 'weight': 5},
        # ]
        return Response(data)


class WordTreeAPI(APIView):
    """ Api to get data from csv."""

    def get(self, request, username, *args, **kwargs):
        messages = get_user_msg(username)
        print(messages)
        msgs = [[i] for i in messages[:2]]
        data = [['Phrases']]
        data.extend(msgs)
        # data = [
        #     ['Phrases'],
        #     ['cats are better than dogs'],
        #     ['cats eat kibble'],
        #     ['cats are better than hamsters'],
        #     ['cats are awesome'],
        #     ['cats are people too'],
        #     ['cats eat mice'],
        #     ['cats meowing'],
        #     ['cats in the cradle'],
        #     ['cats eat mice'],
        #     ['cats in the cradle lyrics'],
        #     ['cats eat kibble'],
        #     ['cats for adoption'],
        #     ['cats are family'],
        #     ['cats eat mice'],
        #     ['cats are better than kittens'],
        #     ['cats are evil'],
        #     ['cats are weird'],
        #     ['cats eat mice'],
        # ]
        return Response(data)


def get_user_msg(username):
    data = pd.read_csv('data.csv')
    user_data = data[data.username == username].message_text
    user_data['msg_cleaned'] = user_data.apply(clean_text)
    return list(user_data.msg_cleaned)


def clean_text(text):
    special_chars = ['.', '?', ',', ':', '*', '/', '\\']
    text = re.sub(
        'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        '', text).strip()
    text = re.sub(
        '(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9_]+)',
        '', text).strip()
    for char in special_chars:
        text = text.replace(char, '').strip()
    return text
