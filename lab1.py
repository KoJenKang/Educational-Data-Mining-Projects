import requests
import  json

url = "https://ntnu-ml.openai.azure.com/openai/deployments/ntnu-ml-gpt4-32k/chat/completions?api-version=2023-07-01-preview"
headers = {
    "Content-Type": "application/json",
    "api-key": ""  # API key
}
#利用 prompt 提示 output format/少量樣本提示（Few-Shot Prompting）讓回應結果符合我們期望的樣子
payload = {
    "messages": [
        {
            "role": "system",
            "content": "根據 ``` 中提供的 rating.csv 資料，用協同過濾的概念推薦餐廳給使用者，請以 json array 格式回答\n```\ncustomerId,restaurantId,rating\nc1,r2,3\nc1,r3,1\nc1,r5,3\nc1,r6,2\nc2,r1,3\nc2,r3,1\nc2,r5,1\nc2,r6,1\nc3,r4,3\nc3,r5,3\nc3,r6,3\nc4,r1,1\nc4,r4,1\nc4,r5,3\nc5,r2,1\nc5,r3,2\nc5,r4,3\nc6,r2,3\nc6,r3,3\nc6,r5,3\nc7,r2,3\nc7,r3,3\nc7,r4,1\nc8,r1,2\nc8,r2,1\nc8,r5,1\nc8,r6,2\n```，舉例來說回傳的結果中需要包含推薦的餐廳的欄位，像是「recommendations:r1、r2」。"
        },
        {
            "role": "user",
            "content": "c2"
        }
    ],
    "max_tokens": 800,
    "temperature": 0.5,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "top_p": 0.95,
    "stop": None
}

#Azure API call取得結果，並處理回傳資料
try:
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        # API call was successful
        data = response.json()
        result=data["choices"][0]
        resultdata=json.loads(result["message"]["content"])
        customer=resultdata[0]["customerId"]
        recommendation=resultdata[0]["recommendations"]
        print("Customer ID:", customer,"\n","Recommendations:", recommendation)
    else:
        # API call failed
        print("API call failed with status code:", response.status_code)
except Exception as e:
    print("An error occurred during the API call:", e)
