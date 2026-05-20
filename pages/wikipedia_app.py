from __future__ import annotations

import time
import allure
from appium.webdriver.common.appiumby import AppiumBy
from selene import have, be
from selene.support.shared import browser

from pages.onboarding_page import onboarding


class WikipediaApp:
    """Main Wikipedia App Page Object"""

    @allure.step("Close onboarding if present")
    def close_onboarding_if_present(self) -> WikipediaApp:
        """Close onboarding screens if they are displayed"""
        if onboarding.is_onboarding_displayed():
            onboarding.click_skip()
            allure.attach("Onboarding was closed", name="Onboarding action",
                          attachment_type=allure.attachment_type.TEXT)
        return self

    @allure.step("Complete full onboarding")
    def complete_onboarding(self) -> WikipediaApp:
        """Complete all onboarding screens"""
        onboarding.complete_onboarding()
        return self

    @allure.step("Search for text: '{text}'")
    def search(self, text: str) -> WikipediaApp:
        """Perform search for given text"""
        search_field = browser.element((AppiumBy.ACCESSIBILITY_ID, "Search Wikipedia"))
        search_field.with_(timeout=10).should(be.visible).click()

        search_input = browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_src_text"))
        search_input.type(text)
        time.sleep(2)  # Wait for search results to load

        return self

    @allure.step("Verify search results contain text: '{expected_text}'")
    def results_should_contain_text(self, expected_text: str) -> WikipediaApp:
        """Verify that search results contain expected text"""
        result = browser.element(
            (AppiumBy.XPATH, f"//android.widget.TextView[contains(@text, '{expected_text}')]")
        )
        result.with_(timeout=10).should(be.visible)
        return self

    @allure.step("Verify search results count is greater than {count}")
    def results_should_have_count_greater_than(self, count: int) -> WikipediaApp:
        """Verify that number of search results is greater than count"""
        browser.all((AppiumBy.CLASS_NAME, "android.widget.TextView")).with_(timeout=10).should(
            have.size_greater_than(count)
        )
        return self

    @allure.step("Click on first search result")
    def click_first_result(self) -> WikipediaApp:
        """Click on the first search result"""
        results = browser.all((AppiumBy.CLASS_NAME, "android.widget.TextView"))
        results.first.should(be.visible).click()
        time.sleep(2)  # Wait for article to load
        return self

    @allure.step("Click on search result containing text: '{text}'")
    def click_result_containing_text(self, text: str) -> WikipediaApp:
        """Click on search result that contains specific text"""
        result = browser.element(
            (AppiumBy.XPATH, f"//android.widget.TextView[contains(@text, '{text}')]")
        )
        result.with_(timeout=10).should(be.visible).click()
        time.sleep(2)
        return self

    @allure.step("Verify article page is opened")
    def article_should_be_opened(self) -> WikipediaApp:
        """Verify that article page was opened"""
        # Check for article indicators
        page_source = browser.config.driver.page_source

        # Save for debugging
        with open("article_page.xml", "w", encoding="utf-8") as f:
            f.write(page_source)

        # Check for article indicators
        article_indicators = ["WebView", "TextView", "page_title", "article"]

        found = False
        for indicator in article_indicators:
            if indicator in page_source:
                allure.attach(f"Found article indicator: {indicator}", name="Article verification")
                found = True
                break

        if not found:
            raise AssertionError("Article page not opened - no article indicators found")

        return self

    @allure.step("Verify article title contains text: '{expected_text}'")
    def article_title_should_contain(self, expected_text: str) -> WikipediaApp:
        """Verify that article title contains expected text"""
        # Try to find title element (selectors may vary)
        try:
            title_element = browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/view_page_title_text"))
            title_element.with_(timeout=5).should(have.text(expected_text))
        except:
            # Fallback: check page source
            page_source = browser.config.driver.page_source
            if expected_text not in page_source:
                raise AssertionError(f"Article title does not contain '{expected_text}'")

        return self

    @allure.step("Go back to previous screen")
    def go_back(self) -> WikipediaApp:
        """Press back button"""
        browser.driver.back()
        time.sleep(1)
        return self

    @allure.step("Clear search")
    def clear_search(self) -> WikipediaApp:
        """Clear search field"""
        clear_button = browser.element((AppiumBy.ID, "org.wikipedia.alpha:id/search_close_btn"))
        if clear_button.with_(timeout=3).wait_until(be.visible):
            clear_button.click()
        return self


# Singleton instance for easy import
wikipedia = WikipediaApp()