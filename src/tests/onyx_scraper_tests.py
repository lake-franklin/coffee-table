import unittest
from unittest.mock import patch
from src.scripts.onyx_scraper import *


class TestOnyxScraper(unittest.TestCase):

    @patch('scraper.requests.get')
    def test_scrape_product_info(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = """
            <div class="product-preview">
                <a class="product-preview" href="/products/product1">
                    <div class="product-meta">
                        <h3 class="title upper">Product 1</h3>
                    </div>
                </a>
            </div>
            <div class="product-preview">
                <a class="product-preview" href="/products/product2">
                    <div class="product-meta">
                        <h3 class="title upper">Product 2</h3>
                    </div>
                </a>
            </div>
        """

        products = scrape_product_info("http://example.com")
        self.assertEqual(len(products), 2)
        self.assertIn("Product 1", products)
        self.assertIn("Product 2", products)
        self.assertEqual(products["Product 1"], "/products/product1")
        self.assertEqual(products["Product 2"], "/products/product2")

    @patch('scraper.requests.get')
    def test_scrape_product_data(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.side_effect = [
            # Response for product 1
            type('', (object,), {
                'content': """
                    <span class="price">$10</span>
                """
            })(),
            # Response for product 2
            type('', (object,), {
                'content': """
                    <span class="price">$20</span>
                """
            })()
        ]

        base_product_url = "http://example.com/products/"

        product_urls = {
            "Product 1": "/product1",
            "Product 2": "/product2"
        }

        product_data = scrape_product_data(base_product_url, product_urls)
        self.assertEqual(len(product_data), 2)
        self.assertIn("Product 1", product_data)
        self.assertIn("Product 2", product_data)
        self.assertEqual(product_data["Product 1"]["price"], "$10")
        self.assertEqual(product_data["Product 2"]["price"], "$20")


if __name__ == '__main__':
    unittest.main()
