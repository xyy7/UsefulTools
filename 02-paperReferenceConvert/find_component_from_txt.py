import re

DEBUG = True

# 从pdf中直接copy的参考文献，不能很好地处理换行符号
def correct(oldfile, newfile):
    with open(oldfile,
              encoding="utf8") as ofile, open(newfile, "w",
                                              encoding="utf8") as nfile:
        contents = ofile.read()
        # 根据[]或者结尾$来分割，并去除\n
        pattern = r"(\[\d*?\].+?)(?=\[|$)"
        res = re.findall(pattern, contents, re.S)
        for i, r in enumerate(res):
            r = r.replace("\n", "") # 可能有多个\n
            nfile.write(r + "\n")   # 末尾添加\n
            if DEBUG:
                print(i+1, r)


# 提取一作姓名
def get_author1list(file):
    with open(file, encoding="utf8") as f:
        contents = f.readlines()
        author1s = []
        for i, c in enumerate(contents):
            # ,|and: 有2个以上作者，只有两个作者，只有一个作者
            pattern = r"\[\d*\](.*?)(?:,|and|\.)"  
            res = re.search(pattern, c)
            a1 = res.group(1)
            author1s.append(a1)
            if DEBUG:
                print(i+1, a1)
    return author1s


# 提取标题
def get_titlelist(file):
    with open(file, encoding="utf8") as f:
        contents = f.readlines()
        titles = []
        for i, c in enumerate(contents):
            res = re.split(r"\.", c)
            # 如果人名没有句号，则第二个最长的；如果有句号，则句号之间，第一个最长的
            for j, r in enumerate(res):
                if len(r) > 20 and j != 0:
                    break
            titles.append(r)
            if DEBUG:
                print(i + 1, r)
    return titles


if __name__ == "__main__":
    OLD = "paper.txt"
    FILE = "new.txt"  # 包含直接的参考文献，而不是bib
    correct(OLD, FILE)
    get_author1list(FILE)
    get_titlelist(FILE)
