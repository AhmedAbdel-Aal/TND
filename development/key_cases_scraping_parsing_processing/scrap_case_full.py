from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class LegalCaseScraperFULL:
    def __init__(self, headless=True):
        """Initialize the scraper with Selenium WebDriver options."""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 5)

    def extract_case_from_elements(self, elements):
        """Extract the facts section from the web page elements."""
        # Skip table of contents
        case_text = []
        for idx, elem in enumerate(elements):
            line = elem.text.strip()
            if not line:
                continue
            else:
                case_text.append(line)
        return case_text

    def scrape_metadata(self):
        meta_data = []
        tabs = self.wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".nav-tabs li"))
        )
        tabs[1].click()
        time.sleep(2)
        elements = self.driver.find_elements(By.CSS_SELECTOR, ".noticefield")
        for idx, elem in enumerate(elements):
            line = elem.text.strip()
            if not line:
                continue
            else:
                meta_data.append(line)
                # print(f"{idx}: {line}")
        return meta_data

    def scrape_case(self, url):
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
            case_text = self.extract_case_from_elements(elements)
            case_metadata = self.scrape_metadata()

            case = {"metadata": case_metadata, "text": case_text}

            return case

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
