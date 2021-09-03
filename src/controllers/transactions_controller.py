"""
Transactions Controller File
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.services.transactions_service import TransactionsService

from src.constants import http_status_codes

from src.schemas.transaction import TransactionSchema


transactions = Blueprint("transactions", __name__, url_prefix="/api/v1/transactions")


@transactions.post('/<account_id>/income')
@jwt_required()
def income(account_id):
    """
    Create income for logged in user account
    """
    data = request.json
    user_id = get_jwt_identity()

    transaction_schema = TransactionSchema()

    found_transaction = TransactionsService.income(user_id, account_id, data)

    return transaction_schema.jsonify(found_transaction), http_status_codes.HTTP_201_CREATED


@transactions.post('/<account_id>/expense')
@jwt_required()
def expense(account_id):
    """
    Create expense for logged in user account
    """
    data = request.json
    user_id = get_jwt_identity()

    transaction_schema = TransactionSchema()

    found_transaction = TransactionsService.expense(user_id, account_id, data)

    return transaction_schema.jsonify(found_transaction), http_status_codes.HTTP_201_CREATED


@transactions.get('/<account_id>/extract')
@jwt_required()
def extract(account_id):
    """
    Get logged in user account extract
    """
    user_id = get_jwt_identity()

    transaction_schema = TransactionSchema(many=True)

    found_transactions = TransactionsService.extract(user_id, account_id)

    return transaction_schema.jsonify(found_transactions), http_status_codes.HTTP_200_OK
