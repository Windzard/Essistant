'''
Welcome to Essistant v1.4.7, sync test
'''

# pyinstaller -i "C:\Users\LynnL\Pictures\Saved Pictures\sadpanda.ico" -p "C:\Program Files (x86)\Microsoft Visual studio\Shared\Python37_64" -p "C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\Lib" -p "C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\Lib\site-packages" -F Essistant.py

from requests import get
from bs4 import BeautifulSoup
import xlwt
import xlrd
from xlutils.copy import copy
from datetime import datetime
import progressbar as pb

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/\
    537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
}

proxies = {
    "http": "socks5h://127.0.0.1:1080",
    "https": "socks5h://127.0.0.1:1080",
}


def ADD():
    artist = input('Artist: ')
    try:
        old = xlrd.open_workbook('log.xls')
        oldsheet = old.sheets()[0]
        num = oldsheet.nrows
        new = copy(old)
    except FileNotFoundError as e:
        # print(sys.exc_info()[0])
        print('WARNING: ' + str(e))
        print('Creating new log file.\n')
        old = xlwt.Workbook(encoding='utf-8')
        oldsheet = old.add_sheet('log')
        num = 0
        new = old
    for x in range(num):
        if artist == oldsheet.cell(x, 0).value:
            print('You have already added this artist.\n')
            return
    url = 'https://e-hentai.org/lofi/?f_search=chinese+artist%3A'\
        + artist + '&f_apply=Search'
    response = get(url, proxies=proxies, headers=headers)
    # response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        work = soup.tr.tr.td.a.contents
    except AttributeError as e:
        print('WARNING: ' + str(e))
        print('Sorry, no such artist.\n')
        return
    newsheet = new.get_sheet(0)
    newsheet.write(num, 0, artist)
    newsheet.write(num, 1, work)
    new.save('log.xls')
    print('Successfully added!\n')


def REFRESH():
    print('Refreshing...')
    news = []
    try:
        workbook = xlrd.open_workbook('log.xls')
    except FileNotFoundError:
        print('The list is empty, please add someone before you refresh.\n')
        return
    worksheet = workbook.sheets()[0]
    num = worksheet.nrows
    widgets = [
        pb.AnimatedMarker(markers='|\\-/'), ' ', 'Progress: ',
        pb.Bar(marker='=', left='[', right=']'), ' ',
        pb.Counter(), ' ',
        pb.Percentage(), ' ',
        pb.AdaptiveETA()
    ]
    pbar = pb.ProgressBar(widgets=widgets, maxval=num).start()
    begin = datetime.now()
    for x in range(0, num):
        artist = worksheet.cell(x, 0).value
        url = 'https://e-hentai.org/lofi/?f_search=chinese+artist%3A'\
            + artist + '&f_apply=Search'
        response = get(url, proxies=proxies, headers=headers)
        # response = get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            work = soup.tr.tr.td.a.contents[0]
            if work != worksheet.cell(x, 1).value:
                old = xlrd.open_workbook('log.xls')
                oldsheet = old.sheets()[0]
                num = oldsheet.nrows
                new = copy(old)
                newsheet = new.get_sheet(0)
                news.append(worksheet.cell(x, 0).value)
                newsheet.write(x, 1, soup.tr.tr.td.a.contents)
        except AttributeError:
            print('Failed to refresh, please try to change your IP adress.\n')
            return
        pbar.update(x + 1)
    new.save('log.xls')
    end = datetime.now()
    print('\n%-2d new work(s) found!\n' % len(news) + '-' * 20)
    for x in news:
        print(x)
    print('-' * 20)
    time = (end - begin).total_seconds()
    print('Running time: ' + str(time) + 's\nAverage time: %fs\n' %
          (time / num))
    return


def main():
    REFRESH()
    while True:
        retort = input(
            'a. add\nb. refresh\nClick enter to exit\nChoose your action:\n')
        print()
        if retort == 'a':
            ADD()
        elif retort == 'b':
            REFRESH()
        else:
            exit()
    return


if __name__ == '__main__':
    main()
