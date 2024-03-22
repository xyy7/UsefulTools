import re
from pprint import *

# 没有解决太特殊的情况，比如：名称中也含有@
# Neural Compression Workshop @ ICLR
DEBUG = True

## 输入文件名
# 按照@分割
def get_paperlist(filename):
    with open(filename, "r", encoding="utf8") as file:
        contents = file.read()
    pattern = r"@.*?(?=@|$)"  # 要么遇到下一个@，要么结尾
    res = re.findall(pattern, contents, re.S)  # re.S可以忽略\n
    papers = []
    for i, r in enumerate(res):
        if DEBUG:
            print(i,r)
        papers.append(r)
    return papers


def get_metalist(filename):
    papers = get_paperlist(filename)
    
    # metalist = [parse_one_meta(paper) for paper in papers]
    metalist = []
    for i, paper in enumerate(papers):
        try:
            one_meta = parse_one_meta(paper)
            if DEBUG:
                print("\ndebuging...\n"*10)
                pprint(one_meta)
            metalist.append(one_meta)
        except:
            print(i,"cannot convert raw to meta!")
    return metalist


def convert2concise(filename, inplace=False):
    newfile = filename if inplace else 'new_' + filename
    metalist = get_metalist(filename)
    with open(newfile, 'w') as file:
        for i, meta in enumerate(metalist):
            try:
                consise_bib = get_one_concise_bib(meta)
                file.write(consise_bib + '\n\n')
            except:
                print(i, "cannot get consise bib from meta!")
                pprint(meta)


def convert2txt(filename):
    newfile = filename.replace('bib', 'txt')
    metalist = get_metalist(filename)
    with open(newfile, 'w') as file:
        for i, meta in enumerate(metalist):
            file.write(f'[{i+1}]' + get_one_txt(meta) + '\n')


# 直接提取某个属性名
def get_attrlist(filename, attr="title"):
    with open(filename, "r", encoding="utf8") as file:
        contents = file.read()
    pattern = r"(?<!\w){} = \{(.*?)\}".format(
        attr)  # 只要title中括号中的题目，不要booktitle
    res = re.findall(pattern, contents, re.S)  # re.S可以忽略\n
    attrs = []
    for i, r in enumerate(res):
        # print(i,r)
        attrs.append(r)
    return attrs


## 解析每一段文本
# 传入一个论文的文本数据，解析成一个meta
def parse_one_meta(content):
    meta = {}
    # 匹配该论文类型
    p0 = r"@(.*?){"
    type = re.search(p0, content).group(1)
    meta["type"] = type

    # 匹配形如： xx = {}的句子
    p1 = r"\W*(.*?)\s?=\s?\{(.*?)\}"
    res = re.findall(p1, content)
    for r in res:
        meta[r[0].strip()] = r[1].strip()

    if "booktitle" in meta.keys():
        meta["journal"] = meta["booktitle"]
    if "journal" in meta.keys():
        meta["booktitle"] = meta["journal"]

    return meta


## 通过meta进一步加工
# 传入一个论文的meta数据，获取方便辨认的标签
def get_one_label(meta):
    booktitle = get_title_abbreviation(meta['booktitle'])
    a1 = meta['author'].split()[0].replace(',', '')
    t1 = meta['title'].split()[0].replace(':', '')
    label = meta['year'] + '_' + booktitle + '_' + a1 + '_' + t1
    meta['label'] = label
    return label


# 解析booktitle缩写
def get_title_abbreviation(booktitle):
    # 利用正则表达式来匹配序列
    booklist = ['arXiv', 'TCSVT', 'TPAMI', 'CVPRW', 'CVPR','WACV','ICCV', 'ACCV','ECCV',  \
    'LNCS', 'NIPS','ISCaS','SPL', "JSTSP", 'ICIP', 'ICLR', 'TIP', 'AAAI', 'ICASSP', 'SiPS', "TM",\
    'MMSP','MM','JSAC', "JVCI"]
    patterns = []
    for bk in booklist:
        pattern = r''
        for b in bk:
            pattern += b + r'(?:\w|\s)*'
        patterns.append(pattern)

    name = ''
    for i, pattern in enumerate(patterns):
        if re.search(pattern, booktitle) is not None:
            name = booklist[i]
            break

    if name == 'TM':
        return 'TMM'
    if name == 'ISCaS':
        return 'ISCAS'
    return name


# 传入一个论文的meta数据，返回一个最必要的bib格式
def get_one_concise_bib(meta):
    not_need_list = [
        'notes', 'abstract', 'issn', 'copyright', 'language', 'label', 'type'
    ]
    meta['label'] = get_one_label(meta)
    bib = f"@{meta['type']}{{{meta['label']},\n"
    for k, y in meta.items():
        if k in not_need_list:
            continue
        bib += k + ' = ' + '{' + y + '}\n'
    bib += '}'
    # print(bib)
    return bib


# 传入一个论文的meta数据，形成一条直接的参考文献
# 参考谷歌学术的引用bib，unrst格式
def get_one_txt(meta):
    author = convert_author(meta['author'])
    title = meta["title"] + ". "
    doi = convert_DOI(meta["URL"]) if "URL" in meta.keys() else ""
    booktitle = meta["booktitle"] + ", "
    year = meta["year"] + ". "

    # 期刊
    if meta["type"] == "article":
        # Zongyu Guo, Zhizheng Zhang, Runsen Feng, and Zhibo Chen. Causal contextual prediction
        # for learned image compression. IEEE Transactions on Circuits and Systems for Video
        # Technology, 32(4):2329–2341, 2021.
        if "volume" in meta.keys():
            volume = meta["volume"]
            number = f'({meta["number"]}): ' if "number" in meta.keys(
            ) else ":"
        else:
            volume = ""
            number = ""
        pages = convert_page(
            meta["pages"]) + ", " if "pages" in meta.keys() else ""
        return author + title + booktitle + volume + number + pages + year

    # 会议
    elif meta["type"] == "inproceedings":
        # Fabian Mentzer, Eirikur Agustsson, Michael Tschannen, Radu Timofte, and Luc Van Gool.
        # Conditional probability models for deep image compression. In Proceedings of the IEEE
        # Computer Society Conference on Computer Vision and Pattern Recognition, pages 4394–
        # 4402, Salt Lake City, UT, United states, 2018. IEEE.
        pages = ("pages " + convert_page(meta["pages"]) +
                 ", " if "pages" in meta.keys() else "")
        address = meta["address"] + ", " if "address" in meta.keys() else ""
        publisher = meta["publisher"] + "." if "publisher" in meta.keys(
        ) else ""
        return author + title + booktitle + pages + address + year + publisher


## 进一步处理
# 将作者名称转化成非逗号格式
def convert_author(author, abbr=False):
    """
    逗号前是姓氏，逗号后面是名称。
    姓氏取完整，名称取首字母缩写。
    返回一个 'Person a, b and c. '格式的字符串 
    
    eg: bib中的人名格式：
    中文名：Fu, Chunyang and Li, Ge and Song, Rui and Gao, Wei and Liu, Shan.
    英文名：Ladune, Theo and Philippe, Pierrick and Hamidouche, Wassim and Zhang, Lu and Deforges, Olivier.
    Args:
        author: 输入是meta[author],格式如上，以英文逗号结尾
        full: 全写/缩写
    """
    au = author.split(" and ")
    namestr = ""
    for i, a in enumerate(au):
        name = a.split(", ")
        last_name = name[0]
        first_name = name[1] if abbr else name[1][0]
        # 如果是倒数第二个，那么逗号改为and
        if i == len(au) - 2:
            namestr += first_name + " " + last_name + " and "
            continue
        if i == len(au) - 1:
            namestr += first_name + " " + last_name + ". "
            break
        # 姓名中间没有逗号，姓氏放在后面，再添加逗号。
        namestr += first_name + " " + last_name + ", "
    return namestr


def convert_page(page):
    return page.replace("--", "-").replace(" ", "")


def convert_DOI(DOI):
    # http://dx.doi.org/10.48550/arXiv.2202.06028
    return f' [DOI: {re.search("doi.org/(.*)", DOI).group(1)}]'


if __name__ == "__main__":
    # FILE = "anystyle.bib"
    # NEW_FILE = "anystyle-mine.bib"
    FILE="Engineering_Village_BIB_3-18-2024_115532236.bib"
    NEW_FILE = "Engineering_Village_BIB_3-18-2024_115532236-new.bib"
    convert2concise(FILE)
    # convert2txt(FILE)
