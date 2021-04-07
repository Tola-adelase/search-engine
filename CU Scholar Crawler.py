import requests
from bs4 import BeautifulSoup


def mycrawler(seed, maxcount):
    Q = [seed]  # this is the queue which initially contains the given seed URL
    count = 0
    while Q != [] and count < maxcount:
        count += 1
        url = Q[0]
        Q = Q[1:]
        print(":" + url)

        code = requests.get(url)
        plain = code.text
        s = BeautifulSoup(plain, "html.parser")
        for link in s.findAll('a', {'class': 'gs_ai_pho'}):
            new_url = link.get('href')
            if new_url is not None and new_url != '/':
                new_url = new_url.strip()
                # print("new_url is : ", new_url)

                # normalise if needed
                if new_url[0:7] != 'http://' and new_url[0:8] != 'https://':
                    if url[len(url) - 1] == '/':
                        new_url = url + new_url
                    else:
                        new_url = url + '/' + new_url
                        # NOTE : further normalization code required here
                # print("new_url is : ", new_url)  #uncomment the print statement to see the urls

                Q.append(new_url)


# use any number, instead of 10, to control the number of pages crawled
mycrawler('https://scholar.google.co.uk/citations?view_op=view_org&hl=en&org=9117984065169182779', 20)
