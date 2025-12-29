import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from bson import ObjectId
from services.order_service import (
    create_order, get_order_by_id, get_orders_by_user,
    get_all_orders, update_order_status, delete_order, get_all_users
)

@pytest.fixture
def mock_orders_col():
    with patch('services.order_service.orders_col') as mock:
        yield mock

@pytest.fixture
def mock_users_col():
    with patch('services.order_service.users_col') as mock:
        yield mock

class TestOrderService:

    def test_create_order_success(self, mock_orders_col, mock_users_col):
        mock_users_col.find_one.return_value = {'_id': ObjectId(), 'email': 'teste@email.com'}
        mock_orders_col.insert_one.return_value = MagicMock(inserted_id=ObjectId())

        items = [{'name': 'Burger', 'quantity': 2, 'unit_price': 10.0, 'total': 20.0}]
        response, status = create_order('teste@email.com', items, 20.0)

        assert status == 201
        assert 'message' in response
        assert 'order_id' in response
        mock_orders_col.insert_one.assert_called_once()

    def test_create_order_user_not_found(self, mock_orders_col, mock_users_col):
        mock_users_col.find_one.return_value = None

        items = [{'name': 'Burger', 'quantity': 2, 'unit_price': 10.0, 'total': 20.0}]
        response, status = create_order('naoexiste@email.com', items, 20.0)

        assert status == 404
        assert 'error' in response
        mock_orders_col.insert_one.assert_not_called()

    def test_get_order_by_id_found(self, mock_orders_col):
        order_id = ObjectId()
        mock_orders_col.find_one.return_value = {
            '_id': order_id,
            'user_email': 'teste@email.com',
            'items': [],
            'total': 20.0,
            'status': 'pending',
            'created_at': datetime.utcnow()
        }

        order = get_order_by_id(str(order_id))

        assert order is not None
        assert order['user_email'] == 'teste@email.com'

    def test_get_order_by_id_not_found(self, mock_orders_col):
        mock_orders_col.find_one.return_value = None

        order = get_order_by_id(str(ObjectId()))

        assert order is None

    def test_get_order_by_id_invalid_id(self, mock_orders_col):
        order = get_order_by_id('invalid_id')
        assert order is None

    def test_get_orders_by_user(self, mock_orders_col):
        mock_orders_col.find.return_value.sort.return_value = [
            {
                '_id': ObjectId(),
                'user_email': 'teste@email.com',
                'items': [],
                'total': 20.0,
                'status': 'pending'
            }
        ]

        orders = get_orders_by_user('teste@email.com')

        assert len(orders) == 1
        assert orders[0]['user_email'] == 'teste@email.com'

    def test_get_all_orders(self, mock_orders_col):
        mock_orders_col.find.return_value.sort.return_value = [
            {'_id': ObjectId(), 'user_email': 'user1@email.com', 'status': 'pending'},
            {'_id': ObjectId(), 'user_email': 'user2@email.com', 'status': 'completed'}
        ]

        orders = get_all_orders()

        assert len(orders) == 2

    def test_update_order_status_success(self, mock_orders_col):
        mock_orders_col.update_one.return_value = MagicMock(modified_count=1)

        response, status = update_order_status(str(ObjectId()), 'completed')

        assert status == 200
        assert 'message' in response

    def test_update_order_status_not_found(self, mock_orders_col):
        mock_orders_col.update_one.return_value = MagicMock(modified_count=0)

        response, status = update_order_status(str(ObjectId()), 'completed')

        assert status == 404
        assert 'error' in response

    def test_update_order_status_invalid_id(self, mock_orders_col):
        mock_orders_col.update_one.side_effect = Exception('Invalid ID')

        response, status = update_order_status('invalid_id', 'completed')

        assert status == 400
        assert 'error' in response

    def test_delete_order_success(self, mock_orders_col):
        mock_orders_col.delete_one.return_value = MagicMock(deleted_count=1)

        response, status = delete_order(str(ObjectId()))

        assert status == 200
        assert 'message' in response

    def test_delete_order_not_found(self, mock_orders_col):
        mock_orders_col.delete_one.return_value = MagicMock(deleted_count=0)

        response, status = delete_order(str(ObjectId()))

        assert status == 404
        assert 'error' in response

    def test_delete_order_invalid_id(self, mock_orders_col):
        mock_orders_col.delete_one.side_effect = Exception('Invalid ID')

        response, status = delete_order('invalid_id')

        assert status == 400
        assert 'error' in response

    def test_get_all_users(self, mock_users_col):
        mock_users_col.find.return_value.sort.return_value = [
            {'email': 'user1@email.com', 'name': 'User 1'},
            {'email': 'user2@email.com', 'name': 'User 2'}
        ]

        users = get_all_users()

        assert len(users) == 2
