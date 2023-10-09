# Import the required modules
from time import sleep
import webbrowser
import requests
import re

# Define the Edge browser path
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
webbrowser.register('edge', None, webbrowser.BackgroundBrowser(edge_path))

# Ask the user for the search query
query = input("Enter your Google search query: ")
print("Sit Back & Relax , Searching and Redirecting.....")
sleep(2)

# Construct the Google search URL
google_url = "https://www.google.com/search?q=" + query

# Get the HTML response from the URL
response = requests.get(google_url)

# Check if the response is successful
if response.status_code == 200:
    # Extract the links from the HTML using regular expressions
    links = re.findall(r'<a href="/url\?q=(.*?)&', response.text)
    
    # Filter out the links that are not valid URLs
    valid_links = []
    for link in links:
        if link.startswith("http"):
            valid_links.append(link)
    
    # Open the top 5 valid links in new tabs in Edge browser
    for i in range(5):
        webbrowser.get('edge').open_new_tab(valid_links[i])

    sleep(5)
    print("Successful")
else:
    # Print an error message if the response is not successful
    print("Something went wrong. Please try again later.")

