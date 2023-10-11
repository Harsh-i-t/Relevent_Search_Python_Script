# Import the required modules
import datetime, re, pdfkit

import requests, webbrowser
import pandas as pd
from bs4 import BeautifulSoup
from pymongo import MongoClient



# Take the user input as the search query
query = input("Enter your search query: ")
print("Sit Back & Relax , Searching and Redirecting.....")


# Define the Chrome browser path
edge_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(edge_path))

# Use the requests module to get the Google search results page
response = requests.get("https://www.google.com/search?q=" + query)

# Use the BeautifulSoup module to parse the HTML content of the response
soup = BeautifulSoup(response.text, "html.parser")





# Connect to a MongoDB database using the pymongo module and 
def Connect_MongoDB_and_Excel(results):

    # Create a pandas dataframe from the results list
    df = pd.DataFrame(results)

    # Save the dataframe as an excel file using the pandas module
    df.to_excel(f"{query}.xlsx",index=False)


    print("Excel Sheet Created : Success")


    client = MongoClient("mongodb://localhost:27017/")
    db = client["google_search"]
    collection = db["results"]

    # Insert the results list as documents into the MongoDB collection
    collection.insert_many(results)

    print("MongoDB Database Updated : Success")


def webpage_to_pdf(url):

    #Define path to wkhtmltopdf.exe
    path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

    #Point pdfkit configuration to wkhtmltopdf.exe
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

    #Convert Webpage to PDF
    pdfkit.from_url(url, output_path=f'{query}.pdf', configuration=config)

def total_Occurance(file_path):

    global num_pages,count

    from pypdf import PdfReader

    reader = PdfReader(file_path)
    num_pages = len(reader.pages)
    text = ''
    for i in range(num_pages):
        text += reader.pages[i].extract_text()

    word = query

    # Finding and counting the word using a regular expression
    pattern = r"\b" + word + r"\b" # \b matches word boundaries
    matches = re.findall(pattern, text, re.IGNORECASE) # re.IGNORECASE ignores case sensitivity
    count = len(matches)




# Find all the elements that contain the links to the webpages
links = soup.find_all("a", href=lambda href: href and "/url?q=" in href)

# Create an empty list to store the titles and urls of the webpages
results = []
id1 = 1
# Loop through the first five links
for link in (links[:20]):

    # Get the url of the webpage by removing the prefix and suffix
    url = link["href"].replace("/url?q=", "").split("&")[0]
    print(url)
    # Get the title of the webpage by getting the text content of the link element
    title = link.text
    try:
        response = requests.get(url)
        if response.status_code == 200:

            # Converting valid url to pdf
            webpage_to_pdf(url)

            # Checking keyword frequency
            total_Occurance(f'{query}.pdf')


            # Append a dictionary with the title and url to the results list
            if count <= 2 * num_pages: quality = "Low"
            elif 2 * num_pages < count <= 4 * num_pages: quality = "Medium"
            elif count > 4 * num_pages: quality = "High"

            date = datetime.date.today()
            results.append({"_id":id1,"Date":str(date),"Keyword Searched":query,"Title": title, "Url": url, "Number of Pages":num_pages, "Quality": quality})
            id1 += 1
            # Open the webpage in a new tab using the webbrowser module
            # webbrowser.get('chrome').open_new_tab(url)
    except: continue
# Print the results list
# print(results)


Connect_MongoDB_and_Excel(results)
print("All task successfully completed.")
