import logging
import json

import requests
from bs4 import BeautifulSoup
from logger import logger



class TorrentScraper:
    def __init__(self, url, css_selector):
        self.url = url
        self.css_selector = css_selector

    def scrape_data(self):
        # Send a GET request to the URL
        response = requests.get(self.url)

        # Log the status code of the request
        logger.info(
            f'Request to {self.url} - Status code: {response.status_code}')

        # Create a BeautifulSoup object from the response content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table body using the CSS selector
        table_body = soup.select_one(self.css_selector)

        # Verify if table body is found
        if table_body is not None:
            # Find all the <tr> elements within the table body
            tr_elements = table_body.find_all('tr')

            # Create a list to store the extracted data
            data = []

            # Iterate over each <tr> element
            for tr in tr_elements:
                # Find the <td> element with class "coll-1 name" within the <tr> element
                coll_1_td = tr.find('td', class_='coll-1 name')

                if coll_1_td is not None:
                    # Find all the <a> tags within the <td> element
                    a_tags = coll_1_td.find_all('a')

                    # Check if there are at least two <a> tags
                    if len(a_tags) >= 2:
                        # Extract the values and href attributes from the second <a> tag
                        tName = a_tags[1].get_text(strip=True)
                        tLink = a_tags[1]['href']

                        # Find the other <td> elements within the <tr> element
                        coll_2_td = tr.find('td', class_='coll-2 seeds')
                        coll_3_td = tr.find('td', class_='coll-3 leeches')
                        coll_4_td = tr.find('td', class_='coll-4 size mob-')
                        coll_5_td = tr.find('td', class_='coll-5 uploader')

                        if coll_4_td is not None:
                            for span_tag in coll_4_td.find_all('span'):
                                span_tag.extract()

                        # Extract the values from the remaining <td> elements
                        tSize = coll_4_td.get_text(
                            strip=True) if coll_4_td is not None else ''
                        tSeeds = coll_2_td.get_text(
                            strip=True) if coll_2_td is not None else ''
                        tLeeches = coll_3_td.get_text(
                            strip=True) if coll_3_td is not None else ''
                        tDate = coll_5_td.get_text(
                            strip=True) if coll_5_td is not None else ''

                        # Append the extracted data as a tuple to the list
                        data.append(
                            (tName, tLink, tSize, tSeeds, tLeeches, tDate))

            return data
        else:
            logger.warning(
                f'No table body found using CSS selector: {self.css_selector}')
            return []
