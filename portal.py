import requests
from bs4 import BeautifulSoup



url = "https://portal.ku.ac.ke/secure/Student/Reg/OnlineRegStep1.aspx?sm=3"

page = requests.get(url)

print(page.content)


soup = BeautifulSoup(page.content, "lxml")

soup.prettify

print(soup)

