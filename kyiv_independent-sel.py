import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the Selenium WebDriver
driver = webdriver.Chrome()

# Open the website
url = "https://kyivindependent.com/"
driver.get(url)

# Wait for the page to load (adjust the timeout as needed)
wait = WebDriverWait(driver, 10)
# wait.until(EC.presence_of_element_located((By.CLASS_NAME, "article-container")))

# Scroll down to load more posts if necessary
# You can customize the number of scrolls based on your requirements
# for _ in range(5):
#    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
#    time.sleep(2)  # Give the page time to load

# Extract links to individual posts
post_links = set()
elements = driver.find_elements(By.CSS_SELECTOR, "a")
for element in elements:
    print('Size of elements is: ' + str(elements))
    href = element.get_attribute("href")
    if href and re.search(r"https://kyivindependent\.com/*/$", href):
        print(href)
        post_links.add(href)

# Create a file to store the found links
output_file = "found_links.txt"

# Open each post, download its HTML, and find links in the text
with open(output_file, 'w') as file:
    for post_link in post_links:
        driver.get(post_link)
        time.sleep(2)  # Allow time for the post to load

        # Extract the HTML content of the post
        post_html = driver.page_source

        # Find links within the post's text using regular expressions
        links_in_text = re.findall(r'href=["\'](https?://[^\s"\']+)["\']', post_html)

        # Write the found links to the output file
        file.write(f"Links in {post_link}:\n")
        for link in links_in_text:
            file.write(f"{link}\n")
        file.write("\n")

# Close the WebDriver
driver.quit()
