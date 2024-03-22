1. find_component_from_txt.py:
* txt文本中，包含可直接观看（pdf或者word中）的多条参考文献。
  > eg. [23] Zongyu Guo, Zhizheng Zhang, Runsen Feng, and Zhibo Chen. Causal contextual prediction
  > for learned image compression. IEEE Transactions on Circuits and Systems for Video
  > Technology, 32(4):2329–2341, 2021.
* correct：将从pdf中复制的参考文献去除多余的换行和空格。
* get_author1list：可以返回作者（一作）列表。
* get_titlelist：可以返回论文标题。
2. find_component_from_bib.py:
* convert2concise：去除bibtex中一般不需要使用的多余的信息。[bib->bib]
* convert2txt：将bib文件，转化成可直接观看（pdf或者word中）的参考文献（txt格式）。[bib->txt]
* get\*,parse\*: 提取bib中meta信息。

