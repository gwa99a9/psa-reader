import http.server
import sqlite3
import json
from urllib.parse import urlparse, parse_qs
import logging
from logger import logger

# Create a custom handler for the HTTP requests


class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Set the response status code
            self.send_response(200)

            # Set the response headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Read the contents of the HTML file
            with open('index.html', 'r') as file:
                html_content = file.read()

            # Send the HTML response
            self.wfile.write(html_content.encode())

            logger.info('HTML response sent successfully.')

        elif self.path.startswith('/search='):
            # Set the response status code
            self.send_response(200)

            # Set the response headers
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            # Get the search query parameter from the URL
            search_query = self.path.split('=')[1]
            logger.info(f'Search query: {search_query}')

            # Establish a connection to the SQLite database
            conn = sqlite3.connect('torrents.db')
            cursor = conn.cursor()

            try:
                if search_query:
                    # Execute the search query
                    cursor.execute('SELECT * FROM torrents WHERE name LIKE ?', ('%' + search_query + '%',))
                else:
                    # Select all records
                    cursor.execute('SELECT * FROM torrents')

                results = cursor.fetchall()

                # Convert the results to JSON format
                json_results = json.dumps(results)

                # Send the JSON response
                self.wfile.write(json_results.encode())

                logger.info('Search results sent successfully.')

            except Exception as e:
                logger.error(f'An error occurred during the search: {str(e)}')

            finally:
                # Close the database connection
                conn.close()


        elif self.path == '/favicon.ico':
            # Set the response status code
            self.send_response(200)

            # Set the response headers
            self.send_header('Content-type', 'image/x-icon')
            self.end_headers()

            # Send an empty response for the favicon
            logger.info('Favicon request handled.')

        else:
            # Set the response status code for unknown routes
            self.send_response(404)
            logger.info('Unknown route.')

    def log_message(self, format, *args):
        # Override the log_message method to use the logger instead of printing to console
        logger.info("%s - - [%s] %s" %
                    (self.client_address[0], self.log_date_time_string(), format % args))


# Create the HTTP server with the custom request handler
server = http.server.HTTPServer(('localhost', 8000), RequestHandler)
logger.info('Server running on http://localhost:8000')

# Start the server
try:
    server.serve_forever()
except KeyboardInterrupt:
    pass

server.server_close()
logger.info('Server stopped.')
