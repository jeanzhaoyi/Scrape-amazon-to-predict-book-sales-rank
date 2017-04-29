# Amazon Sales Ranking Prediction

Data collection:
"fun_ParseReviews.py" has two functions-- downloading an html file for a given url, and scraping a book given its book review url

"scrape_biographies.py" is an example of book list based scraping scripts that calls the "fun_ParseReviews.py" file.
The output is saved as a json file in a directory.

"scrape_meta_data.ipynb" scrapes the book title, number of reviews and review url as well as ASIN of each book list site.
The resulting data frame is stored as "complete_meta.csv"

"CountVectorizer_process_parsed_reviews.ipynb" loads in all the json files in a directory, format them as a data frame, and expands list elements of reviews by book into a spreadsheet of columns of words with their number of occurences as values. It also does EDA on the dataset.

"cross-validated_ML_book_sales_rank.ipynb" loads in the pre-processed data from the notebook above and applies cross validated machine learning algorithms to predict book sales. Analyses also include LDA topics analysis, in addition to a simple word count.
