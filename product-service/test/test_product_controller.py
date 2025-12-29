import pytest
from unittest.mock import patch, MagicMock

# IMPORTANTE: Mockar initialize_products ANTES de importar o controller
with patch('services.product_service.initialize_products'):
    from flask import Flask
    from controllers.product_controller import product_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.register_blueprint(product_bp, url_prefix='/product')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

class TestProductController:

    @patch('controllers.product_controller.render_template')
    @patch('controllers.product_controller.get_available_products')
    @patch('controllers.product_controller.get_categories')
    def test_list_products(self, mock_categories, mock_products, mock_render, client):
        mock_products.return_value = [{'id': '123', 'name': 'Burger X'}]
        mock_categories.return_value = ['Hambúrgueres', 'Bebidas']
        mock_render.return_value = 'rendered_template'

        response = client.get('/product/list')

        assert response.status_code == 200
        mock_render.assert_called_once()

    @patch('controllers.product_controller.render_template')
    @patch('controllers.product_controller.get_available_products')
    @patch('controllers.product_controller.get_products_by_category')
    @patch('controllers.product_controller.get_categories')
    def test_list_products_with_category(self, mock_categories, mock_by_category, mock_available, mock_render, client):
        mock_available.return_value = []
        mock_by_category.return_value = [{'id': '123', 'name': 'Burger X'}]
        mock_categories.return_value = ['Hambúrgueres']
        mock_render.return_value = 'rendered_template'

        response = client.get('/product/list?category=Hambúrgueres')

        assert response.status_code == 200
        mock_by_category.assert_called_once_with('Hambúrgueres')

    @patch('controllers.product_controller.render_template')
    @patch('controllers.product_controller.get_all_products')
    @patch('controllers.product_controller.get_categories')
    def test_admin_products(self, mock_categories, mock_products, mock_render, client):
        mock_products.return_value = [{'id': '123', 'name': 'Burger X'}]
        mock_categories.return_value = ['Hambúrgueres']
        mock_render.return_value = 'rendered_template'

        response = client.get('/product/admin')

        assert response.status_code == 200
        mock_render.assert_called_once()

    @patch('controllers.product_controller.render_template')
    @patch('controllers.product_controller.get_categories')
    def test_create_product_get(self, mock_categories, mock_render, client):
        mock_categories.return_value = ['Hambúrgueres', 'Bebidas']
        mock_render.return_value = 'rendered_template'

        response = client.get('/product/create')

        assert response.status_code == 200
        mock_render.assert_called_once()

    @patch('controllers.product_controller.redirect')
    @patch('controllers.product_controller.create_product')
    def test_create_product_post_success(self, mock_create, mock_redirect, client):
        mock_create.return_value = ({'message': 'Produto criado'}, 201)
        mock_redirect.return_value = 'redirect_response'

        response = client.post('/product/create', data={
            'name': 'Burger X',
            'description': 'Delicious',
            'category': 'Hambúrgueres',
            'price': '25.90',
            'ingredients': 'pão, carne, queijo',
            'available': 'on'
        })

        mock_create.assert_called_once()
        mock_redirect.assert_called()

    @patch('controllers.product_controller.redirect')
    @patch('controllers.product_controller.create_product')
    def test_create_product_post_error(self, mock_create, mock_redirect, client):
        mock_create.return_value = ({'error': 'Preço inválido'}, 400)
        mock_redirect.return_value = 'redirect_response'

        response = client.post('/product/create', data={
            'name': 'Burger X',
            'description': 'Delicious',
            'category': 'Hambúrgueres',
            'price': 'invalid',
            'ingredients': 'pão, carne',
            'available': 'on'
        })

        mock_redirect.assert_called()

    @patch('controllers.product_controller.render_template')
    @patch('controllers.product_controller.get_product_by_id')
    @patch('controllers.product_controller.get_categories')
    def test_edit_product_get(self, mock_categories, mock_get_product, mock_render, client):
        mock_get_product.return_value = {'id': '123', 'name': 'Burger X', 'ingredients': ['pão']}
        mock_categories.return_value = ['Hambúrgueres']
        mock_render.return_value = 'rendered_template'

        response = client.get('/product/edit/123')

        assert response.status_code == 200
        mock_render.assert_called_once()

    @patch('controllers.product_controller.redirect')
    @patch('controllers.product_controller.get_product_by_id')
    def test_edit_product_not_found(self, mock_get_product, mock_redirect, client):
        mock_get_product.return_value = None
        mock_redirect.return_value = 'redirect_response'

        response = client.get('/product/edit/999')

        mock_redirect.assert_called()

    @patch('controllers.product_controller.redirect')
    @patch('controllers.product_controller.get_product_by_id')
    @patch('controllers.product_controller.update_product')
    def test_edit_product_post_success(self, mock_update, mock_get_product, mock_redirect, client):
        mock_get_product.return_value = {'id': '123', 'name': 'Burger X'}
        mock_update.return_value = True
        mock_redirect.return_value = 'redirect_response'

        response = client.post('/product/edit/123', data={
            'name': 'Burger X Updated',
            'description': 'New Description',
            'category': 'Hambúrgueres',
            'price': '30.00',
            'ingredients': 'pão, carne',
            'available': 'on'
        })

        mock_update.assert_called_once()
        mock_redirect.assert_called()

    @patch('controllers.product_controller.redirect')
    @patch('controllers.product_controller.get_product_by_id')
    @patch('controllers.product_controller.update_product')
    def test_edit_product_post_error(self, mock_update, mock_get_product, mock_redirect, client):
        mock_get_product.return_value = {'id': '123', 'name': 'Burger X'}
        mock_update.return_value = False
        mock_redirect.return_value = 'redirect_response'

        response = client.post('/product/edit/123', data={
            'name': 'Burger X',
            'description': 'Desc',
            'category': 'Hambúrgueres',
            'price': '25.00',
            'ingredients': 'pão',
            'available': 'on'
        })

        mock_redirect.assert_called()

    @patch('controllers.product_controller.redirect')
    @patch('controllers.product_controller.delete_product')
    def test_delete_product_success(self, mock_delete, mock_redirect, client):
        mock_delete.return_value = True
        mock_redirect.return_value = 'redirect_response'

        response = client.post('/product/delete/123')

        mock_delete.assert_called_once_with('123')
        mock_redirect.assert_called()

    @patch('controllers.product_controller.redirect')
    @patch('controllers.product_controller.delete_product')
    def test_delete_product_error(self, mock_delete, mock_redirect, client):
        mock_delete.return_value = False
        mock_redirect.return_value = 'redirect_response'

        response = client.post('/product/delete/999')

        mock_redirect.assert_called()

    @patch('controllers.product_controller.render_template')
    @patch('controllers.product_controller.get_product_by_id')
    def test_details_product_found(self, mock_get_product, mock_render, client):
        mock_get_product.return_value = {'id': '123', 'name': 'Burger X'}
        mock_render.return_value = 'rendered_template'

        response = client.get('/product/details/123')

        assert response.status_code == 200
        mock_render.assert_called_once()

    @patch('controllers.product_controller.redirect')
    @patch('controllers.product_controller.get_product_by_id')
    def test_details_product_not_found(self, mock_get_product, mock_redirect, client):
        mock_get_product.return_value = None
        mock_redirect.return_value = 'redirect_response'

        response = client.get('/product/details/999')

        mock_redirect.assert_called()

    @patch('controllers.product_controller.get_available_products')
    def test_api_products(self, mock_products, client):
        mock_products.return_value = [{'id': '123', 'name': 'Burger X'}]

        response = client.get('/product/api/products')

        assert response.status_code == 200
        assert response.json == [{'id': '123', 'name': 'Burger X'}]

    @patch('controllers.product_controller.get_products_by_category')
    def test_api_products_with_category(self, mock_by_category, client):
        mock_by_category.return_value = [{'id': '123', 'name': 'Burger X'}]

        response = client.get('/product/api/products?category=Hambúrgueres')

        assert response.status_code == 200
        mock_by_category.assert_called_once_with('Hambúrgueres')

    @patch('controllers.product_controller.get_categories')
    def test_api_categories(self, mock_categories, client):
        mock_categories.return_value = ['Hambúrgueres', 'Bebidas']

        response = client.get('/product/api/categories')

        assert response.status_code == 200
        assert response.json == ['Hambúrgueres', 'Bebidas']
