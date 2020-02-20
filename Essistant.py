'''
Welcome to Essistant v1.5, Reforge & Simplify
'''

# pyinstaller -i "C:\Users\LynnL\Pictures\Saved Pictures\sadpanda.ico" -p "C:\Program Files (x86)\Microsoft Visual studio\Shared\Python37_64" -p "C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\Lib" -p "C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\Lib\site-packages" -F Essistant.py

from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import progressbar as pb
# import sys

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/\
    537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}

proxies = {
    "http": "socks5h://127.0.0.1:1080",
    "https": "socks5h://127.0.0.1:1080",
}


def SEARCH(artist):
    url = 'https://e-hentai.org/lofi/?f_search=chinese+artist%3A'\
        + artist + '&f_apply=Search'
    try:
        response = get(url, proxies=proxies, headers=headers, timeout=5)
    except ConnectionError:
        # print(sys.exc_info()[0])
        print('Failed to refresh, please try to change your IP adress.\n')
        return
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        work = soup.select('a.b')
        time = soup.select('td.ip')
        return work[0].contents[0], time[1].contents[0]
    except AttributeError:
        print('Seems like there are no results found.\n')
        return


def ADD():
    artist = input('Artist: ')
    try:
        log = pd.read_csv('log.csv', encoding='utf-8')
    except FileNotFoundError as e:
        # print(sys.exc_info()[0])
        print('WARNING: ' + str(e))
        print('Creating new log file...\n')
        log = pd.DataFrame(columns=['Artists', 'Works', 'Time'])
    for x in range(len(log)):
        if artist == log.iloc[x, 0]:
            print('You have already added this artist.\n')
            return
    latest_work, post_time = SEARCH(artist)
    log = log.append(
        {
            'Artists': artist,
            'Works': latest_work,
            'Time': post_time
        },
        ignore_index=True)
    log.to_csv('log.csv', index=False, encoding='utf-8')
    print('Successfully added!\n')


def REFRESH():
    print('Refreshing...')
    news = []
    try:
        log = pd.read_csv('log.csv', encoding='utf-8')
    except FileNotFoundError:
        print('The list is empty.\n')
        return

    widgets = [
        pb.AnimatedMarker(markers='|\\-/'), ' ', 'Progress: ',
        pb.Bar(marker='=', left='[', right=']'), ' ',
        pb.Counter(), ' ',
        pb.Percentage(), ' ',
        pb.AdaptiveETA()
    ]
    pbar = pb.ProgressBar(widgets=widgets, maxval=len(log)).start()

    for x in range(0, len(log)):
        latest_work, post_time = SEARCH(log.iloc[x, 0])
        if post_time != log.iloc[x, 2]:
            log.iloc[x, 1] = latest_work
            log.iloc[x, 2] = post_time
            news.append(log.iloc[x, 0] + ' - ' + post_time)
        pbar.update(x + 1)
    log.to_csv('log.csv', index=False, encoding='utf-8')
    print('\n%-2d new work(s) found!\n' % len(news) + '-' * 20)
    for x in news:
        print(x)
    print('-' * 20)
    return


def main():
    REFRESH()
    while True:
        opt = input(
            'a. add\nb. refresh\nClick Enter to exit\nChoose your action:\n')
        print()
        if opt == 'a':
            ADD()
        elif opt == 'b':
            REFRESH()
        else:
            exit()
    return


if __name__ == '__main__':
    main()
