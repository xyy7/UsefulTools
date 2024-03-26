* read_excel函数会默认把表格的第一行为列索引名。另外，对于行索引名来说，默认从第二行开始编号（因为默认第一行是列索引名，所以默认第一行不是数据），如果不特意指定，则自动从0开始编号

* 安装：

  * ```
    pip install pandas # 以及其他依赖的xls库
    ```

* 读取：`sheet = pd.read_excel(filename)`

* 保存：`result_excel.to_excel(filename)`

* 分组：`grouped = sheet.groupby('科目名称',as_index=False)`

  * ```
    result_df = grouped.apply(lambda x: x.sort_values(by='项目支出', ascending=False).head(head))
    ```

* 排序：

  * ```
    result_df.sort_values(by=["科目名称","凭证日期","项目支出"],inplace=True,ascending=True)
    ```

    

  

