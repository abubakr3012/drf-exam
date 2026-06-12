ТЗ: Системаи бонкии таълимӣ бо DRF — танҳо дар доираи Week 1
Номи проект
MiniBank Mobile Wallet API

Ё:

Alif-like Wallet API
Мақсад

Сохтани REST API барои системаи бонкии таълимӣ, ки ба mobile wallet монанд аст.

Система бояд дошта бошад:

1. Истифодабарандаҳо
2. Профили клиент
3. Ҳамён / суратҳисоб
4. Корт
5. Транзаксияҳо
6. Категорияҳои пардохт
7. Провайдерҳо
8. Пардохтҳо
9. Favorite payments
10. Notifications

Ин проект танҳо аз мавзуҳои Week 1 истифода мекунад:

URL
API
JSON
HTTP / HTTPS
DRF
CRUD
FBV
Serializers
Nested serializers
Custom validation
to_representation
Filtering
Search
Pagination
APIView
GenericAPIView
ViewSets
Swagger / OpenAPI
Postman
Чизҳое, ки ба Week 1 дохил НЕСТАНД

Инҳоро ҳоло намегирем:

JWT Authentication
OTP
Permissions
Celery
Redis
Real SMS
Real bank integration
Real card payment
Webhook
Anti-fraud
KYC-и пурраи воқеӣ
QR payment
PDF receipt

Яъне проект реалистичный менамояд, вале аз ҷиҳати техникӣ танҳо Week 1 мебошад.

1. Моделҳои система
1. User

Метавонед default User-и Django-ро истифода баред.

Fields
id
username
first_name
last_name
email
password
date_joined
is_active
Барои чӣ лозим?

Барои нигоҳ доштани маълумоти асосии клиент.

2. CustomerProfile

Профили клиент.

Fields
id
user
phone_number
birth_date
address
passport_number
created_at
updated_at
Relationship
User 1 --- 1 CustomerProfile
CRUD
GET    /api/profiles/
POST   /api/profiles/
GET    /api/profiles/{id}/
PATCH  /api/profiles/{id}/
DELETE /api/profiles/{id}/
Week 1 topics
CRUD
Serializer
Nested object
Custom validation
ViewSet
3. Wallet

Ҳамёни мобилӣ ё суратҳисоби клиент.

Fields
id
user
wallet_number
balance
currency
status
created_at
updated_at
currency
TJS
USD
RUB
status
ACTIVE
BLOCKED
CLOSED
Relationship
User 1 --- 1 Wallet
Қоидаи муҳим

balance бояд read_only бошад.

Яъне user набояд чунин кунад:

{
  "balance": 100000
}

Баланс танҳо тавассути transaction тағйир меёбад.

CRUD
GET    /api/wallets/
POST   /api/wallets/
GET    /api/wallets/{id}/
PATCH  /api/wallets/{id}/
DELETE /api/wallets/{id}/
Week 1 topics
CRUD
Serializer
Custom validation
to_representation
ViewSet
4. BankCard

Корти бонкӣ.

Fields
id
user
card_holder
masked_pan
card_type
expire_month
expire_year
status
created_at
card_type
VISA
MASTERCARD
KORTI_MILLI
OTHER
status
ACTIVE
BLOCKED
EXPIRED
Намунаи masked_pan
**** **** **** 1234
Relationship
User 1 --- many BankCard
CRUD
GET    /api/cards/
POST   /api/cards/
GET    /api/cards/{id}/
PATCH  /api/cards/{id}/
DELETE /api/cards/{id}/
Validation
expire_month бояд аз 1 то 12 бошад
expire_year набояд гузашта бошад
masked_pan бояд холӣ набошад
card_holder бояд холӣ набошад
Week 1 topics
CRUD
Serializer
Custom validation
ViewSet
5. Transaction

Модели асосии системаи бонкӣ.

Fields
id
sender_wallet
receiver_wallet
transaction_type
amount
commission
total_amount
currency
status
description
created_at
updated_at
transaction_type    
TOP_UP
TRANSFER
PAYMENT
WITHDRAW
status
PENDING
SUCCESS
FAILED
CANCELLED
Relationship
Wallet 1 --- many Transaction as sender
Wallet 1 --- many Transaction as receiver
Қоидаи муҳим

Transaction одатан DELETE ва UPDATE намешавад.

Барои Week 1 кофӣ аст:

GET list
GET detail
POST special actions
Endpoints
GET  /api/transactions/
GET  /api/transactions/{id}/
POST /api/transactions/top-up/
POST /api/transactions/transfer/
POST /api/transactions/withdraw/
Week 1 topics
APIView
GenericAPIView
Serializer
Nested serializer
Custom validation
Filtering
Search
Pagination
to_representation
6. PaymentCategory

Категорияи пардохт.

Fields
id
name
description
is_active
created_at
Намунаҳо
Мобилӣ
Интернет
Коммуналӣ
Такси
Телевизион
Дӯконҳо
CRUD
GET    /api/payment-categories/
POST   /api/payment-categories/
GET    /api/payment-categories/{id}/
PATCH  /api/payment-categories/{id}/
DELETE /api/payment-categories/{id}/
Week 1 topics
Simple CRUD using Rest FBV
Serializer
JSON response
HTTP methods

Ин моделро махсус бо Function-Based View сохтан мумкин аст, то мавзӯи Day 1 иҷро шавад.

7. ServiceProvider

Провайдери хизматрасонӣ.

Fields
id
category
name
account_mask
min_amount
max_amount
commission_percent
is_active
created_at
Намунаҳо
Tcell
Megafon
Babilon
ZET Mobile
Dushanbe City Internet
Relationship
PaymentCategory 1 --- many ServiceProvider
CRUD
GET    /api/providers/
POST   /api/providers/
GET    /api/providers/{id}/
PATCH  /api/providers/{id}/
DELETE /api/providers/{id}/
Week 1 topics
CRUD
Nested serializer
Filtering
Search
ViewSet
8. Payment

Пардохти хизматрасонӣ.

Fields
id
user
wallet
provider
account_number
amount
commission
total_amount
status
transaction
created_at
status
PENDING
SUCCESS
FAILED
CANCELLED
Relationship
User 1 --- many Payment
Wallet 1 --- many Payment
ServiceProvider 1 --- many Payment
Payment 1 --- 1 Transaction
Endpoints
GET  /api/payments/
GET  /api/payments/{id}/
POST /api/payments/
Week 1 topics
APIView
Serializer
Nested serializer
Custom validation
Filtering
Search
Pagination
9. FavoritePayment

Пардохти дӯстдошта.

Fields
id
user
provider
title
account_number
created_at
Намуна
Телефони ман
Интернети хона
Телефони модар
Relationship
User 1 --- many FavoritePayment
ServiceProvider 1 --- many FavoritePayment
CRUD
GET    /api/favorites/
POST   /api/favorites/
GET    /api/favorites/{id}/
PATCH  /api/favorites/{id}/
DELETE /api/favorites/{id}/
Week 1 topics
CRUD
Serializer
Nested serializer
ViewSet
10. Notification

Огоҳинома барои клиент.

Fields
id
user
title
message
notification_type
is_read
created_at
notification_type
TRANSACTION
PAYMENT
SYSTEM
CARD
Relationship
User 1 --- many Notification
Endpoints
GET   /api/notifications/
GET   /api/notifications/{id}/
PATCH /api/notifications/{id}/
DELETE /api/notifications/{id}/
PATCH /api/notifications/{id}/mark-as-read/
Week 1 topics
CRUD
APIView custom action
Serializer
Filtering
Pagination
2. Relationship-и умумӣ
User 1 --- 1 CustomerProfile
User 1 --- 1 Wallet
User 1 --- many BankCard
User 1 --- many Payment
User 1 --- many FavoritePayment
User 1 --- many Notification

Wallet 1 --- many Transaction as sender
Wallet 1 --- many Transaction as receiver

PaymentCategory 1 --- many ServiceProvider
ServiceProvider 1 --- many Payment
ServiceProvider 1 --- many FavoritePayment

Payment 1 --- 1 Transaction
3. CRUD-ҳои лозим
CRUD-и пурра
CustomerProfile CRUD
Wallet CRUD
BankCard CRUD
PaymentCategory CRUD
ServiceProvider CRUD
FavoritePayment CRUD
Notification CRUD
CRUD-и маҳдуд
Transaction:
    GET list
    GET detail
    POST top-up
    POST transfer
    POST withdraw

Payment:
    GET list
    GET detail
    POST create payment

Сабаб: transaction ва payment баъди иҷро шудан набояд оддӣ edit/delete шаванд.

4. Endpoint-ҳои пурраи система
Profiles
GET    /api/profiles/
POST   /api/profiles/
GET    /api/profiles/{id}/
PATCH  /api/profiles/{id}/
DELETE /api/profiles/{id}/
Wallets
GET    /api/wallets/
POST   /api/wallets/
GET    /api/wallets/{id}/
PATCH  /api/wallets/{id}/
DELETE /api/wallets/{id}/
Cards
GET    /api/cards/
POST   /api/cards/
GET    /api/cards/{id}/
PATCH  /api/cards/{id}/
DELETE /api/cards/{id}/
Transactions
GET  /api/transactions/
GET  /api/transactions/{id}/
POST /api/transactions/top-up/
POST /api/transactions/transfer/
POST /api/transactions/withdraw/
Payment Categories
GET    /api/payment-categories/
POST   /api/payment-categories/
GET    /api/payment-categories/{id}/
PATCH  /api/payment-categories/{id}/
DELETE /api/payment-categories/{id}/
Providers
GET    /api/providers/
POST   /api/providers/
GET    /api/providers/{id}/
PATCH  /api/providers/{id}/
DELETE /api/providers/{id}/
Payments
GET  /api/payments/
GET  /api/payments/{id}/
POST /api/payments/
Favorites
GET    /api/favorites/
POST   /api/favorites/
GET    /api/favorites/{id}/
PATCH  /api/favorites/{id}/
DELETE /api/favorites/{id}/
Notifications
GET    /api/notifications/
GET    /api/notifications/{id}/
PATCH  /api/notifications/{id}/
DELETE /api/notifications/{id}/
PATCH  /api/notifications/{id}/mark-as-read/
5. Кадом View барои кадом қисм?
Function-Based View — Day 1

Барои CRUD-и содда:

PaymentCategory CRUD

Мақсад: нишон додани @api_view.

ViewSet — Day 3

Барои CRUD-и стандартӣ:

CustomerProfileViewSet
WalletViewSet
BankCardViewSet
ServiceProviderViewSet
FavoritePaymentViewSet
NotificationViewSet
GenericAPIView — Day 3

Барои list/create бо logic:

TransactionListAPIView
PaymentListCreateAPIView
APIView — Day 3

Барои амалиёти махсус:

TopUpAPIView
TransferAPIView
WithdrawAPIView
MarkNotificationAsReadAPIView
6. Serializer-ҳои лозим
UserShortSerializer

Барои nested output.

id
username
first_name
last_name
email
CustomerProfileSerializer
id
user
phone_number
birth_date
address
passport_number
created_at
updated_at
Nested output
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "ali",
    "first_name": "Ali",
    "last_name": "Rahimov"
  },
  "phone_number": "+992900000000",
  "address": "Dushanbe"
}
WalletSerializer
id
user
wallet_number
balance
currency
status
created_at
updated_at
Read only fields
balance
wallet_number
created_at
updated_at
Nested output
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "ali"
  },
  "wallet_number": "992000001",
  "balance": "1500.00",
  "currency": "TJS",
  "status": "ACTIVE"
}
BankCardSerializer
id
user
card_holder
masked_pan
card_type
expire_month
expire_year
status
created_at
Validation
expire_month: 1-12
expire_year: набояд гузашта бошад
masked_pan: бояд format-и **** **** **** 1234 дошта бошад
PaymentCategorySerializer
id
name
description
is_active
created_at
ServiceProviderSerializer
id
category
name
account_mask
min_amount
max_amount
commission_percent
is_active
created_at
Nested output
{
  "id": 1,
  "name": "Tcell",
  "category": {
    "id": 1,
    "name": "Мобилӣ"
  },
  "min_amount": "1.00",
  "max_amount": "1000.00",
  "commission_percent": "0.00",
  "is_active": true
}
TransactionSerializer
id
sender_wallet
receiver_wallet
transaction_type
amount
commission
total_amount
currency
status
description
created_at
Nested output
{
  "id": 15,
  "transaction_type": "TRANSFER",
  "amount": "100.00",
  "commission": "1.00",
  "total_amount": "101.00",
  "currency": "TJS",
  "status": "SUCCESS",
  "sender_wallet": {
    "wallet_number": "992000001",
    "owner": "ali"
  },
  "receiver_wallet": {
    "wallet_number": "992000002",
    "owner": "vali"
  },
  "description": "Transfer to friend"
}
TopUpSerializer

Барои POST /api/transactions/top-up/.

wallet_id
amount
description
Request example
{
  "wallet_id": 1,
  "amount": "200.00",
  "description": "Top up from cash desk"
}
TransferSerializer

Барои POST /api/transactions/transfer/.

sender_wallet_id
receiver_wallet_number
amount
description
Request example
{
  "sender_wallet_id": 1,
  "receiver_wallet_number": "992000002",
  "amount": "100.00",
  "description": "For lunch"
}
PaymentSerializer
id
user
wallet
provider
account_number
amount
commission
total_amount
status
transaction
created_at
Request example
{
  "user": 1,
  "wallet": 1,
  "provider": 2,
  "account_number": "900000000",
  "amount": "50.00"
}
FavoritePaymentSerializer
id
user
provider
title
account_number
created_at
NotificationSerializer
id
user
title
message
notification_type
is_read
created_at
7. Custom validation
Wallet validation
currency бояд TJS, USD ё RUB бошад
status бояд ACTIVE, BLOCKED ё CLOSED бошад
Card validation
expire_month бояд аз 1 то 12 бошад
expire_year набояд гузашта бошад
masked_pan бояд холӣ набошад
card_holder бояд холӣ набошад
Transaction validation
amount бояд аз 0 калон бошад
wallet бояд ACTIVE бошад
sender_wallet ва receiver_wallet якхела набошанд
sender balance бояд кофӣ бошад
receiver_wallet бояд вуҷуд дошта бошад
Payment validation
provider бояд active бошад
amount бояд аз min_amount кам набошад
amount бояд аз max_amount зиёд набошад
wallet balance бояд кофӣ бошад
account_number набояд холӣ бошад
FavoritePayment validation
title набояд холӣ бошад
account_number набояд холӣ бошад
provider бояд active бошад
8. to_representation

Дар Week 1 to_representation() ҳаст, бинобар ин дар система истифода мешавад.

Барои Wallet

Database:

balance = 1500.00
currency = TJS

Response:

{
  "balance": "1500.00 TJS"
}
Барои Transaction

Database:

transaction_type = TRANSFER
status = SUCCESS

Response:

{
  "transaction_type": "Интиқоли пул",
  "status": "Иҷро шуд",
  "amount": "100.00 TJS"
}
Барои Notification

Database:

is_read = false

Response:

{
  "is_read": false,
  "status_text": "Хонда нашудааст"
}
9. Filtering
Transactions filtering
GET /api/transactions/?status=SUCCESS
GET /api/transactions/?transaction_type=TRANSFER
GET /api/transactions/?currency=TJS
GET /api/transactions/?sender_wallet=1
GET /api/transactions/?receiver_wallet=2
Payments filtering
GET /api/payments/?status=SUCCESS
GET /api/payments/?provider=1
GET /api/payments/?wallet=1
Providers filtering
GET /api/providers/?category=1
GET /api/providers/?is_active=true
Cards filtering
GET /api/cards/?status=ACTIVE
GET /api/cards/?card_type=VISA
Notifications filtering
GET /api/notifications/?is_read=false
GET /api/notifications/?notification_type=TRANSACTION
10. Search queries
Search providers
GET /api/providers/?search=tcell
GET /api/providers/?search=internet

Search fields:

name
category__name
Search transactions
GET /api/transactions/?search=992000001
GET /api/transactions/?search=lunch

Search fields:

description
sender_wallet__wallet_number
receiver_wallet__wallet_number
Search payments
GET /api/payments/?search=900000000
GET /api/payments/?search=tcell

Search fields:

account_number
provider__name
Search cards
GET /api/cards/?search=1234
GET /api/cards/?search=VISA

Search fields:

masked_pan
card_holder
card_type
11. Pagination

Pagination бояд барои list endpoint-ҳо бошад.

Pagination endpoint-ҳо
/api/profiles/
/api/wallets/
/api/cards/
/api/transactions/
/api/providers/
/api/payments/
/api/favorites/
/api/notifications/
Custom pagination response
{
  "count": 120,
  "total_pages": 12,
  "current_page": 1,
  "page_size": 10,
  "next": "http://localhost:8000/api/transactions/?page=2",
  "previous": null,
  "results": []
}
12. Business logic дар доираи Week 1
Top up wallet

Endpoint:

POST /api/transactions/top-up/

Logic:

1. Wallet гирифта мешавад
2. Amount санҷида мешавад
3. Агар amount > 0 бошад, balance зиёд мешавад
4. Transaction бо type TOP_UP сохта мешавад
5. Notification сохта мешавад
Transfer money

Endpoint:

POST /api/transactions/transfer/

Logic:

1. Sender wallet гирифта мешавад
2. Receiver wallet бо wallet_number ёфт мешавад
3. Amount санҷида мешавад
4. Balance санҷида мешавад
5. Аз sender balance кам мешавад
6. Ба receiver balance зиёд мешавад
7. Transaction бо type TRANSFER сохта мешавад
8. Notification барои sender ва receiver сохта мешавад
Pay service provider

Endpoint:

POST /api/payments/

Logic:

1. User provider интихоб мекунад
2. Account number ворид мекунад
3. Amount ворид мекунад
4. Provider active буданаш санҷида мешавад
5. Min/max amount санҷида мешавад
6. Balance санҷида мешавад
7. Payment сохта мешавад
8. Transaction бо type PAYMENT сохта мешавад
9. Balance кам мешавад
10. Notification сохта мешавад
Mark notification as read

Endpoint:

PATCH /api/notifications/{id}/mark-as-read/

Logic:

1. Notification ёфт мешавад
2. is_read = true мешавад
3. Response бармегардад
13. JSON request/response examples
Create wallet
Request
{
  "user": 1,
  "currency": "TJS",
  "status": "ACTIVE"
}
Response
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "ali"
  },
  "wallet_number": "992000001",
  "balance": "0.00 TJS",
  "currency": "TJS",
  "status": "ACTIVE"
}
Transfer
Request
{
  "sender_wallet_id": 1,
  "receiver_wallet_number": "992000002",
  "amount": "100.00",
  "description": "Transfer to friend"
}
Response
{
  "id": 10,
  "transaction_type": "Интиқоли пул",
  "amount": "100.00 TJS",
  "commission": "0.00 TJS",
  "total_amount": "100.00 TJS",
  "status": "Иҷро шуд",
  "sender_wallet": {
    "wallet_number": "992000001",
    "owner": "ali"
  },
  "receiver_wallet": {
    "wallet_number": "992000002",
    "owner": "vali"
  }
}
Payment
Request
{
  "user": 1,
  "wallet": 1,
  "provider": 1,
  "account_number": "900000000",
  "amount": "50.00"
}
Response
{
  "id": 5,
  "provider": {
    "id": 1,
    "name": "Tcell",
    "category": {
      "id": 1,
      "name": "Мобилӣ"
    }
  },
  "account_number": "900000000",
  "amount": "50.00 TJS",
  "commission": "0.00 TJS",
  "total_amount": "50.00 TJS",
  "status": "SUCCESS"
}
14. URL, API, JSON, HTTP дар проект
URL

Намуна:

/api/wallets/
/api/transactions/
/api/payments/
/api/providers/
API

Ин project REST API мебошад, ки frontend ё mobile app метавонад истифода барад.

JSON

Ҳама request ва response бо JSON мешаванд.

HTTP methods
GET     гирифтани маълумот
POST    сохтани маълумот
PATCH   тағйир додани қисман маълумот
DELETE  нест кардани маълумот
HTTP status codes
200 OK
201 Created
400 Bad Request
404 Not Found
500 Server Error
15. DRF vs Django дар ин проект
Django

Django асосан барои:

models
database
admin panel
views
templates
DRF

DRF барои API:

serializers
JSON response
API views
ViewSets
Pagination
Filtering
Swagger
Browsable API
Чаро DRF лозим аст?

Чун mobile banking frontend ё mobile app HTML намехоҳад. Он JSON API мехоҳад.

16. Swagger / OpenAPI Docs

Барои Day 4 ҳатмӣ.

Tools

Яке аз инҳо:

drf-spectacular

ё:

drf-yasg
Endpoint-ҳо
/api/schema/
/api/docs/
/api/redoc/
Дар Swagger бояд бошад
Profiles
Wallets
Cards
Transactions
Payment Categories
Providers
Payments
Favorites
Notifications
17. Postman test plan
Test 1: Create profile
POST /api/profiles/
Test 2: Create wallet
POST /api/wallets/
Test 3: Top up wallet
POST /api/transactions/top-up/
Test 4: Create second wallet
POST /api/wallets/
Test 5: Transfer money
POST /api/transactions/transfer/
Test 6: Get transactions
GET /api/transactions/
Test 7: Filter transactions
GET /api/transactions/?transaction_type=TRANSFER
Test 8: Search providers
GET /api/providers/?search=tcell
Test 9: Pagination
GET /api/transactions/?page=1
Test 10: Swagger
GET /api/docs/
18. Структураи проект
minibank/
    config/
        settings.py
        urls.py

    apps/
        customers/
            models.py
            serializers.py
            views.py
            urls.py

        wallets/
            models.py
            serializers.py
            views.py
            urls.py

        transactions/
            models.py
            serializers.py
            views.py
            urls.py

        payments/
            models.py
            serializers.py
            views.py
            urls.py

        notifications/
            models.py
            serializers.py
            views.py
            urls.py

        common/
            pagination.py
19. Тақсимоти project аз рӯйи рӯзҳои Week 1
Day 1
URL
API
JSON
HTTP / HTTPS
DRF introduction
Simple CRUD using FBV
Postman

Дар project:

PaymentCategory CRUD бо FBV
Postman test
GET / POST / PATCH / DELETE
JSON request/response
Day 2
Serializers
Nested objects
Custom validation
to_representation

Дар project:

WalletSerializer
TransactionSerializer
PaymentSerializer
Nested user дар wallet
Nested provider дар payment
Validation барои amount ва balance
to_representation барои status ва currency
Day 3
Filtering
Search
Pagination
APIView
GenericAPIView
ViewSets

Дар project:

Transaction filtering
Provider search
Custom pagination
TransferAPIView
PaymentListCreateAPIView
WalletViewSet
CardViewSet
Day 4
Swagger/OpenAPI
drf-yasg / drf-spectacular
Build API with CRUD, nested serializers, filtering

Дар project:

Swagger docs
Mobile Wallet API final demo
CRUD + nested + filter + search + pagination
20. Версияи ниҳоии assignment барои имтиҳон
Task

Сохтани REST API барои MiniBank Mobile Wallet.

API бояд дошта бошад:

CustomerProfile
Wallet
BankCard
Transaction
PaymentCategory
ServiceProvider
Payment
FavoritePayment
Notification
Ҳатмӣ
1. CRUD барои profile, wallet, card, category, provider, favorite, notification
2. Transaction list/detail
3. Top up wallet
4. Transfer money between wallets
5. Pay service provider
6. Nested serializers
7. Custom validation
8. to_representation
9. Filtering
10. Search
11. Custom pagination
12. APIView
13. GenericAPIView
14. ViewSets
15. Swagger/OpenAPI docs
16. Postman testing
Набояд дохил шавад
JWT
OTP
Permissions
Real payment gateway
Real SMS
Celery
Redis
Webhook
Anti-fraud
21. Баҳо додан
60%
Models дуруст
CRUD кор мекунад
JSON request/response дуруст
Postman test
75%
Serializers
Nested serializers
Custom validation
90%
Filtering
Search
Pagination
APIView
GenericAPIView
ViewSets
Swagger
100%
Transfer logic дуруст
Payment logic дуруст
Balance readonly
Transaction history
to_representation
Clean API structure