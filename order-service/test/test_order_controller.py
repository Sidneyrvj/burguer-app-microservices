import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from controllers.order_controller import order_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.register_blueprint(order_bp, url_prefix='/order')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

class TestOrderController:

    @patch('controllers.order_controller.render_template')
    @patch('controllers.order_controller.redirect')
    @patch('controllers.order_controller.create_order')
    @patch('controllers.order_controller.get_all_users')
    @patch('controllers.order_controller.get_products_from_service')
    @patch('controllers.order_controller.get_categories_from_service')
    def test_create_order_post_success(self, mock_categories, mock_products, mock_users, mock_create, mock_redirect, mock_render, client):
        mock_create.return_value = ({'message': 'Pedido criado com sucesso'}, 201)
        mock_redirect.return_value = 'redirect_response'

        response = client.post('/order/create', data={
            'user_email': 'teste@email.com',
            'item_name': ['Burger'],
            'item_quantity': ['2'],
            'item_price': ['10.0']
        })

        mock_create.assert_called_once()
        mock_redirect.assert_called()

    @patch('controllers.order_controller.render_template')
    @patch('controllers.order_controller.redirect')
    @patch('controllers.order_controller.create_order')
    @patch('controllers.order_controller.get_all_users')
    @patch('controllers.order_controller.get_products_from_service')
    @patch('controllers.order_controller.get_categories_from_service')
    def test_create_order_post_no_items(self, mock_categories, mock_products, mock_users, mock_create, mock_redirect, mock_render, client):
        response = client.post('/order/create', data={
            'user_email': 'teste@email.com',
            'item_name': [],
            'item_quantity': [],
            'item_price': []
        })

        mock_create.assert_not_called()
        mock_redirect.assert_called()

    @patch('controllers.order_controller.render_template')
    @patch('controllers.order_controller.get_all_users')
    @patch('controllers.order_controller.get_products_from_service')
    @patch('controllers.order_controller.get_categories_from_service')
    def test_create_order_get(self, mock_categories, mock_products, mock_users, mock_render, client):
        mock_users.return_value = [{'email': 'teste@email.com', 'name': 'Teste'}]
        mock_products.return_value = []
        mock_categories.return_value = []
        mock_render.return_value = 'rendered_template'

        response = client.get('/order/create')

        assert response.status_code == 200
        mock_render.assert_called_once()

    @patch('controllers.order_controller.render_template')
    @patch('controllers.order_controller.get_all_orders')
    def test_list_orders(self, mock_get_all, mock_render, client):
        mock_get_all.return_value = [{'id': '123', 'user_email': 'teste@email.com'}]
        mock_render.return_value = 'rendered_template'

        response = client.get('/order/list')

        assert response.status_code == 200
        mock_render.assert_called_once()

    @patch('controllers.order_controller.render_template')
    @patch('controllers.order_controller.get_order_by_id')
    def test_order_details_found(self, mock_get_order, mock_render, client):
        mock_get_order.return_value = {'id': '123', 'user_email': 'teste@email.com'}
        mock_render.return_value = 'rendered_template'

        response = client.get('/order/details/123')

        assert response.status_code == 200
        mock_render.assert_called_once()

    @patch('controllers.order_controller.redirect')
    @patch('controllers.order_controller.get_order_by_id')
    def test_order_details_not_found(self, mock_get_order, mock_redirect, client):
        mock_get_order.return_value = None
        mock_redirect.return_value = 'redirect_response'

        response = client.get('/order/details/123')

        mock_redirect.assert_called()

    @patch('controllers.order_controller.render_template')
    @patch('controllers.order_controller.get_orders_by_user')
    def test_user_orders(self, mock_get_by_user, mock_render, client):
        mock_get_by_user.return_value = [{'id': '123', 'user_email': 'teste@email.com'}]
        mock_render.return_value = 'rendered_template'

        response = client.get('/order/user/teste@email.com')

        assert response.status_code == 200
        mock_render.assert_called_once()

    @patch('controllers.order_controller.redirect')
    @patch('controllers.order_controller.update_order_status')
    def test_update_status_success(self, mock_update, mock_redirect, client):
        mock_update.return_value = ({'message': 'Status atualizado'}, 200)
        mock_redirect.return_value = 'redirect_response'

        response = client.post('/order/update_status/123', data={'status': 'completed'})

        mock_update.assert_called_once_with('123', 'completed')
        mock_redirect.assert_called()

    @patch('controllers.order_controller.redirect')
    def test_update_status_no_status(self, mock_redirect, client):
        mock_redirect.return_value = 'redirect_response'

        response = client.post('/order/update_status/123', data={})

        mock_redirect.assert_called()

    @patch('controllers.order_controller.redirect')
    @patch('controllers.order_controller.delete_order')
    def test_delete_order_success(self, mock_delete, mock_redirect, client):
        mock_delete.return_value = ({'message': 'Pedido deletado'}, 200)
        mock_redirect.return_value = 'redirect_response'

        response = client.post('/order/delete/123')

        mock_delete.assert_called_once_with('123')
        mock_redirect.assert_called()
