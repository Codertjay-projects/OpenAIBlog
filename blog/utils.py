import math
import operator
import re
from functools import reduce

import openai
from decouple import config
from django.db.models import Q
from django.utils.html import strip_tags
from django.utils.text import slugify
from google.oauth2 import service_account
from googleapiclient.discovery import build


def count_words(html_string):
    """
    :param html_string: <h1>this is an html string</h1>
    :return: this is an html string
    """
    word_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+', word_string)
    count = len(matching_words)
    return count


def get_read_time(html_string):
    count = count_words(html_string)
    read_time_min = math.ceil((count / 200.0))  # assuming 200 word perminute reading
    # read_time_sec = read_time_min * 60
    # read_time = str(datetime.timedelta(minutes=read_time_min))
    return int(read_time_min)


def create_slug(instance, new_slug=None):
    from blog.models import Post

    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        new_slug = f'{slug}-{qs.first().id}'
        return create_slug(instance, new_slug=new_slug)
    return slug


def get_contents():
    content_list = []

    # Path to the JSON key file for your service account
    KEY_PATH = 'credential.json'

    # Authenticate with the Google Docs API
    creds = service_account.Credentials.from_service_account_file(KEY_PATH, scopes=[
        'https://www.googleapis.com/auth/documents.readonly'])
    docs_service = build('docs', 'v1', credentials=creds)

    # Read a document
    # theirs
    document_id = '1jlNXtc9T3CTPPzbPhzw630dyEONtg2CIvYWJaYxIQrA'
    # mine
    result = docs_service.documents().get(documentId=document_id).execute()
    content = result.get('body').get('content')
    for item in content:
        try:
            content_list.append(item.get("paragraph").get("elements")[0].get("textRun").get("content"))
        except:
            print("error")
            pass
    return content_list


def create_description(name):
    openai.api_key = config("OPEN_AI_API_KEY")

    model_engine = "text-davinci-002"  # choose your preferred model engine
    prompt = f"Write an informative article about {name}"

    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=2000,  # maximum length of the generated text
        n=1,  # number of text responses to generate
        stop=None,
        temperature=0.5
    )

    text = response.choices[0].text
    return text


def query_items(query, item):
    """
    this query list is used to filter item more of like a custom query the return the query set
    :param query:
    :param item:
    :return:
    """
    query_list = []
    query_list += query.split()
    query_list = sorted(query_list, key=lambda x: x[-1])
    query = reduce(
        operator.or_,
        (Q(name=x) |
         Q(description=x) |
         Q(name__in=[x]) for x in query_list)
    )
    object_list = item.filter(query).distinct()
    return object_list
