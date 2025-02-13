import requests as req
from bs4 import BeautifulSoup
import pandas as pd

page= req.get("https://en.wikipedia.org/wiki/Samsung")   #requesting the page
if page.status_code == 200:
    print("Page downloaded successfully!")

soup = BeautifulSoup(page.content, 'html.parser')   #parsing the page

link_url = [a['href'] for a in soup.find_all('a', href=True)]   #finding all the links in the page
link_text = [a.text for a in soup.find_all('a', href=True)]  #finding all the text in the page

text_and_links = pd.DataFrame(list(zip(link_text, link_url)), columns=['Text', 'Link']) #creating a dataframe of text and links

#finding the infobox
infobox = soup.find('table', class_='infobox')

if infobox:     
    rows = infobox.find_all('tr')
    data = {}
    for row in rows: 
        header = row.find('th')
        value = row.find('td')
        if header and value:
            data[header.text.strip()] = value.text.strip()
else: print("No infobox found")

info_table = pd.DataFrame(list(data.items()), columns=['Attribute', 'Value']) #creating a dataframe of the infobox

#finding all the headings in the page
topics = [heading.text.strip() for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]

samsung_topics = pd.DataFrame(topics, columns=['Topic']) #creating a dataframe of the headings

#saving the dataframes to an excel file
excel_file = 'Web_Scraping_Samsung_Wiki.xlsx'
with pd.ExcelWriter(excel_file) as writer:
    text_and_links.to_excel(writer, sheet_name='Samsung Links', index=False) #each dataframe is saved in a separate sheet
    info_table.to_excel(writer, sheet_name='Samsung Info', index=False)
    samsung_topics.to_excel(writer, sheet_name='Samsung Topics', index=False)
print(f"Dataframes saved to {excel_file} successfully!") #printing the success message