# coding: utf-8
import datetime
import time
from nytimesarticle import articleAPI
from tgrocery import Grocery


_api = '4288c097737d48b8a563975addd7fa52'

# generating date series
def time_gen_series(start_year=2015, start_month=12, start_day=31, step=30):
    """
    @param:integer
    @return: list of date series with format %Y%m%d
    """
    dt = datetime.datetime(start_year, start_month, start_day)
    end = datetime.datetime.now()
    step = datetime.timedelta(days=step)
    date_series = []
    while dt < end:
        date_series.append(dt.strftime('%Y%m%d %H:%M:%S').split(' ')[0])
        dt += step
    return date_series


# download articles from NYTIMEs website with official API, the website is provided below
# http://developer.nytimes.com/signup
# set up the keywords to downloads the articles with related keywords


def article_inform(keywords, date_series, file_name='data.txt',api_key=_api):
    """
    @:param: keywords: list of keywords
    @:param: date_series: list of date
    @:param: file_name: string
    @:return: content: list of records of NEWYORKTIMES
    """
    content = []
    api = articleAPI(api_key)
    # Downloads the information you need
    for keyword in keywords:
        for i in range(0, len(date_series) - 1):

            try:
                articles = api.search(q=keyword, start_date=date_series[i], end_date=date_series[i + 1])
                time.sleep(1)
                # my personal API, please get your own API through the website I provided.
                # For Usage: http://developer.nytimes.com/article_search_v2.json#/Documentation/GET/articlesearch.json
                # Articles are json files, which is a dict-like file
                for text in articles['response']['docs']:
                    content.append(text)
            except Exception:
                continue
    # save file
    with open(file_name, 'w') as f:
        for item in content:
            f.write("{}\n".format(item))
    return content


# Using the subsection_name as the keywords of classification. 
# Save the useful information as you want, here we need headlines, subsection_name and web_url
def classification(content):
    inform_list = [];
    for text in content:
        inform = {'headline': None, 'field': None, 'source': None}
        if text['subsection_name'] != None:
            # if we don't have the subsection_name, we throw out the articles
            inform['headline'], inform['field'], inform['source'] = text['headline']['main'], text['subsection_name'], \
                                                                    text['web_url']
            inform_list.append(inform)
        else:
            continue
    return inform_list


def train_test_sampling(inform_list,train_per=0.9):
    all_src = [];
    for text in inform_list:
        record = (text['field'], text['headline'])
        all_src.append(record)
    train_num = int(len(inform_list) * train_per)
    train_src = all_src[0:train_num]
    test_src = all_src[train_num + 1:-1]
    return train_src,test_src


def train_compare_result(train_src,test_src):
    grocery = Grocery('test')
    grocery.train(train_src)
    print grocery.get_load_status()
    len_test = len(test_src)
    print len_test
    Predict_num = 0
    History = []
    for test in test_src:
        Predict_result = {'predict_title': test[1], 'predict_class': None, 'true_class': None}
        predict_title = Predict_result['predict_title']
        predict_result = grocery.predict(predict_title)
        Predict_result['predict_class'], Predict_result['true_class'] = test[0], predict_result
        if str(predict_result) == str(test[0]):
            # print 'prediction is True'
            Predict_num += 1
        History.append(Predict_result)
        # print 'prediction is False'
    predict_precision = float(Predict_num) / len_test
    return predict_precision,History


if __name__ == '__main__':
    date_series = time_gen_series()
    Keywords = ['Dollars', 'Sex', 'Trump', 'China', 'Crash']
    content = article_inform(Keywords, date_series, file_name='data.txt')
    inform_list = classification(content)
    train_src,test_src = train_test_sampling(inform_list,0.9)
    predict_precision, History = train_compare_result(train_src,test_src)
    print predict_precision
