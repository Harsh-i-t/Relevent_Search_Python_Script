# Import the required modules
from time import sleep
import requests
import webbrowser
import pandas as pd
from bs4 import BeautifulSoup
from pymongo import MongoClient
import pdfkit

# Take the user input as the search query
query = input("Enter your search query: ")
print("Sit Back & Relax , Searching and Redirecting.....")
sleep(2)

# Define the Chrome browser path
edge_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(edge_path))

# Use the requests module to get the Google search results page
response = requests.get("https://www.google.com/search?q=" + query)

# Use the BeautifulSoup module to parse the HTML content of the response
soup = BeautifulSoup(response.text, "html.parser")

# Find all the elements that contain the links to the webpages
links = soup.find_all("a", href=lambda href: href and "/url?q=" in href)

# Create an empty list to store the titles and urls of the webpages
results = []

# Loop through the first five links
for link in links[:5]:
    # Get the url of the webpage by removing the prefix and suffix
    url = link["href"].replace("/url?q=", "").split("&")[0]
    
    # Get the title of the webpage by getting the text content of the link element
    title = link.text
    
    # Append a dictionary with the title and url to the results list
    results.append({"title": title, "url": url})
    
    # Open the webpage in a new tab using the webbrowser module
    webbrowser.get('chrome').open_new_tab(url)
    
# Print the results list
# print(results)

# Create a pandas dataframe from the results list
df = pd.DataFrame(results)

# Save the dataframe as an excel file using the pandas module
df.to_excel(f"{query}.xlsx", index=False)

# Connect to a MongoDB database using the pymongo module
client = MongoClient("mongodb://localhost:27017/")
db = client["google_search"]
collection = db["results"]

# Insert the results list as documents into the MongoDB collection
collection.insert_many(results)

print("MongoDB Database Updated : Success")
print("Excel Sheet Updated : Success")

# Get the url of the first webpage from the results list
def get_the_working_url(results):
    for i in range(len(results)):
            response = requests.get(results[i]["url"])
            # If the response status code is 200, it means the url is working
            if response.status_code == 200:
                # Print the url and break the loop
                return results[i]["url"] 

first_url = get_the_working_url(results)


def webpage_to_pdf(url):

    #Define path to wkhtmltopdf.exe
    path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

    #Point pdfkit configuration to wkhtmltopdf.exe
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

    #Convert Webpage to PDF
    pdfkit.from_url(url, output_path=f'{query}.pdf', configuration=config)

webpage_to_pdf(first_url)
print("Webpage copied to PDF : Success")
