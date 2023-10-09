# Relevent_Search_Python_Script
The script can be useful for finding information that matches certain criteria or keywords, without having to manually browse through the search results. 


I have successfully created a python script that can show the most relevant data from the Google search containing specified words in it which the user has inputted. The script can take a user query or a list of words as inputs. The script can then filter the results based on the presence of the specified words in the title or snippet of the result. The script can also display them in new tab.

The script can be useful for finding information that matches certain criteria or keywords, without having to manually browse through the search results. For example, if the user wants to find articles about "python" that also contain the words "web scraping" or "data analysis", they can use the script to get the most relevant results that satisfy these conditions.

The script is written in Python 3 and uses the requests and webbrowsers libraries. 

My WorkFlow was :
 - Installed and Imported the required libraries: requests and webbrowser.
 - Define a function that takes a search query as input.
 - Use requests to send an HTTP request to Bing search engine with the query as a parameter.
 - Extract the URLs of the top search results from the parsed HTML content.
 - Filter out any sponsored content URLs and invalid URLs.
 - Open each URL in a new tab of your default browser using webbrowser.
