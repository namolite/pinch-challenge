# -*- coding: utf-8 -*-
import urllib3
import json
import os


def fetch_problem():
    base_url = 'https://leetcode.com/graphql/'
    usr_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
    data = {
        "query": "\n    query questionOfToday {\n  activeDailyCodingChallengeQuestion {\n    date\n    userStatus\n    link\n    question {\n      acRate\n      difficulty\n      freqBar\n      frontendQuestionId: questionFrontendId\n      isFavor\n      paidOnly: isPaidOnly\n      status\n      title\n      titleSlug\n      content\n      hasVideoSolution\n      hasSolution\n      topicTags {\n        name\n        id\n        slug\n      }\n    }\n  }\n}\n    ",
        "variables": {}
    }
    encoded_data = json.dumps(data).encode('utf-8')

    r = urllib3.PoolManager().request(
        'POST',
        base_url,
        body=encoded_data,
        headers={
            'Content-Type': 'application/json',
            'User-Agent': usr_agent
        },
    )
    if r.status != 200:
        print(r.status + r.data)
    response_content = json.loads(r.data)
    return response_content


# TODO data proceeding
def tags(arr):
    re = ''
    for i in range(len(arr)):
        re += ('#' + arr[i - 1]['name'] + '  ')
    return re


def p(c):
    data = c['data']['activeDailyCodingChallengeQuestion']
    qt = data['question']

    dct = {
        'dt': data['date'],
        'tt': qt['frontendQuestionId'] + '. ' + qt['title'],
        'di': qt['difficulty'],
        'tag': tags(qt['topicTags']),
        'twn': qt['title'],
        'acc': str(round(qt['acRate'], 2)),
        'dtl': qt['content'],
        'url': 'https://leetcode.com' + data['link']
    }
    return dct


md_map = {
    '\n\n': '\n', '	': ' ',
    '<p>': '', '</p>': '',
    '<ul>': '', '</ul>': '',
    '<li>': '- ', '</li>': '',
    '<ol>': '', '</ol>': '',
    '<sup>': '^', '</sup>': '',
    '<pre>': '```', '</pre>': '```',
    '<code>': '`', '</code>': '`',
    '<strong>': '**', '</strong>': '**',
    '&lt;': '<', '&gt;': '>', '&quot;': '"', '&le;': '≤', '&ge;': '≥', '&nbsp;': ' '
}
txt_map = {
    '\n': '', '	': '',
    '<p>': '', '</p>': '',
    '<ul>': '', '</ul>': '',
    '<li>': '- ', '</li>': '',
    '<ol>': '', '</ol>': '',
    '<sup>': '^', '</sup>': '',
    '<pre>': '', '</pre>': '',
    '<code>': '', '</code>': '',
    '<strong>': '', '</strong>': '',
    '&lt;': '<', '&gt;': '>', '&quot;': '"', '&le;': '≤', '&ge;': '≥', '&nbsp;': ' '
}


def replace_use_a_dict(ct, dic):
    for word, initial in dic.items():
        ct = ct.replace(word.lower(), initial)
    return ct


def add_info(text, used_map):
    if used_map == 'md':
        ex = '# ' + pb_info['twn'] + '\n' + pb_info['di'] + '   acc: ' + pb_info['acc'] + '   tags: ' + pb_info['tag'] + '\nurl: ' + pb_info['url'] + '\n' + text
    else:
        ex = pb_info['twn'] + '\n' + pb_info['di'] + '   acc: ' + pb_info['acc'] + '\ntags: ' + pb_info['tag'] + text + pb_info['url']
    return ex


# TODO output
def md_file(dir_path, pb_dir, title, text):
    filepath = os.path.join(os.getcwd(), dir_path, pb_dir)
    print(filepath)
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    with open(filepath + '/' + title + '.md', 'w') as f:
        f.write(text)


# TODO main
if __name__ == '__main__':
    pb_info = p(fetch_problem())
    md_text = add_info(replace_use_a_dict(pb_info['dtl'], md_map), 'md')
    md_file('problems', pb_info['dt'], pb_info['tt'], md_text)
