from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


class LegalCaseScraper:
    def __init__(self, headless=True):
        """Initialize the scraper with Selenium WebDriver options."""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=chrome_options)

    def extract_facts_from_elements(self, elements):
        """Extract the facts section from the web page elements."""
        # Skip table of contents
        start_after_index = 0
        toc_found = False
        for idx, elem in enumerate(elements):
            line = elem.text.strip()
            # print(f"Line: {line}")
            if not line:
                continue
            if line.startswith("TABLE OF CONTENTS") or line.startswith(
                "Table of Contents"
            ):
                print(f"Found TABLE OF CONTENTS at index: {idx}")
                toc_found = True

            if ("CONCLUSION" in line) or ("Conclusion" in line) or ("THE LAW" in line):
                print(f"Found CONCLUSION at index: {idx}")
                start_after_index = idx + 1
                break

        if not toc_found:
            print("TABLE OF CONTENTS not found")
            start_after_index = 0
        print(f"toc_found: {toc_found}")
        print(f"Starting after index: {start_after_index}")

        # Extract facts
        facts = []
        in_facts_section = False
        print(f"Total elements: {len(elements)}")

        for elem in elements[start_after_index:]:
            line = elem.text.strip()
            if not line:
                continue
            # print(f"--Line: {line}")
            if line.startswith("THE FACTS"):
                in_facts_section = True
                facts.append(line)
            elif line.startswith("THE LAW") or line.startswith(
                "RELEVANT LEGAL FRAMEWORK AND PRACTICE"
            ):
                in_facts_section = False
                break
            elif in_facts_section:
                facts.append(line)

        facts_string = "\n".join(facts)
        print(f"Facts: {len(facts_string)}")
        return facts_string

    def scrape_facts(self, url):
        """Main method to scrape facts from a given case URL."""
        try:
            # Load the page
            self.driver.get(url)
            time.sleep(5)

            # Get all elements that might contain text
            elements = self.driver.find_elements(
                By.CSS_SELECTOR, "p, h1, h2, h3, h4, h5, h6"
            )

            # Extract and format facts
            facts_text = self.extract_facts_from_elements(elements)

            return facts_text

        except Exception as e:
            print(f"Error: {str(e)}")
            return None

    def close(self):
        """Close the WebDriver."""
        self.driver.quit()


# Usage example
# if __name__ == "__main__":
#    url = "https://hudoc.echr.coe.int/eng?i=001-233261"
#    scraper = LegalCaseScraper()
#    try:
#        facts = scraper.scrape_facts(url)
#        print("=" * 80)
#        print(facts)
#        print("=" * 80)
#    finally:
#        scraper.close()
