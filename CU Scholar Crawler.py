import requests
from bs4 import BeautifulSoup
import webbrowser
#webbrowser.open(url)


def mycrawler(seed, maxcount):
    Q = [seed]  # this is the queue which initially contains the given seed URL
    count = 0
    while Q != [] and count < maxcount:
        count += 1
        url = Q[0]
        Q = Q[1:]
        print(":" + url)

        # def fetch(url):
        # try:
        code = requests.get(url)
    # except requests.exceptions.ConnectionError:
    # print('Given URL: "%s" is not available!' % url)
    # return

    plain = code.text
    s = BeautifulSoup(plain, "html.parser")
    for link in s.findAll('a', {'class': 'gs_ai_pho'}):
        new_url = link.get('href')
        if new_url is not None and new_url != '/':
            new_url = new_url.strip()
            # print("new_url is : ", new_url)

            # normalise if needed
            if new_url[0:7] != 'https://' and new_url[0:8] != 'https://':
                if url[len(url):0] == '/':
                    new_url = 'https:' + url.strip(
                        '/citations?view_op=view_org&hl=en&org=9117984065169182779') + new_url
                else:
                    new_url = 'https' + url.strip(
                        '/citations?view_op=view_org&hl=en&org=9117984065169182779') + new_url

                    print("new_url is : ", new_url)  # uncomment the print statement to see the urls
                    Q.append(new_url)


# use any number, instead of 10, to control the number of pages crawled
mycrawler('https://scholar.google.co.uk/citations?view_op=view_org&hl=en&org=9117984065169182779', 15)

# fetch(mycrawler)
