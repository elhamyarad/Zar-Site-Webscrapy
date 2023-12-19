import random
import time

import requests
from bs4 import BeautifulSoup
import pandas as pd

# We find how many pages are in this page
n = ''
firstPage = "https://zar.ir/shop/cat-34-1.html"
site1 = requests.get(firstPage)
soup1 = BeautifulSoup(site1.text, 'html.parser')

# In the last page we can find number of pages
pages = soup1.find_all('li', {'class': 'last'})

for i in str(pages[0]):
    if i.isnumeric():
        n += str(i)

# Titles of ProductLists
Prices = []
ProductName = []
Models = []

# Titles of ProductSpec
WeightPure = []
WeightBrilliant = []
KindBrilliant = []
ColourDegree = []
Guaranty = []
StandardCode = []

# Scrap pages
try:
    for page in range(1, int(n[2:]) + 1):
        siteUrl = "https://zar.ir/shop/cat-34-" + str(page) + ".html"
        site = requests.get(siteUrl)
        soup = BeautifulSoup(site.text, 'html.parser')
        div1 = soup.find('div', {'class': 'grid-container'})
        div2 = div1.find_all('div', {'class': 'Box'})

        # Scraping every item in per page
        for item in range(len(div2)):

            # Scraping price of items
            price = div2[item].find_all('div', {'lblprice'})[0].text
            Prices.append(int(price.replace('\n', '').replace(',', '').replace('تومان', '')))

            # Scraping title of each product
            titleMain = div2[item].find_all('a', {'pcitem-title'})[0].text
            title = titleMain.split(':')
            ProductName.append(title[0].replace('\n', '').replace(',', '').replace('مدل', ''))
            Models.append(title[1].replace('\n', '').replace(',', '').replace(' ', ''))

            # Scraping photos
            photo = div2[item].find_all('img', {'lozad'})[0]
            photoUrl = photo['data-src']
            photoUrl = 'https://zar.ir/' + photoUrl

            # We go inside link of each item and scraping details of each item
            sitePhotoRequest = requests.get(photoUrl)
            photoResult = sitePhotoRequest.content

            with open("/app/" + title[1].replace('\n', '').replace(',', '').replace(' ', '') + '.jpg',
                      mode='wb') as photos:
                photos.write(photoResult)

            detail = div2[item].find_all('a', {'pcitem-pic'})[0]
            detailUrl = 'https://zar.ir' + detail['href']
            siteDetail = requests.get(detailUrl)
            soupDetail = BeautifulSoup(siteDetail.text, 'html.parser')
            divDetail = soupDetail.find_all('div', {'id': 'product-summary-props'})

            weightpure = divDetail[0].find_all('span', {'class': 'goldW'})[0].text
            WeightPure.append(weightpure.replace('\n', ''))

            weightbrilliant = divDetail[0].find_all('span', {'class': 'berlianW'})[0].text
            WeightBrilliant.append(weightbrilliant.replace('\n', ''))

            kindbrilliant = divDetail[0].find_all('span')[5].text
            KindBrilliant.append(kindbrilliant.replace('\n', ''))

            colordegree = divDetail[0].find_all('span')[7].text
            ColourDegree.append(colordegree.replace('\n', ''))

            guaranty = divDetail[0].find_all('span')[15].text
            Guaranty.append(guaranty.replace('\n', ''))

            standardcode = divDetail[0].find_all('span')[17].text
            StandardCode.append(standardcode.replace('\n', ''))

        time.sleep(random.randint(3, 7))

    # Made a dictionary of titles of ProductList
    zarDictionary = {
        'ProductName': ProductName,
        'Model': Models,
        'Price': Prices
    }

    # Made a dataframe with pandas library for list of products
    df = pd.DataFrame(zarDictionary)

    # Made a comma-separated values file
    df.to_csv('/app/ProductList.csv')

    # You can see your result in console
    zarSetDataList = pd.read_csv('/app/ProductList.csv')
    # print(zarSetDataList.to_string())

    # Made a dictionary of titles of Product details
    detailDictionary = {
        'Model': Models,
        'WeightPure': WeightPure,
        'WeightBrilliant': WeightBrilliant,
        'KindBrilliant': KindBrilliant,
        'ColourDegree': ColourDegree,
        'Guaranty': Guaranty,
        'StandardCode': StandardCode
    }

    # Made a dataframe with pandas library for details of product
    df2 = pd.DataFrame(detailDictionary)

    # Made a comma-separated values file for details
    df2.to_csv('/app/ProductSpec.csv')

    zarSetDetailDataList = pd.read_csv('/app/ProductSpec.csv')
    # print(zarSetDetailDataList.to_string())

except:
    print("Can not run")
