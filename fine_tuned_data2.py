from opencc import OpenCC
import pandas as pd 
import re
import json 
def scrape_poem_data():
    import requests
    from bs4 import BeautifulSoup
    num=["001","034","041","070","083","163","216","217","246","254","305"]
    data_store=""
    converter = OpenCC('s2twp')
    for i in range(1,12):
        if i<10:
            url = f"https://www.millionbook.net/gd/h/hengtangtuishi/tssb/00{i}.htm#{num[i-1]}"
        else:
            url = f"https://www.millionbook.net/gd/h/hengtangtuishi/tssb/0{i}.htm#{num[i-1]}"
        response = requests.get(url)
        response.encoding = 'big5'
        content = response.text
        result = BeautifulSoup(content, "html.parser")
        data=result.find_all("span",{"class":"swy1"})
        for i in data:
            t=converter.convert(i.text)
            data_store+=t
    lst=data_store.split("=============================")
    documents = lst[1:]
    documents = [s.replace('\r', '') for s in documents]
    name_pattern=r'《(.*?)》'
    author_pattern=r'作者：(.*?)\n'
    peom_pattern= r'作者：.*?\n(.*?)\n\n【註解】'
    exp_pattern = r'\n\n【韻譯】：\n(.*?)\n\n【評析】'
    mean_pattern= r'【評析】：\n.*?(\S.*?)\n'
    all_dict={}
    for i in documents:
        match1 = re.search(name_pattern,i)
        match2 = re.search(author_pattern,i)
        match3 = re.search(peom_pattern,i,re.DOTALL)
        match4 = re.search(exp_pattern,i,re.DOTALL)
        match5 = re.search(mean_pattern,i,re.DOTALL)
        name=match1.group(1).replace('\n',"")
        author=match2.group(1).replace('\n',"")
        poem=match3.group(1).replace('\n',"")
        exp=match4.group(1).replace('\n',"")
        mean=match5.group(1).replace('\n',"").replace("�U�U","")
        # print(name,author)
        all_dict[f"{name}"]={}
        all_dict[f"{name}"]["作者"]= author
        all_dict[f"{name}"]["詩"]=poem
        all_dict[f"{name}"]["解釋"]= exp
        all_dict[f"{name}"]["詩意"]= mean    
    return all_dict

#instruction, context, response, category 請給我這首詩的詩名、作者、解析以及這首詩想表達的意義，
data=scrape_poem_data()
print(data)
datafram_dic={'input':[],"output":[]}

for i,j in data.items():
    datafram_dic['input'].append(f"我想要知道關於下面這首詩的資訊，請給我這首詩的詩名、作者、解析以及這首詩想表達的意義: {j['詩']}")
    datafram_dic["output"].append(f"(1) 詩名: {i} (2) 作者: {j['作者']}  (3) 解析: {j['解釋']}  (4) 詩意: {j['詩意']}")
    

data_fram=pd.DataFrame(data=datafram_dic)
file_name = 'fine_tuned_data2.xlsx'
data_fram.to_excel(file_name) 
print('DataFrame is written to Excel File successfully.')
# Write data to JSONL file
df = pd.read_excel('fine_tuned_data2.xlsx')

# Determine the number of rows for each split (80% and 20%)
num_rows_80 = int(len(df) * 0.8)

# Open files for writing JSONL (80% and 20%)
with open('train.jsonl', 'w', encoding='utf-8') as jsonl_file_80, open('test.jsonl', 'w', encoding='utf-8') as jsonl_file_20:
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Select only the second and third columns
        selected_row = row[['input', 'output']]
        # Convert selected row to JSON
        json_data = selected_row.to_json(orient='columns', force_ascii=False)
        
        # Write JSON data to appropriate JSONL file
        if index < num_rows_80:
            jsonl_file_80.write(json_data + '\n')
        else:
            jsonl_file_20.write(json_data + '\n')