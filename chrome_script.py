#  Import the required modules
import datetime, re, pdfkit
from multiprocessing.connection import wait
from time import sleep
import requests, webbrowser
import pandas as pd
from bs4 import BeautifulSoup
from pymongo import MongoClient
from googlesearch import search
from func_timeout import func_timeout, FunctionTimedOut

def get_google_search_results(query, num_results):
    search_results = []
    try:
        for result in search(query,sleep_interval = 5, num_results=num_results):
            search_results.append(result)
    except Exception as e:
        print(f"An error occurred: {e}")
    return search_results


# Connect to a MongoDB database using the pymongo module and 
def Connect_MongoDB_and_Excel(results):

    # Create a pandas dataframe from the results list
    df = pd.DataFrame(results)

    # Save the dataframe as an excel file using the pandas module
    df.to_excel(f"{query}.xlsx",index=False)

    print("Excel Sheet Created : Success")


    # client = MongoClient("mongodb://localhost:27017/")
    # db = client["google_search"]
    # collection = db["results"]

    # # Insert the results list as documents into the MongoDB collection
    # collection.insert_many(results)

    # print("MongoDB Database Updated : Success")



def webpage_to_pdf(url):

    #Define path to wkhtmltopdf.exe
    path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

    #Point pdfkit configuration to wkhtmltopdf.exe
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

    #Convert Webpage to PDF
    pdfkit.from_url(url, output_path=f'{query}.pdf', configuration=config)

    return 1

# Define the function that terminates the long function
def execute_long_function(url):
    # Set the timeout limit to 10 seconds
    timeout = 10
    # Try to call the long function with n and catch the exception if it times out
    try:
        result = func_timeout(timeout, webpage_to_pdf, args=(url,))
        return result
    except FunctionTimedOut:
        print(" -- Last Link terminated")
        return None

def total_Occurance(text):

    global count,num_pages
    from pypdf import PdfReader

    reader = PdfReader(f'{query}.pdf')
    num_pages = len(reader.pages)

    word = query

    # Finding and counting the word using a regular expression
    pattern = r"\b" + word + r"\b" # \b matches word boundaries
    matches = re.findall(pattern, text, re.IGNORECASE) # re.IGNORECASE ignores case sensitivity
    count = len(matches)
    return count

# Define the function
def get_text_between_dots(url):
    # Create a regular expression pattern to match text between dots
    pattern = r"\.(.*?)\."
    # Find all the matches in the URL
    matches = re.findall(pattern, url)
    # Return the matches as a list
    return str(matches[0]) if  len(matches)>0 else query

# Take the user input as the search query
query = input("Enter your search query: ")
print("Sit Back & Relax , Searching and Redirecting.....")


links = get_google_search_results(query,num_results=105)


# Create an empty list to store the titles and urls of the webpages
results = []
id1 = 1
exclude_list = ["www.youtube.com", "in.linkedin.com","twitter.com"]


# Loop through the first five links
for url in (links[:100]):

    # Get the title of the webpage by getting the text content of the link element
    title = get_text_between_dots(url)
    allowed = 1
    for i in exclude_list:
        if i in url:
            allowed = 0
            break
    if allowed == 1:
        print(url)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                
                num_pages = -1

                # Converting valid url to pdf
                execute_long_function(url)

                # Find and print the text from the webpage
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text()

                # Checking keyword frequency
                total_Occurance(text)

                # Append a dictionary with the title and url to the results list
                if count <= 2 * num_pages: quality = "Low"
                elif 2 * num_pages < count <= 4 * num_pages: quality = "Medium"
                elif count > 4 * num_pages: quality = "High"

                date = datetime.date.today()
                results.append({"_id":id1,"Date":str(date),"Keyword Searched":query,"Title": title, "Url": url, "Number of Pages":num_pages, "Occurance": total_Occurance(text), "Quality":quality})
                id1 += 1

                # Open the webpage in a new tab using the webbrowser module
                # webbrowser.get('chrome').open_new_tab(url)
        except: continue


Connect_MongoDB_and_Excel(results)
print("All task successfully completed.")
