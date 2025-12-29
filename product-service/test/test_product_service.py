import pytest
from unittest.mock import patch, MagicMock
from bson import ObjectId
from services.product_service import (
    create_product, get_all_products, get_available_products,
    get_products_by_category, get_product_by_id, update_product,
    delete_product, get_categories, initialize_products
)

@pytest.fixture
def mock_products_col():
    with patch('services.product_service.products_col') as mock:
        yield mock

class TestProductService:

    def test_create_product_success(self, mock_products_col):
        mock_products_col.insert_one.return_value = MagicMock(inserted_id=ObjectId())

        response, status = create_product('Burger X', 'Delicious burger', 'Hambúrgueres', '25.90', ['pão', 'carne'])

        assert status == 201
        assert 'message' in response
        assert 'id' in response

    def test_create_product_invalid_price(self, mock_products_col):
        response, status = create_product('Burger X', 'Delicious burger', 'Hambúrgueres', 'invalid', ['pão'])

        assert status == 400
        assert 'error' in response

    def test_get_all_products(self, mock_products_col):
        mock_products_col.find.return_value.sort.return_value = [
            {'_id': ObjectId(), 'name': 'Burger 1', 'price': 20.0, 'available': True},
            {'_id': ObjectId(), 'name': 'Burger 2', 'price': 25.0, 'available': False}
        ]

        products = get_all_products()

        assert len(products) == 2

    def test_get_available_products(self, mock_products_col):
        mock_products_col.find.return_value.sort.return_value = [
            {'_id': ObjectId(), 'name': 'Burger 1', 'price': 20.0, 'available': True}
        ]

        products = get_available_products()

        assert len(products) == 1
        mock_products_col.find.assert_called_with({'available': True})

    def test_get_products_by_category(self, mock_products_col):
        mock_products_col.find.return_value.sort.return_value = [
            {'_id': ObjectId(), 'name': 'Burger 1', 'category': 'Hambúrgueres', 'available': True}
        ]

        products = get_products_by_category('Hambúrgueres')

        assert len(products) == 1
        mock_products_col.find.assert_called_with({'category': 'Hambúrgueres', 'available': True})

    def test_get_product_by_id_found(self, mock_products_col):
        product_id = ObjectId()
        mock_products_col.find_one.return_value = {
            '_id': product_id,
            'name': 'Burger X',
            'price': 25.90
        }

        product = get_product_by_id(str(product_id))

        assert product is not None
        assert product['name'] == 'Burger X'

    def test_get_product_by_id_not_found(self, mock_products_col):
        mock_products_col.find_one.return_value = None

        product = get_product_by_id(str(ObjectId()))

        assert product is None

    def test_get_product_by_id_invalid_id(self, mock_products_col):
        product = get_product_by_id('invalid_id')

        assert product is None

    def test_update_product_success(self, mock_products_col):
        mock_products_col.update_one.return_value = MagicMock(modified_count=1)

        result = update_product(str(ObjectId()), 'New Name', 'New Desc', 'Category', '30.0', ['ingredient'], True)

        assert result is True

    def test_update_product_not_modified(self, mock_products_col):
        mock_products_col.update_one.return_value = MagicMock(modified_count=0)

        result = update_product(str(ObjectId()), 'New Name', 'New Desc', 'Category', '30.0', ['ingredient'], True)

        assert result is False

    def test_update_product_exception(self, mock_products_col):
        mock_products_col.update_one.side_effect = Exception('DB Error')

        result = update_product('invalid_id', 'Name', 'Desc', 'Category', '30.0', ['ingredient'], True)

        assert result is False

    def test_delete_product_success(self, mock_products_col):
        mock_products_col.delete_one.return_value = MagicMock(deleted_count=1)

        result = delete_product(str(ObjectId()))

        assert result is True

    def test_delete_product_not_found(self, mock_products_col):
        mock_products_col.delete_one.return_value = MagicMock(deleted_count=0)

        result = delete_product(str(ObjectId()))

        assert result is False

    def test_delete_product_exception(self, mock_products_col):
        mock_products_col.delete_one.side_effect = Exception('DB Error')

        result = delete_product('invalid_id')

        assert result is False

    def test_get_categories(self, mock_products_col):
        mock_products_col.distinct.return_value = ['Hambúrgueres', 'Bebidas', 'Sobremesas']

        categories = get_categories()

        assert len(categories) == 3
        assert 'Hambúrgueres' in categories

    def test_initialize_products_empty_db(self, mock_products_col):
        mock_products_col.count_documents.return_value = 0

        initialize_products()

        mock_products_col.insert_many.assert_called_once()

    def test_initialize_products_has_data(self, mock_products_col):
        mock_products_col.count_documents.return_value = 10

        initialize_products()

        mock_products_col.insert_many.assert_not_called()
