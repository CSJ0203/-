
import pandas as pd

table = pd.read_html('https://mizykk.tistory.com/39', header=0, encoding='utf-8')
print(table)