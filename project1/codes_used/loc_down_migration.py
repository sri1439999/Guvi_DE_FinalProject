import requests
import zipfile
import io
from io import BytesIO

#Downloading & extracting the file to localmachine

url = 'https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip'

headers= {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
print("download started")
target_loaction = 'D:\GUVI\project\submissions_unzip'
response = requests.get(url,headers = headers, stream= True)
print(response)

zip_file = zipfile.ZipFile(io.BytesIO(response.content))
zip_file.extrectall(target_loaction)

print("download finished")