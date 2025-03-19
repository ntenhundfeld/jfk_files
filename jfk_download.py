import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from urllib.parse import urljoin

def download_pdfs():
    # Base URL
    base_url = "https://www.archives.gov/research/jfk/release-2025"
    
    # Create a directory for downloads if it doesn't exist
    download_dir = "jfk_pdfs"
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    # Get the webpage content
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table (assuming it's the first table on the page)
    table = soup.find('table')
    if not table:
        print("No table found on the page")
        return
    
    # Extract all rows from the table
    rows = table.find_all('tr')
    
    # Skip the header row and process each data row
    for row in rows[1:]:
        try:
            # Get all columns in the row
            columns = row.find_all('td')
            if len(columns) > 0:
                # First column should contain the Record Number
                record_number = columns[0].text.strip()
                
                # Find any link in the row (usually in the last column)
                link = row.find('a', href=True)
                if link and link['href'].endswith('.pdf'):
                    pdf_url = urljoin(base_url, link['href'])
                    
                    # Download the PDF
                    pdf_response = requests.get(pdf_url)
                    
                    # Create a safe filename using the record number
                    filename = f"{record_number.replace('/', '_')}.pdf"
                    filepath = os.path.join(download_dir, filename)
                    
                    # Save the PDF
                    with open(filepath, 'wb') as f:
                        f.write(pdf_response.content)
                    
                    print(f"Downloaded: {filename}")
                
        except Exception as e:
            print(f"Error processing row: {str(e)}")
            continue

if __name__ == "__main__":
    print("Starting PDF download process...")
    download_pdfs()
    print("Download process completed!")
