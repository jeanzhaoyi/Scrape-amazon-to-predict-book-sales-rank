# Capstone_1

Data collection:
"fun_ParseReviews.py" has two functions-- downloading an html file for a given url, and scraping a book given its book review url

"scrape_biographies.py" is an example of book list based scraping scripts that calls the "fun_ParseReviews.py" file.
The output is saved as a json file in a directory.

"process_parsed_reviews.ipynb" loads in all the json files in a directory, format them as a data frame, and expands list elements of reviews by book into a spreadsheet of columns of words with their number of occurences as values.

"scrape_meta_data.ipynb" scrapes the book title, number of reviews and review url as well as ASIN of each book list site.
The resulting data frame is stored as "complete_meta.csv"
