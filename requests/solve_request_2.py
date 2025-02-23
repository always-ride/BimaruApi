import requests

url = "https://bimaruapi.fly.dev/api/solve"
headers = {"Content-Type": "text/plain"}
data = (
"2 | . . . . . > . . . .\n"
"1 | . . . . . . . . . .\n"
"3 | . . . . . . . . . .\n"
"5 | . . . . . . . . . .\n"
"1 | . . . . . . . . . .\n"
"4 | . . ~ . v . . . . .\n"
"0 | . . . . . . . . . .\n"
"0 | . . . . . . . . . .\n"
"4 | . . . . . . . . . .\n"
"0 | . . . . . . . . . .\n"
"    1 2 4 1 5 1 1 1 4 0"
)

response = requests.post(url, data=data, headers=headers)

print("Status Code:", response.status_code)
print("Response:\n" + response.text)
