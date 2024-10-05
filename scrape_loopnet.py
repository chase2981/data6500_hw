import requests
from bs4 import BeautifulSoup
import csv

# Function to scrape LoopNet
def scrape_loopnet(url, headers):
    # Send a GET request to the URL
    response = requests.get(url, headers=headers)

    # Check if request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve content from {url}")
        return

    # Parse the page content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the section containing the listings
    listings = soup.find_all("div", class_="placardContent")

    # Create a list to store property data
    properties = []

    for listing in listings:
        # Extract the property title (name)
        title = listing.find("h4", class_="property-title").get_text(strip=True) if listing.find("h4", class_="property-title") else None

        # Extract price, location, and other information
        price = listing.find("div", class_="property-price").get_text(strip=True) if listing.find("div", class_="property-price") else None
        location = listing.find("div", class_="property-address").get_text(strip=True) if listing.find("div", class_="property-address") else None
        sqft = listing.find("div", class_="property-sqft").get_text(strip=True) if listing.find("div", class_="property-sqft") else None

        # Store the data in a dictionary
        property_data = {
            "title": title,
            "price": price,
            "location": location,
            "sqft": sqft
        }

        # Append the property data to the list
        properties.append(property_data)

    # Return the list of properties
    return properties

# Function to write data to CSV
def save_to_csv(properties, filename="loopnet_properties.csv"):
    # Define the CSV header
    keys = properties[0].keys()

    # Write data to a CSV file
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(properties)

    print(f"Data saved to {filename}")

# Main execution
if __name__ == "__main__":
    # URL of the LoopNet page to scrape (you'll need to update this based on the specific search you're interested in)
    url = "https://www.loopnet.com/commercial-real-estate/logan-ut/for-lease/"

    # Define headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # Scrape the LoopNet page
    properties = scrape_loopnet(url, headers)

    # Save the data to a CSV file if we have scraped properties
    if properties:
        save_to_csv(properties)
    else:
        print("No properties found.")

