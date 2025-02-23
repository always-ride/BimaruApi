import requests

url = "https://bimaruapi.fly.dev/api/solve"
headers = {"Content-Type": "text/plain"}
data = (
"6 | . . . . . . . . ~ .\n"
"0 | . . . . . . . . . .\n"
"1 | . . . . . . . . . .\n"
"0 | . . . . . . . . . .\n"
"2 | . . . . . . . . . .\n"
"3 | . . . . . . . . . .\n"
"0 | . . . . . . . . . .\n"
"2 | . . . . . . . . . .\n"
"3 | . ~ . . . . . . . .\n"
"3 | . . . . . . . . . .\n"
"    3 4 1 4 2 0 1 0 3 2"
)

response = requests.post(url, data=data, headers=headers)

print("Status Code:", response.status_code)
print("Response:\n" + response.text)
