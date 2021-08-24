from flask import Blueprint, request

from src.services.transactions_service import TransactionsService

from src.constants import http_status_codes

from src.schemas.transaction import TransactionSchema


transactions = Blueprint("transactions", __name__, url_prefix="/api/v1/transactions")


@transactions.post('/<account_id>/income')
def income(account_id):
    data = request.json

    transaction_schema = TransactionSchema()

    found_transaction = TransactionsService.income(account_id, data)

    return transaction_schema.jsonify(found_transaction), http_status_codes.HTTP_201_CREATED


@transactions.post('/<account_id>/expense')
def expense(account_id):
    data = request.json

    transaction_schema = TransactionSchema()

    found_transaction = TransactionsService.expense(account_id, data)

    return transaction_schema.jsonify(found_transaction), http_status_codes.HTTP_201_CREATED


@transactions.get('/<account_id>/extract')
def extract(account_id):

    transaction_schema = TransactionSchema(many=True)

    found_transactions = TransactionsService.extract(account_id)

    return transaction_schema.jsonify(found_transactions), http_status_codes.HTTP_200_OK
