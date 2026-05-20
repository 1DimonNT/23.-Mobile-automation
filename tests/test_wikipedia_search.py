from __future__ import annotations

import allure
import pytest

from pages.wikipedia_app import wikipedia


@allure.suite("Wikipedia Mobile Tests")
@allure.tag("android", "search", "bstack")
@allure.title("Search functionality tests")
class TestWikipediaSearch:

    @allure.title("Search for 'BrowserStack' and verify results exist")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("""
    Test objective: Verify that search functionality works correctly.

    Steps:
    1. Close onboarding if present
    2. Search for query 'BrowserStack'
    3. Verify that search results contain the search term
    """)
    @pytest.mark.android
    @pytest.mark.search
    @pytest.mark.bstack
    def test_search_in_wikipedia__valid_query_BrowserStack__should_find_results(self):
        # Given: Wikipedia app is open
        wikipedia.close_onboarding_if_present()

        # When: User searches for "BrowserStack"
        wikipedia.search("BrowserStack")

        # Then: Search results should contain "BrowserStack"
        wikipedia.results_should_contain_text("BrowserStack")

    @allure.title("Search for 'Selenium' and verify results count")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("""
    Test objective: Verify that search returns multiple results.

    Steps:
    1. Search for query 'Selenium'
    2. Verify that more than 1 result is displayed
    """)
    @pytest.mark.android
    @pytest.mark.search
    def test_search_in_wikipedia__valid_query_Selenium__should_have_multiple_results(self):
        # Given: Wikipedia app is open
        wikipedia.close_onboarding_if_present()

        # When: User searches for "Selenium"
        wikipedia.search("Selenium")

        # Then: Should have more than 1 result
        wikipedia.results_should_have_count_greater_than(1)

    @allure.title("Search for non-existent query and verify no results")
    @allure.severity(allure.severity_level.MINOR)
    @allure.description("""
    Test objective: Verify behavior for non-existent search query.

    Steps:
    1. Search for non-existent query 'xyzabc123'
    2. Verify appropriate message or empty results
    """)
    @pytest.mark.android
    @pytest.mark.search
    def test_search_in_wikipedia__invalid_query__should_show_no_results(self):
        # Given: Wikipedia app is open
        wikipedia.close_onboarding_if_present()

        # When: User searches for non-existent term
        wikipedia.search("xyzabc123")

        # Then: Should show "No results" or empty state
        # Note: This is a placeholder - implement based on actual app behavior
        import time
        time.sleep(2)

        # Check that there are no results (or error message)
        page_source = wikipedia.browser.config.driver.page_source
        assert "No results" in page_source or "No matching" in page_source

        allure.attach(
            "Search for non-existent query completed",
            name="Search result",
            attachment_type=allure.attachment_type.TEXT
        )