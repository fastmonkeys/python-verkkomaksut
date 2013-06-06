# -*- coding: utf-8 -*-
"""
    verkkomaksut
    ~~~~~~~~~~~~

    Python wrapper for the JSON API of Suomen Verkkomaksut.

    :copyright: (c) 2013 by Janne Vanhala.
    :license: BSD, see LICENSE for more details.
"""
__version__ = '0.2.0'

import hashlib
import json
import requests


class VerkkomaksutException(Exception):
    """This exception is raised when the request made to the Verkkomaksut API
    is invalid, or some other error occurs in the usage of the API."""

    def __init__(self, code, message):
        #: Error code is a unique string identifying the error. Possible error
        #: codes are listed in the `documentation`_ of Suomen Verkkomaksut
        #: REST API .
        #:
        #: .. _documentation: http://docs.verkkomaksut.fi/en/ch03s03.html
        self.code = code

        #: An error description of the error in chosen localization. This error
        #: description is not meant to be displayed to the end-user.
        self.message = message


class Contact(object):
    """This class represents the payer of a payment."""

    def __init__(self, first_name, last_name, email, street, postal_code,
                       postal_office, country, telephone=None, mobile=None,
                       company_name=None):
        #: Payer's first name.
        self.first_name = first_name

        #: Payer's surname.
        self.last_name = last_name

        #: Payer's email address.
        self.email = email

        #: Company name.
        self.company_name = company_name

        #: Payer's telephone number.
        self.telephone = telephone

        #: Payer's mobile number.
        self.mobile = mobile

        #: Payer's street address.
        self.street = street

        #: Payer's postal code.
        self.postal_code = postal_code

        #: Payer's post office.
        self.postal_office = postal_office

        #: Payer's country.  The data are sent as a two-numbered character
        #: string in ISO-3166-1 standard format.  For example, Finnish is FI
        #: and Swedish SE.  The data are used for verifying credit history,
        #: and is thus required.
        self.country = country

    @property
    def json(self):
        """JSON representation of this contact."""
        return {
            'telephone': self.telephone,
            'mobile': self.mobile,
            'email': self.email,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'companyName': self.company_name,
            'address': {
                'street': self.street,
                'postalCode': self.postal_code,
                'postalOffice': self.postal_office,
                'country': self.country
            }
        }


class Payment(object):
    def __init__(self, order_number, contact, success_url, failure_url,
                       notification_url, **options):
        #: Order number is a string of characters identifying the customer's
        #: purchase and the used webshop software creates it.
        self.order_number = order_number

        #: Reference number is sent to bank by default and is automatically
        #: created.  In those payment methods that are used as an interface,
        #: this field can contain own reference number, which is sent to the
        #: bank service instead of the automatically generated reference
        #: number.
        self.reference_number = options.get('reference_number')

        #: Any data about the order in text format can be sent to the payment
        #: system.  The most usual pieces of data are customer name and contact
        #: information and order product information.  They are shown in the
        #: Merchant's Panel in payment details.
        self.description = options.get('description')

        #: Payment currency.  Value must EUR for the Finnish banks, otherwise
        #: the payment will not be accepted.
        self.currency = options.get('currency', 'EUR')

        #: Localisation defines default language for the payment method
        #: selection page and presentation format for the sums.  Available
        #: localisations are "fi_FI", "sv_SE" and "en_US". The default
        #: localisation is always "fi_FI".
        self.locale = options.get('locale', 'fi_FI')

        #: A flag indicating whether the product row prices include value
        #: added tax.  If `True` VAT is included in the shown price; otherwise
        #: it will be added.  Therefore, set this to `True`, if the prices in
        #: your webshop include value added tax, and `False` if the prices do
        #: not include value added tax.
        self.include_vat = options.get('include_vat', True)

        self.contact = contact

        #: A list of products. There must be at least one product, and the
        #: maximum number of products is 500.
        self.products = []

        #: URL to which user is directed after a successful payment.
        self.success_url = success_url

        #: URL to which user is directed after a cancelled or failed payment.
        self.failure_url = failure_url

        #: URL to which user is directed, if the payment is pending.  The
        #: status is with NetPosti payment method.  After the actual payment,
        #: the payment is signed for receipt with notify request.
        self.pending_url = options.get('pending_url')

        #: URL requested when the payment is marked as successful.  The URL is
        #: requested with the same GET parameters as success address when the
        #: payment is made.  Notification request is typically executed within
        #: a few minutes from the payment.
        self.notification_url = notification_url

    @property
    def currency(self):
        return self._currency

    @currency.setter
    def currency(self, value):
        if value != 'EUR':
            raise ValueError("Currently EUR is the only supported currency.")
        self._currency = value

    @property
    def locale(self):
        return self._locale

    @locale.setter
    def locale(self, value):
        if value not in ('fi_FI', 'sv_SE', 'en_US'):
            raise ValueError("Given locale is not supported: %r" % value)
        self._locale = value

    @property
    def json(self):
        return {
            'orderNumber': self.order_number,
            'referenceNumber': self.reference_number,
            'description': self.description,
            'currency': self.currency,
            'locale': self.locale,
            'urlSet': {
                'success': self.success_url,
                'failure': self.failure_url,
                'pending': self.pending_url,
                'notification': self.notification_url
            },
            'orderDetails': {
                'includeVat': '1' if self.include_vat else '0',
                'contact': self.contact.json,
                'products': [product.json for product in self.products]
            }
        }


class Product(object):
    TYPE_NORMAL = 1
    TYPE_POSTAGE = 2
    TYPE_PROCESSING = 3

    def __init__(self, title, price, vat, amount=1, code=None, discount=0, type=TYPE_NORMAL):
        #: Product name in free format.  The product title is shown in the
        #: Merchant's Panel and on Klarna service invoices on a product row.
        #: Product details are shown also on the payment method selection page.
        self.title = title

        #: Optional product number. Using a product number may help in
        #: aligning a correct product.
        self.code = code

        #: If an order consists of several samples of the same product, you
        #: can enter the number of products here and there won't be a need for
        #: adding each product as a separate row.  Usually this field contains
        #: value 1.
        self.amount = amount

        #: Price for one product.  If the field payment includes VAT, this is
        #: a price excluding VAT.  Otherwise, this is a price including VAT.
        #: The price can also be negative if you want to add discounts to the
        #: service.  However, the total amount of the product rows must always
        #: be bigger than 0.
        self.price = price

        #: Tax percentage for a product.  The value added tax in Finland for
        #: most products is 23.
        self.vat = vat

        #: If you have reduced the product price, you can show the discount
        #: percentage as a figure between 0 and 100 in this field.  Default
        #: discount value is 0.
        self.discount = discount

        #: A type can be specified for the product row.  `Product.TYPE_NORMAL`
        #: refers to a normal product row.  `Product.TYPE_POSTAGE` can be used
        #: for postage and `Product.TYPE_PROCESSING` for processing costs.
        #: `Product.TYPE_NORMAL` can be used for all rows, but postage and
        #: processing costs cannot be differentiated from other rows to the
        #: invoice.  Default value for the field is `Product.TYPE_NORMAL`.
        self.type = type

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if value not in (
            Product.TYPE_NORMAL,
            Product.TYPE_POSTAGE,
            Product.TYPE_PROCESSING
        ):
            raise ValueError('Given product type not supported: %r' % value)
        self._type = value

    @property
    def json(self):
        return {
            'title': self.title,
            'code': self.code,
            'amount': self.amount,
            'price': self.price,
            'vat': self.vat,
            'discount': self.discount,
            'type': self.type
        }


class Client(object):
    SERVICE_URL = "https://payment.verkkomaksut.fi/api-payment/create"

    def __init__(self, merchant_id='13466',
                       merchant_secret='6pKF4jkv97zmqBJ3ZL8gUw5DfT2NMQ'):
        """
        Initialize the client with your own merchant id and merchant secret.

        :param merchant_id: Mercant ID is given to you by Suomen Verkkomaksut
            when you make the contract. Default is the test merchant account.
        :param merchant_secret: Merchant secret is given to you by Suoment
            Verkkomaksut. Default is the test merchant account.
        """
        self.merchant_id = merchant_id
        self.merchant_secret = merchant_secret
        self.session = requests.Session()
        self.session.auth = (merchant_id, merchant_secret)
        self.session.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-Verkkomaksut-Api-Version': '1'
        }

    def create_payment(self, payment):
        """Creates a new payment and returns a `dict` with the following data:
        `orderNumber`

        :param payment: a `Payment` object

        """
        response = self.session.post(self.SERVICE_URL,
            data=json.dumps(payment.json)
        )

        if response.status_code != requests.codes.created:
            data = json.loads(response.content)
            raise VerkkomaksutException(
                code=data['errorCode'],
                message=data['errorMessage']
            )

        data = json.loads(response.content)
        return {
            'order_number': data['orderNumber'],
            'token': data['token'],
            'url': data['url']
        }

    def _calculate_payment_receipt_hash(self, *params):
        base = '|'.join(params + (self.merchant_secret,))
        return hashlib.md5(base).hexdigest().upper()

    def _validate_payment_receipt_parameters(self, authcode, *params):
        hash_ = self._calculate_payment_receipt_hash(*params)
        return authcode == hash_

    def validate_successful_payment(self, authcode, order_number, timestamp,
                                   paid, method):
        """
        Validates parameters sent by Suomen Verkkomaksut to the success URL or
        pending URL after a successful payment. The parameters must be validated
        in order to avoid hacking attempts to confirm payment. Returns `True`
        when the parameters are valid, and `False` otherwise.

        :param authcode: A hash value calculated by payment system.
        :param order_number: The same order number that was previously sent to
            the payment system. Order number uniquely identifies each payment.
        :param timestamp: A Unix timestamp produced by Suomen Verkkomaksut used
            for calculating the hash.
        :param paid: A 10-character payment code, which is part of payment
            confirmation. In case of a pending payment, this parameter is
            always "0000000000".
        :param method: The payment method used.
        """
        return self._validate_payment_receipt_parameters(
            authcode, order_number, timestamp, paid, method
        )

    def validate_failed_payment(self, authcode, order_number, timestamp):
        """
        Validates parameters sent by Suomen Verkkomaksut to the failure URL
        after a cancelled or failed payment.

        :param authcode: A hash value calculated by payment system.
        :param order_number: The same order number that was previously sent to
            the payment system. Order number uniquely identifies each payment.
        :param timestamp: A Unix timestamp produced by Suomen Verkkomaksut used
            for calculating the hash.
        """
        return self._validate_payment_receipt_parameters(
            authcode, order_number, timestamp
        )
