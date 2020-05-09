from urllib.request import urlretrieve
from random import randint
import tarfile
import os
import re

data_source = [
    ('http://data.statmt.org/wmt17/translation-task/training-parallel-ep-v8.tgz', 'training-parallel-ep-v8.tgz'),
    ('http://data.statmt.org/wmt17/translation-task/rapid2016.tgz', 'rapid2016.tgz'),
    ('http://data.statmt.org/wmt17/translation-task/books.lv-en.v1.tgz', 'books.lv-en.v1.tgz'),
    ('http://data.statmt.org/wmt17/translation-task/dcep.lv-en.v1.tgz', 'dcep.lv-en.v1.tgz')
]


def general_clean(raw):
    cleaned = re.sub(r'\(|\)|-|”|"|\'|:|«|»|\+|/|\\|;', '', raw)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    cleaned = re.sub(r'^[0-9]+.(\s+)?$', '', cleaned)
    cleaned = re.sub(r'^(,|.(\s+)?)$', '', cleaned)

    return cleaned.strip()


def clean(en_source, lv_source):
    with open(en_source, 'r') as en_data:
        with open(lv_source, 'r') as lv_data:
            for en_raw, lv_raw in zip(en_data, lv_data):
                if not en_raw.strip() or any(lookup in en_raw.lower() for lookup in ['email:', 'e-mail:', 'fax:', 'phone:', 'mob.:', 'tel.:', 'website:',
                                                                                     'article t', 'ibid', 'press release', 'book i', 'book v', 'chapter i',
                                                                                     'chapter v', 'chapter x', 'oral question']):
                    continue

                if en_raw.strip().lower() in ['by', 'to the commission', 'to the council', 'and']:
                    continue

                en_cleaned = general_clean(en_raw)
                lv_cleaned = general_clean(lv_raw)

                if not en_cleaned or en_cleaned == lv_cleaned:
                    continue

                yield en_cleaned, lv_cleaned


data_to_clean = [
    ('rapid2016.en-lv.en', 'rapid2016.en-lv.lv'),
    ('training/europarl-v8.lv-en.en', 'training/europarl-v8.lv-en.lv'),
    ('farewell/farewell.en', 'farewell/farewell.lv'),
    ('dcep.en-lv/dcep.en', 'dcep.en-lv/dcep.lv')
]


def maybe_download_and_extract_data():
    for url, file in data_source:
        source = os.path.join('data', file)

        if os.path.exists(source):
            continue

        urlretrieve(url, source)

        tar = tarfile.open(source)
        tar.extractall('./data')
        tar.close()


def maybe_clean_data():
    for en_source, lv_source in data_to_clean:
        clean_path = os.path.join('data', 'cleaned')
        os.makedirs(clean_path, exist_ok=True)
        en_clean_path = os.path.join(clean_path, os.path.basename(en_source))
        lv_clean_path = os.path.join(clean_path, os.path.basename(lv_source))

        en_path = os.path.join('data', en_source)
        lv_path = os.path.join('data', lv_source)

        if os.path.exists(en_clean_path):
            continue

        with open(en_clean_path, 'w') as en_dest:
            with open(lv_clean_path, 'w') as lv_dest:
                for en, lv in clean(en_path, lv_path):
                    en_dest.write(f'{en}\n')
                    lv_dest.write(f'{lv}\n')


def validate(en_file, lv_file):
    en_source = os.path.join('data', 'cleaned', en_file)
    lv_source = os.path.join('data', 'cleaned', lv_file)
    sample = [randint(0, 100000) for _ in range(10)]

    with open(en_source, 'r') as en_data:
        with open(lv_source, 'r') as lv_data:
            for i, (en, lv) in enumerate(zip(en_data, lv_data)):
                if i in sample:
                    print(f'EN: "{en}" | LV: "{lv}"')


if __name__ == '__main__':
    maybe_download_and_extract_data()
    maybe_clean_data()
    validate('rapid2016.en-lv.en', 'rapid2016.en-lv.lv')
    validate('europarl-v8.lv-en.en', 'europarl-v8.lv-en.lv')
    validate('farewell.en', 'farewell.lv')
    validate('dcep.en', 'dcep.lv')
