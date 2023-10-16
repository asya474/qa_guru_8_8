import pytest
from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def another_product():
    return Product("pen", 50, "This is a pen", 300)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    def test_product_check_quantity(self, product):
        assert product.check_quantity(1000)
        assert not product.check_quantity(1001)

    def test_product_buy(self, product):
        product.buy(1000)
        assert product.quantity == 0

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError):
            product.buy(1001)


class TestCart:
    def test_cart_add_new_product(self, cart, product):
        cart.add_product(product, buy_count=3)
        assert len(cart.products) == 1
        assert cart.products[product] == 3

    def test_cart_add_same_product(self, cart, product):
        cart.add_product(product, buy_count=3)

        cart.add_product(product, buy_count=5)

        assert len(cart.products) == 1
        assert cart.products[product] == 8

    def test_cart_remove_product_one_item(self, cart, product):
        cart.add_product(product, buy_count=3)
        cart.remove_product(product, remove_count=1)

        assert len(cart.products) == 1
        assert cart.products[product] == 2

    def test_cart_remove_product_all_items(self, cart, product):
        cart.add_product(product, buy_count=3)
        cart.remove_product(product, remove_count=3)

        assert not cart.products

    def test_cart_remove_product_more_than_in_cart(self, cart, product):
        cart.add_product(product, buy_count=3)
        cart.remove_product(product, remove_count=4)

        assert not cart.products

    def test_cart_remove_product_none_items(self, cart, product):
        cart.add_product(product, buy_count=3)
        cart.remove_product(product)

        assert not cart.products

    def test_cart_remove_not_added_product(self, cart, product):
        with pytest.raises(ValueError):
            cart.remove_product(product)

        assert not cart.products

    def test_cart_clear(self, cart, product):
        cart.add_product(product, buy_count=3)
        cart.clear()

        assert not cart.products

    def test_cart_get_total_price(self, cart, product, another_product):
        cart.add_product(product, buy_count=3)
        cart.add_product(another_product, buy_count=2)

        assert cart.get_total_price() == 400

    def test_cart_buy(self, cart, product, another_product):
        cart.add_product(product, 3)
        cart.add_product(another_product, 2)

        cart.buy()

        assert product.quantity == 997
        assert another_product.quantity == 298
        assert not cart.products

    def test_cart_buy_more_than_available(self, cart, product, another_product):
        cart.add_product(product, buy_count=1001)

        with pytest.raises(ValueError):
            cart.buy()
