from models import Author, Quote
import connect
import re

redis_client = connect.redis_client

def cache_result(key, result):
    try:
        redis_client.set(key, result)
    except Exception as e:
        print(f"Failed to cache result: {e}")

def get_cached_result(key):
    try:
        return redis_client.get(key)
    except Exception as e:
        print(f"Failed to get cached result: {e}")
        return None

def search_quotes():
    while True:
        command = input("Enter command: ").strip()
        if command.lower() == 'exit':
            break

        if ':' not in command:
            print("Invalid command format. Please use 'command: value'")
            continue
        
        command_type, value = command.split(':', 1)
        value = value.strip()

        cache_key = f"{command_type}:{value}"
        cached_result = get_cached_result(cache_key)
        if cached_result:
            print(cached_result)
            continue

        result = ""
        if command_type == 'name':
            regex = re.compile(f".*{re.escape(value)}.*", re.IGNORECASE)
            authors = Author.objects(fullname=regex)
            if authors:
                for author in authors:
                    quotes = Quote.objects(author=author)
                    for quote in quotes:
                        result += quote.quote + "\n"
            if not result:
                result = f"No quotes found for author containing: {value}"
        elif command_type == 'tag':
            regex = re.compile(f".*{re.escape(value)}.*", re.IGNORECASE)
            quotes = Quote.objects(tags=regex)
            for quote in quotes:
                result += quote.quote + "\n"
            if not result:
                result = f"No quotes found for tag containing: {value}"
        elif command_type == 'tags':
            tags = value.split(',')
            regexes = [re.compile(f".*{re.escape(tag)}.*", re.IGNORECASE) for tag in tags]
            quotes = Quote.objects(tags__in=regexes)
            for quote in quotes:
                result += quote.quote + "\n"
            if not result:
                result = f"No quotes found for tags: {', '.join(tags)}"
        else:
            result = "Invalid command. Try again."
        
        cache_result(cache_key, result.strip())
        print(result.strip())

if __name__ == "__main__":
    search_quotes()
