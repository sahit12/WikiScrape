import requests
from bs4 import BeautifulSoup as bs
from gensim.summarization.summarizer import summarize

def crawl(url):
    # call the first page to crawl and then proceed as getting links
    # crawling entire page one by one

    try:
        r = requests.get(url).content
    except Exception as e:
        print(e)
        exit()
    
    # create a BeautifulSoup object

    soup = bs(r, 'html.parser')
    cp_links = soup.select("div.mw-allpages-body ul.mw-allpages-chunk li a")

    for i,text in enumerate(cp_links):
        try:
            wiki_link_url = "https://en.wikipedia.org/{}".format(text['href'])

            print("Call : " + str(i) + " : " + wiki_link_url)

            # call the current page

            r = requests.get(wiki_link_url).content
            soup = bs(r, 'html.parser')
            
            # get the main headlines of the page

            headlines_tag = soup.find_all('span', class_='mw-headline')
            headlines = [x.get_text() for x in headlines_tag]

            # get the content(text) of the body

            body_text = [x.get_text() for x in soup.find_all('p')]
            summarized = "".join(body_text)
            return summarize(summarized)

            # get references, their links and the reference text

            ref_tag = soup.select('ul li cite')
            ref_links = [x.find('a')['href'] for x in ref_tag]
            ref_text = [x.get_text for x in ref_tag]

        except Exception as e:
            pass

"""def main():
    crawl('https://en.wikipedia.org/w/index.php?title=Special:AllPages&hideredirects=1')

main()"""