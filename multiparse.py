import os
import re
import pickle
import multiprocessing
from wiki_dump_reader import Cleaner, iterate

ROOT = os.getcwd()[:-20]


def stream(path):
    cleaner = Cleaner()
    name = re.search(r'.+multistream(\d).+', path)
    if name:
        print(f'File {name.group(1)} is in process')
    res = dict()
    for title, text in iterate(path):
        text = cleaner.clean_text(text)
        cleaned_text, links = cleaner.build_links(text)
        links = [{'link': x['link'], 'text': x['text']} for x in links]
        res[title] = (cleaned_text, links)
    pickle.dump(res, open(path + '.bin', 'wb'))
    # return res

if __name__ == '__main__':
    lang = input('Select language, worm: ')
    files = [os.path.join(f'{ROOT}/dumps/{lang}', n) for n in os.listdir(f'{ROOT}/dumps/{lang}') if (not n.endswith('.bin') and 'multistream' in n)]
    
    if len(files) < 7:
        print('Number of files less than 7. Start monopool')
        pool = multiprocessing.Pool(processes = len(files))
        pool.map(stream, files)

    else:
        print(f'Number of files is {len(files)}. Start split pool')
        files1, files2 = files[:len(files) // 2], files[len(files) // 2:]
        pool = multiprocessing.Pool(processes = len(files1))
        pool.map(stream, files1)
        print('First part is processed')

        pool = multiprocessing.Pool(processes = len(files2))
        pool.map(stream, files2)
        print('Second part is processed')



