import re
import requests
import csv
import configparser
from bs4 import BeautifulSoup
import sys

"""
    This script scrapes mashable.com atricles for the following,
    author, timestamp of post, title and atricle content. The html
    layout differs in some of the atricles so cleaning of the data
    is needed. The cleaning consists of removed endlines, seperate
    date and name(from the author-info paragraph), and also removing
    image script that occur sometimes in the atricle content.


"""

def scrapeTitle(string):
    #returns empty strings if not found

    soup = BeautifulSoup(string, 'html.parser')
    title_ele = soup.find('h1', attrs={'class':'title'})

    if title_ele:
        return title_ele.text
    else:
        # no title was found
        return ''

def scrapeAuthorDate(string):
    #returns empty if nothing is found

    soup = BeautifulSoup(string, 'html.parser')
    author_info_ele = soup.find('div', attrs={'class':'article-info'})
    if not author_info_ele:
        return '',''

    # handle date
    date_ele = author_info_ele.find('time')
    if not date_ele:
        return '', ''
    date = date_ele.text

    # handle author name
    author_ele = author_info_ele.find('span', attrs={'class':'author_name'})
    if not author_ele:

        # remove newlines first, since .* can't match newlines
        author_info = re.sub(r'\n', ' ', author_info_ele.text)
        # remove everything ' for' and rest, and space
        author = re.sub(r' for.*', '', author_info)[1:]
    else:
        # remove 'By '
        author = author_ele.text[3:]

    return author, date

def scrapeContent(string):
    #returns empty if nothing is found

    # articles from CES shows redundant info, remove after 'More CES 2013 Coverage'
    # script lang needs to be removed


    soup = BeautifulSoup(string, 'html.parser')
    article_content_ele = soup.find('section', attrs={'class':'article-content'})
    if not article_content_ele:
        return ''

    # clean
    raw_article = article_content_ele.text

    # endlines after sentances needs to be dealt with seperatly, to avoid
    # mashing sentences together
    art_wo_endlines = re.sub(r'\.\n', '. ', raw_article)
    art_wo_endlines = re.sub(r'\n+', '', art_wo_endlines)

    # remove brackets, greedy
    art_wo_script = re.sub(r'\{.*\}', '', art_wo_endlines)

    # some CES stuff that was in many articles
    article = re.sub(r'More CES 2013 Coverage.*', '', art_wo_script)

    return article

if __name__ == '__main__':

    conf = configparser.ConfigParser()
    conf.read('config.cfg')

    file_name_in = conf['SCRAPE']['file_name_in']
    file_name_out = conf['SCRAPE']['file_name_out']

    file_in = open(file_name_in, 'r')
    file_out = open(file_name_out,  'w')

    csvr = csv.reader(file_in)
    csvw = csv.writer(file_out, delimiter='\t')

    # add header to new file
    header = ['url', 'title', 'author', 'time_of_post', 'content']
    csvw.writerow(header)

    # skipp header form file_in
    csvr.__next__()

    amt_done = 1
    for row in csvr:

        # get html
        url_name = row[0]
        try:
            resp = requests.get(url_name)

            if resp.status_code == 200:

                    # scrape
                    title = scrapeTitle(resp.text)
                    author, date = scrapeAuthorDate(resp.text)
                    content = scrapeContent(resp.text)

                    # write to file
                    r = [url_name, title, author, date, content]
                    csvw.writerow(r)

                    print('Finnished with link number {}'.format(amt_done))
                    amt_done += 1

        except KeyboardInterrupt:
            sys.exit()
