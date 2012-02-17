# -*- coding: utf-8 -*-
"""
    test_verkkomaksut
    ~~~~~~~~~~~~~~~~~

    Tests for `verkkomaksut` module.

    :copyright: (c) 2012 by Janne Vanhala.
    :license: BSD, see LICENSE for more details.
"""
import requests
from flexmock import flexmock
from pytest import raises
from verkkomaksut import (
    Client,
    Contact,
    Payment,
    Product,
    VerkkomaksutException
)


class TestVerkkomaksutException(object):
    def setup_method(self, method):
        self.exception = VerkkomaksutException('code', 'message')

    def test_is_an_exception(self):
        assert isinstance(self.exception, Exception)

    def test_sets_error_code(self):
        assert self.exception.code == 'code'

    def test_sets_error_message(self):
        assert self.exception.message == 'message'


class TestContactWithMinimumParameters(object):
    def setup_method(self, method):
        self.contact = Contact(
            first_name='Matti',
            last_name='Meikäläinen',
            email='matti.meikalainen@gmail.com',
            street='Esimerkkikatu 123',
            postal_code='01234',
            postal_office='Helsinki',
            country='FI'
        )

    def test_sets_first_name(self):
        assert self.contact.first_name == 'Matti'

    def test_sets_last_name(self):
        assert self.contact.last_name == 'Meikäläinen'

    def test_sets_email(self):
        assert self.contact.email == 'matti.meikalainen@gmail.com'

    def test_sets_street(self):
        assert self.contact.street == 'Esimerkkikatu 123'

    def test_sets_postal_code(self):
        assert self.contact.postal_code == '01234'

    def test_sets_postal_office(self):
        assert self.contact.postal_office == 'Helsinki'

    def test_sets_country(self):
        assert self.contact.country == 'FI'

    def test_telephone_is_none_by_default(self):
        assert self.contact.telephone is None

    def test_mobile_is_none_by_default(self):
        assert self.contact.mobile is None

    def test_company_name_is_none_by_default(self):
        assert self.contact.company_name is None


class TestContactWithAllParameters(object):
    def setup_method(self, method):
        self.contact = Contact(
            first_name='Matti',
            last_name='Meikäläinen',
            email='matti.meikalainen@gmail.com',
            street='Esimerkkikatu 123',
            postal_code='01234',
            postal_office='Helsinki',
            country='FI',
            telephone='020123456',
            mobile='050123456',
            company_name='Yhtiö'
        )

    def test_sets_telephone(self):
        assert self.contact.telephone == '020123456'

    def test_sets_mobile(self):
        assert self.contact.mobile == '050123456'

    def test_sets_company_name(self):
        assert self.contact.company_name == 'Yhtiö'

    def test_json(self):
        assert self.contact.json == {
            'telephone': '020123456',
            'mobile': '050123456',
            'email': 'matti.meikalainen@gmail.com',
            'firstName': 'Matti',
            'lastName': 'Meikäläinen',
            'companyName': 'Yhtiö',
            'address': {
                'street': 'Esimerkkikatu 123',
                'postalCode': '01234',
                'postalOffice': 'Helsinki',
                'country': 'FI',
            },
        }


class TestProductWithMinimumParameters(object):
    def setup_method(self, method):
        self.product = Product(
            title='Esimerkkituote',
            price='19.90',
            vat='23.00'
        )

    def test_sets_title(self):
        assert self.product.title == 'Esimerkkituote'

    def test_sets_price(self):
        assert self.product.price == '19.90'

    def test_sets_vat(self):
        assert self.product.vat == '23.00'

    def test_amount_is_one_by_default(self):
        assert self.product.amount == 1

    def test_code_is_none_by_default(self):
        assert self.product.code is None

    def test_discount_is_zero_by_default(self):
        assert self.product.discount == 0

    def test_type_is_normal_by_default(self):
        assert self.product.type == Product.TYPE_NORMAL

    def test_type_can_be_normal(self):
        self.product.type = Product.TYPE_NORMAL
        assert self.product.type == Product.TYPE_NORMAL

    def test_type_can_be_postage(self):
        self.product.type = Product.TYPE_POSTAGE
        assert self.product.type == Product.TYPE_POSTAGE

    def test_type_can_be_processing(self):
        self.product.type = Product.TYPE_PROCESSING
        assert self.product.type == Product.TYPE_PROCESSING

    def test_raises_value_error_on_unsupported_type(self):
        with raises(ValueError) as exc_info:
            self.product.type = 0
        assert exc_info.value.message == 'Given product type not supported: 0'


class TestProductWithAllParameters(object):
    def setup_method(self, method):
        self.product = Product(
            title='Esimerkkituote',
            price='19.90',
            vat=23,
            amount=2,
            code='XX-123',
            discount=50,
            type=Product.TYPE_POSTAGE
        )

    def test_sets_amount(self):
        assert self.product.amount == 2

    def test_sets_code(self):
        assert self.product.code == 'XX-123'

    def test_sets_discount(self):
        assert self.product.discount == 50

    def test_sets_type(self):
        assert self.product.type == Product.TYPE_POSTAGE

    def test_json(self):
        assert self.product.json == {
            'title': 'Esimerkkituote',
            'code': 'XX-123',
            'amount': 2,
            'price': '19.90',
            'vat': 23,
            'discount': 50,
            'type': 2
        }


class TestPaymentWithMinimumParameters(object):
    def setup_method(self, method):
        self.contact = Contact(
            first_name='Matti',
            last_name='Meikäläinen',
            email='matti.meikalainen@gmail.com',
            street='Esimerkkikatu 123',
            postal_code='01234',
            postal_office='Helsinki',
            country='FI'
        )
        self.payment = Payment(
            order_number='12345678',
            contact=self.contact,
            success_url='https://www.esimerkkikauppa.fi/sv/success',
            failure_url='https://www.esimerkkikauppa.fi/sv/failure',
            notification_url='https://www.esimerkkikauppa.fi/sv/success'
        )

    def test_sets_order_number(self):
        assert self.payment.order_number == '12345678'

    def test_sets_contact(self):
        assert self.payment.contact is self.contact

    def test_sets_success_url(self):
        assert self.payment.success_url == \
            'https://www.esimerkkikauppa.fi/sv/success'

    def test_sets_failure_url(self):
        assert self.payment.failure_url == \
            'https://www.esimerkkikauppa.fi/sv/failure'

    def test_sets_notification_url(self):
        assert self.payment.notification_url == \
            'https://www.esimerkkikauppa.fi/sv/success'

    def test_product_list_is_empty(self):
        assert len(self.payment.products) == 0

    def test_reference_number_is_none_by_default(self):
        assert self.payment.reference_number is None

    def test_description_is_none_by_default(self):
        assert self.payment.description is None

    def test_currency_is_euro_by_default(self):
        assert self.payment.currency == 'EUR'

    def test_locale_is_finnish_by_default(self):
        assert self.payment.locale == 'fi_FI'

    def test_vat_is_included_by_default(self):
        assert self.payment.include_vat

    def test_pending_url_is_none_by_default(self):
        assert self.payment.pending_url is None

    def test_unsupported_currency_raises_value_error(self):
        with raises(ValueError) as exc_info:
            self.payment.currency = 'USD'
        assert exc_info.value.message == \
            'Currently EUR is the only supported currency.'

    def test_locale_can_be_finnish(self):
        self.payment.locale = 'fi_FI'
        assert self.payment.locale == 'fi_FI'

    def test_locale_can_be_swedish(self):
        self.payment.locale = 'sv_SE'
        assert self.payment.locale == 'sv_SE'

    def test_locale_can_be_english(self):
        self.payment.locale = 'en_US'
        assert self.payment.locale == 'en_US'

    def test_unsupported_locale_raises_value_error(self):
        with raises(ValueError) as exc_info:
            self.payment.locale = 'de_DE'
        assert exc_info.value.message == \
            "Given locale is not supported: 'de_DE'"

    def test_json(self):
        assert self.payment.json == {
            'orderNumber': '12345678',
            'referenceNumber': None,
            'description': None,
            'currency': 'EUR',
            'locale': 'fi_FI',
            'urlSet': {
                'success': 'https://www.esimerkkikauppa.fi/sv/success',
                'pending': None,
                'failure': 'https://www.esimerkkikauppa.fi/sv/failure',
                'notification': 'https://www.esimerkkikauppa.fi/sv/success'
            },
            'orderDetails': {
                'includeVat': '1',
                'contact': self.contact.json,
                'products': []
            }
        }


class TestPaymentWithAllParameters(object):
    def setup_method(self, method):
        self.contact = Contact(
            first_name='Matti',
            last_name='Meikäläinen',
            email='matti.meikalainen@gmail.com',
            street='Esimerkkikatu 123',
            postal_code='01234',
            postal_office='Helsinki',
            country='FI'
        )
        self.payment = Payment(
            order_number='12345678',
            contact=self.contact,
            reference_number='12345-12345-12345',
            description='Esimerkkimaksun kuvaus',
            currency='EUR',
            locale='sv_SE',
            include_vat=False,
            success_url='https://www.esimerkkikauppa.fi/sv/success',
            pending_url='https://www.esimerkkikauppa.fi/sv/pending',
            failure_url='https://www.esimerkkikauppa.fi/sv/failure',
            notification_url='https://www.esimerkkikauppa.fi/sv/success'
        )
        self.payment.products.append(
            Product(
                title='Esimerkkituote',
                price='19.90',
                vat='23.00'
            )
        )

    def test_sets_reference_number(self):
        assert self.payment.reference_number == '12345-12345-12345'

    def test_sets_description(self):
        assert self.payment.description == 'Esimerkkimaksun kuvaus'

    def test_sets_currency(self):
        assert self.payment.currency == 'EUR'

    def test_sets_locale(self):
        assert self.payment.locale == 'sv_SE'

    def test_sets_include_vat(self):
        assert not self.payment.include_vat

    def test_sets_pending_url(self):
        assert self.payment.pending_url == \
            'https://www.esimerkkikauppa.fi/sv/pending'

    def test_json(self):
        assert self.payment.json == {
            'orderNumber': '12345678',
            'referenceNumber': '12345-12345-12345',
            'description': 'Esimerkkimaksun kuvaus',
            'currency': 'EUR',
            'locale': 'sv_SE',
            'urlSet': {
                'success': 'https://www.esimerkkikauppa.fi/sv/success',
                'failure': 'https://www.esimerkkikauppa.fi/sv/failure',
                'pending': 'https://www.esimerkkikauppa.fi/sv/pending',
                'notification': 'https://www.esimerkkikauppa.fi/sv/success'
            },
            'orderDetails': {
                'includeVat': '0',
                'contact': self.contact.json,
                'products': [self.payment.products[0].json]
            }
        }


class MockPayment(object):
    def __init__(self, order_number='12345'):
        self.order_number = order_number

    @property
    def json(self):
        return {
            'orderNumber': self.order_number
        }


class TestClient(object):
    def test_defaults_to_merchant_test_account(self):
        client = Client()
        assert client.session.auth == \
            ('13466', '6pKF4jkv97zmqBJ3ZL8gUw5DfT2NMQ')

    def test_custom_merchant_credentials(self):
        client = Client(merchant_id='12345', merchant_secret='secret')
        assert client.session.auth == ('12345', 'secret')

    def test_request_content_type_is_json(self):
        client = Client()
        assert client.session.headers['Content-Type'] == 'application/json'

    def test_request_accepts_json(self):
        client = Client()
        assert client.session.headers['Accept'] == 'application/json'

    def test_request_defines_api_version(self):
        client = Client()
        assert client.session.headers['X-Verkkomaksut-Api-Version'] == '1'

    def test_successful_payment_creation(self):
        response = requests.Response()
        response._content = """{
  "orderNumber": "12345",
  "token": "secret_token",
  "url": "https://payment.verkkomaksut.fi/payment/load/token/secret_token"
}"""
        response.status_code = requests.codes.created

        client = Client()
        flexmock(client.session)
        client.session \
            .should_receive('post') \
            .with_args(
                'https://payment.verkkomaksut.fi/api-payment/create',
                data='{"orderNumber": "12345"}',
            ) \
            .and_return(response)

        payment = MockPayment(order_number='12345')
        assert client.create_payment(payment) == {
            'order_number': '12345',
            'token': 'secret_token',
            'url': 'https://payment.verkkomaksut.fi/payment/load/token/'
                   'secret_token'
        }

    def test_payment_creation_failure(self):
        response = requests.Response()
        response._content = """{
  "errorCode": "invalid-order-number",
  "errorMessage": "Missing or invalid order number"
}"""
        response.status_code = requests.codes.bad_request

        client = Client()
        flexmock(client.session)
        client.session \
            .should_receive('post') \
            .with_args(
                'https://payment.verkkomaksut.fi/api-payment/create',
                data='{"orderNumber": "12345"}',
            ) \
            .and_return(response)

        payment = MockPayment()
        with raises(VerkkomaksutException) as exc_info:
            client.create_payment(payment)

        assert exc_info.value.code == 'invalid-order-number'
        assert exc_info.value.message == 'Missing or invalid order number'

    def test_calculate_payment_receipt_hash(self):
        client = Client()
        hash_ = client._calculate_payment_receipt_hash(
            '15153',
            '1176557554',
            '012345ABCDE',
            '1'
        )
        assert hash_ == '555E0C0DE304938AACA5D594DB72F315'

    def test_validate_payment_receipt_parameters_ok(self):
        client = Client()
        flexmock(client) \
            .should_receive('_calculate_payment_receipt_hash') \
            .with_args('order_number', 'timestamp', 'paid', 'method') \
            .and_return('authcode')
        assert client._validate_payment_receipt_parameters(
            'authcode', 'order_number', 'timestamp', 'paid', 'method')

    def test_validate_payment_receipt_parameters_fail(self):
        client = Client()
        flexmock(client) \
            .should_receive('_calculate_payment_receipt_hash') \
            .with_args('order_number', 'timestamp', 'paid', 'method') \
            .and_return('not_ok')
        assert not client._validate_payment_receipt_parameters(
            'authcode', 'order_number', 'timestamp', 'paid', 'method')
