import json
from models import Author, Quote

def load_authors(authors_file):
    try:
        with open(authors_file, 'r', encoding='utf-8') as file:
            authors = json.load(file)
            for author_data in authors:
                if Author.objects(fullname=author_data['fullname']).first():
                    print(f"Author {author_data['fullname']} already exists. Skipping.")
                else:
                    author = Author(**author_data)
                    author.save()
                    print(f"Author {author.fullname} has been added.")
    except Exception as e:
        print(f"An error occurred while loading authors: {e}")

def load_quotes(quotes_file):
    try:
        with open(quotes_file, 'r', encoding='utf-8') as file:
            quotes = json.load(file)
            for quote_data in quotes:
                author_name = quote_data.pop('author')
                author = Author.objects(fullname=author_name).first()
                if author:
                    if Quote.objects(quote=quote_data['quote'], author=author).first():
                        print(f"Quote by {author.fullname} already exists. Skipping.")
                    else:
                        quote_data['author'] = author
                        quote = Quote(**quote_data)
                        quote.save()
                        print(f"Quote by {author.fullname} has been added.")
                else:
                    print(f"Author {author_name} not found for quote: {quote_data['quote']}. Skipping.")
    except Exception as e:
        print(f"An error occurred while loading quotes: {e}")

if __name__ == "__main__":
    load_authors('authors.json')
    load_quotes('qoutes.json')

