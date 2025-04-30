import requests
from bs4 import BeautifulSoup


def sanitize_filename(title):
    whitespace_removed = title.replace(" ", "_")
    return whitespace_removed


def get_article_text(article_url):
    try:
        response = requests.get(article_url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')
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


def scrape_nature_articles(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        articles = soup.find_all('article')

        for article in articles:
            article_type_span = article.find('span', {'data-test': 'article.type'})
            if article_type_span and article_type_span.text.strip() == "News":
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
                            try:
                                with open(filename, "w", encoding="utf-8") as f:
                                    f.write(article_text)
                                print(f"Saved article: {article_title} to {filename}")
                            except Exception as e:
                                print(f"Error saving article: {e}")
                        else:
                            print(f"Couldn't find title for article. Skipping")
                    else:
                        print(f"Failed to retrieve article text for {article_url}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    site_url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3"
    scrape_nature_articles(site_url)
