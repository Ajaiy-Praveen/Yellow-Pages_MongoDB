
# Web Scraping and Data Extraction with Python

This project showcases web scraping and data extraction using Python and Selenium. The project includes two parts: Bored Ape Yacht Club NFT collection and Yellow Pages data extraction.

Bored Ape Yacht Club

Bored Ape Yacht Club is a popular non-fungible token (NFT) collection built on the Ethereum blockchain. In this project, we used Selenium to access the Bored Ape Yacht Club website and select all apes with "Solid gold" fur, then sorted them by price from high to low. We then clicked on each of the top-8 most expensive Bored Apes and saved the resulting details page to disk.

Yellow Pages

We also extracted data from Yellow Pages, a popular online directory of businesses. We searched for the top 30 Pizzerias in San Francisco and saved the search result page to disk. We then parsed out all shop information, such as search rank, name, linked URL, star rating, number of reviews, TripAdvisor rating, number of TA reviews, "$" signs, years in business, review, and amenities. We skipped all "Ad" results.

We then created a MongoDB collection called "sf_pizzerias" that stored all the extracted shop information, one document for each shop. We also parsed each shop's address, phone number, and website from their respective pages and updated the MongoDB collection with the shop's geolocation.

Conclusion

This project demonstrates how web scraping and data extraction can be used to gather valuable data from websites. By using tools such as Selenium and BeautifulSoup, we were able to access and extract data from multiple web pages and store them in a MongoDB collection. These techniques can be applied to many other websites and can help businesses and researchers to gain valuable insights from online data.
