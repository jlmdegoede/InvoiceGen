from bunq.sdk import context
from bunq.sdk.model import generated
from bunq.sdk.model.generated import object_

from settings.helper import get_setting
from settings.const import BUNQ_API_KEY, DEFAULT_BUNQ_ACCOUNT

from ..models import BunqRequest


class BunqApi(object):
    _REQUEST_CURRENCY = 'EUR'
    _COUNTERPARTY_POINTER_TYPE = 'EMAIL'

    def __init__(self):
        try:
            self.context = context.ApiContext.restore()
        except Exception as e:
            api_key = get_setting(BUNQ_API_KEY, '')
            self.context = context.ApiContext(
                context.ApiEnvironmentType.SANDBOX,
                api_key,
                'test device python'
            )
            self.context.save()

        for user in generated.User.list(self.context):
            self.user_id = user.UserCompany.id_
            self.user = generated.User.get(self.context, self.user_id)
        self.monetary_account = int(get_setting(DEFAULT_BUNQ_ACCOUNT, 0))

    def monetary_accounts(self):
        accounts = generated.MonetaryAccount.list(self.context, self.user_id)
        account_list = []
        for account in accounts:
            account_dict = {'id': account.MonetaryAccountBank.id_}
            for alias in account.MonetaryAccountBank.alias:
                if alias.type_ == 'IBAN':
                    account_dict['name'] = alias.name
                    account_dict['value'] = alias.value
                    account_list.append(account_dict)
        return account_list

    def create_request(self, invoice):
        bunq_request = BunqRequest()
        bunq_request.counterparty_email = invoice.to_company.company_email
        bunq_request.description = invoice.title
        bunq_request.payment_amount = invoice.get_total_amount()
        bunq_request.for_invoice = invoice.id
        bunq_request.status = BunqRequest.PENDING

        request_map = {
            generated.RequestInquiry.FIELD_AMOUNT_INQUIRED: object_.Amount(
                str(bunq_request.payment_amount),
                self._REQUEST_CURRENCY
            ),
            generated.RequestInquiry.FIELD_COUNTERPARTY_ALIAS: object_.Pointer(
                self._COUNTERPARTY_POINTER_TYPE,
                bunq_request.counterparty_email
            ),
            generated.RequestInquiry.FIELD_DESCRIPTION: bunq_request.description,
            generated.RequestInquiry.FIELD_ALLOW_BUNQME: True,
        }
        request_id = generated.RequestInquiry.create(
            self.context,
            request_map,
            self.user_id,
            self.monetary_account
        )
        bunq_request.bunq_request_id = request_id
        bunq_request.save()

    def get_request_status(self, request_id):
        return generated.RequestInquiry.get(
            self.context,
            self.user_id,
            self.monetary_account,
            request_id
        )
