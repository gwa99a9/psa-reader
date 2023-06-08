import concurrent.futures

from database import Database
from torrent_data import TorrentData
from torrent_scraper import TorrentScraper
from logger import logger

# Log application start
logger.info('Application started.')

css_selector = 'body main div div div:nth-of-type(2) div:nth-of-type(1) table tbody'

# Define the function to scrape and insert data for a single page
def process_page(page_num):
    # Establish a connection to the database file
    db = Database('torrents.db')

    try:
        # Construct the URL for the page
        url = f'https://1337x.to/BedBug-torrents/{page_num}/'
        logger.info(f'Extracting data from {url}...')

        # Create a TorrentScraper object
        scraper = TorrentScraper(url, css_selector)

        # Scrape the data
        scraped_data = scraper.scrape_data()

        # Insert each torrent into the database
        for torrent_data in scraped_data:
            torrent = TorrentData(*torrent_data)
            db.insert_torrent(torrent)

        # Commit the changes to the database
        db.commit_changes()
        logger.info('Changes committed to the database.')

    finally:
        # Close the database connection
        db.close_connection()
        logger.info('Database connection closed.')

# Create a thread pool with a maximum of 4 threads
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    try:
        # Submit tasks to the thread pool for each page
        futures = [executor.submit(process_page, page_num) for page_num in range(1, 101)]

        # Wait for all tasks to complete
        concurrent.futures.wait(futures)

    except Exception as e:
        logger.error(f'An error occurred: {str(e)}')

# Log application end
logger.info('Application ended.')
