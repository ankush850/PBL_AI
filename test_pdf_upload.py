import requests

url = "http://127.0.0.1:5000/api/summarize"
file_path = "app/static/uploads/Final-Report.pdf"

with open(file_path, "rb") as f:
    files = {"file": ("Final-Report.pdf", f, "application/pdf")}
    response = requests.post(url, files=files)

print("Status code:", response.status_code)
print("Response JSON:", response.json())
