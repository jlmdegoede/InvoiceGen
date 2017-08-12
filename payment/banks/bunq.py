from bunq.sdk import context
from bunq.sdk.json import converter
from bunq.sdk.model import generated
from bunq.sdk.model.generated import object_


class BunqApi(object):
    _REQUEST_CURRENCY = 'EUR'
    _COUNTERPARTY_POINTER_TYPE = 'EMAIL'
    _REQUEST_DESCRIPTION = 'This is a generated request!'
    _USER_ITEM_ID = 0  # Put your user ID here
    _MONETARY_ACCOUNT_ITEM_ID = 0  # Put your monetary account ID here
    _STATUS_REVOKED = 'REVOKED'

    def __init__(self):
        self.context = context.ApiContext(
            context.ApiEnvironmentType.SANDBOX,
            '###YOUR_API_KEY###',  # Put your API key here
            'test device python'
        )

        self.context.save()
        ctx_restored = context.ApiContext.restore()
        print('Is original context equal the one saved and restored?:',
              converter.class_to_json(self.context) == converter.class_to_json(ctx_restored))

    def create_request(self, counterparty_email, request_amount, description):
        request_map = {
            generated.RequestInquiry.FIELD_AMOUNT_INQUIRED: object_.Amount(
                request_amount,
                self._REQUEST_CURRENCY
            ),
            generated.RequestInquiry.FIELD_COUNTERPARTY_ALIAS: object_.Pointer(
                self._COUNTERPARTY_POINTER_TYPE,
                counterparty_email
            ),
            generated.RequestInquiry.FIELD_DESCRIPTION: description,
            generated.RequestInquiry.FIELD_ALLOW_BUNQME: True,
        }

        request_id = generated.RequestInquiry.create(
            self.context,
            request_map,
            self._USER_ITEM_ID,
            self._MONETARY_ACCOUNT_ITEM_ID
        )
        print(
            generated.RequestInquiry.get(
                self.context,
                self._USER_ITEM_ID,
                self._MONETARY_ACCOUNT_ITEM_ID,
                request_id
            ).to_json()
        )