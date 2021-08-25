from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.services.accounts_service import AccountsService

from src.constants import http_status_codes

from src.schemas.account import AccountSchema
from src.schemas.balance import BalanceSchema


accounts = Blueprint("accounts", __name__, url_prefix="/api/v1/accounts")


@accounts.post('/')
@jwt_required()
def create():
    data = request.json
    user_id = get_jwt_identity()

    account_schema = AccountSchema()

    created_account = AccountsService.create(user_id, data)

    return account_schema.jsonify(created_account), http_status_codes.HTTP_201_CREATED


@accounts.get('/')
def index():
    account_schema = AccountSchema(many=True)

    found_accounts = AccountsService.index()

    return account_schema.jsonify(found_accounts), http_status_codes.HTTP_200_OK


@accounts.get('/<account_id>/balance')
def balance(account_id):
    balance_schema = BalanceSchema()

    found_account = AccountsService.retrieve(account_id)

    return balance_schema.jsonify(found_account), http_status_codes.HTTP_200_OK
