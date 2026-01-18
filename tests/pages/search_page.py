from .category_page import CategoryPage
from config import BASE_URL


class SearchPage(CategoryPage):
    def get_search_url(self, query: str) -> str:
        return f"{BASE_URL}szukaj?controller=search&s={query}"
