import requests
from bs4 import BeautifulSoup
import os
import string

def sanitize_filename(title):
    """
    Sanitizes a string to be used as a filename by replacing whitespaces with
    underscores and removing punctuation.

    Args:
        title (str): The string to sanitize.

    Returns:
        str: The sanitized string.
    """
    whitespace_removed = title.replace(" ", "_")
    return whitespace_removed

def get_article_text(article_url):
    """
    Retrieves the text content of an article from a given URL.

    Args:
        article_url (str): The URL of the article.

    Returns:
        str: The text content of the article, or None on error.
    """
    try:
        response = requests.get(article_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find the paragraph containing the article teaser/body.
        article_body_tag = soup.find("p", {"class": "article__teaser"})
        if article_body_tag:
            return article_body_tag.text.strip()
        else:
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching article content: {e}")
        return None
    except Exception as e:
        print(f"Error parsing article HTML: {e}")
        return None

def scrape_nature_articles(num_pages, article_type):
    """
    Scrapes articles from Nature.com, filters by article type, and saves
    them to separate files in directories named Page_N.

    Args:
        num_pages (int): The number of pages to scrape.
        article_type (str): The type of articles to filter for (e.g., "News").
    """
    base_url = "https://www.nature.com/nature/articles"
    for page_num in range(1, num_pages + 1):
        page_url = f"{base_url}?sort=PubDate&year=2020&page={page_num}"
        print(f"Scraping page: {page_num} - URL: {page_url}")  # Added for debugging
        try:
            response = requests.get(page_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            articles = soup.find_all('article')
            # Create directory for the current page
            page_dir = f"Page_{page_num}"
            os.makedirs(page_dir, exist_ok=True)

            articles_found = False  # Flag to check if any articles were found

            for article in articles:
                # Find the article type.
                article_type_span = article.find('span', {'data-test': 'article.type'})
                if article_type_span and article_type_span.text.strip() == article_type:
                    # Find the link to the full article.
                    view_article_link = article.find('a', {'data-track-action': 'view article'})
                    if view_article_link:
                        article_url = "https://www.nature.com" + view_article_link['href']
                        article_text = get_article_text(article_url)
                        if article_text:
                            article_title_tag = article.find('h3')
                            if article_title_tag:
                                article_title = article_title_tag.text.strip()
                                sanitized_title = sanitize_filename(article_title)
                                filename = f"{sanitized_title}.txt"
                                filepath = os.path.join(page_dir, filename)  # Save in page directory
                                try:
                                    with open(filepath, "w", encoding="utf-8") as f:
                                        f.write(article_text)
                                    print(f"Saved article: {article_title} to {filepath}")
                                    articles_found = True  # Set flag to True if article found and saved
                                except Exception as e:
                                    print(f"Error saving article: {e}")
                            else:
                                print(f"Couldn't find title for article. Skipping")
                        else:
                            print(f"Failed to retrieve article text for {article_url}")
            if not articles_found:
                print(f"No articles of type '{article_type}' found on Page {page_num}.")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    num_pages = int(input("Enter the number of pages to scrape: "))
    article_type = input("Enter the type of articles to filter (e.g., News): ")
    scrape_nature_articles(num_pages, article_type)
    print("Scraping complete.") # added completion message
