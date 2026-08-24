# Source: https://docs.stripe.com/api/checkout/sessions

# [Checkout Sessions](/api/checkout/sessions)

Ask about this section

Copy for LLMView as Markdown

A Checkout Session represents your customer’s session as they pay for one-time purchases or subscriptions through [Checkout](/payments/checkout) or [Payment Links](/payments/payment-links). We recommend creating a new Session each time your customer attempts to pay.

Once payment is successful, the Checkout Session will contain a reference to the [Customer](/api/customers), and either the successful [PaymentIntent](/api/payment_intents) or an active [Subscription](/api/subscriptions).

You can create a Checkout Session on your server and redirect to its URL to begin Checkout.

Related guide: [Checkout quickstart](/checkout/quickstart)

Was this section helpful?YesNo

Create a Checkout Session

POST/v1/checkout/sessions

Update a Checkout Session

POST/v1/checkout/sessions/:id

Retrieve a Checkout Session

GET/v1/checkout/sessions/:id

Retrieve a Checkout Session's line items

GET/v1/checkout/sessions/:id/line\_items

List all Checkout Sessions

GET/v1/checkout/sessions

Expire a Checkout Session

POST/v1/checkout/sessions/:id/expire

# [The Checkout Session object](/api/checkout/sessions/object)

Ask about this section

Copy for LLMView as Markdown

### Attributes

* #### idstring

  Unique identifier for the object.
* #### automatic\_taxobject

  Details on the state of automatic tax for the session, including the status of the latest tax calculation.

  Show child attributes
* #### client\_reference\_idnullable string

  A unique string to reference the Checkout Session. This can be a customer ID, a cart ID, or similar, and can be used to reconcile the Session with your internal systems.
* #### currencynullable enum

  Three-letter [ISO currency code](https://www.iso.org/iso-4217-currency-codes.html), in lowercase. Must be a [supported currency](https://stripe.com/docs/currencies).
* #### customernullable stringExpandable

  The ID of the customer for this Session. For Checkout Sessions in `subscription` mode or Checkout Sessions with `customer_creation` set as `always` in `payment` mode, Checkout will create a new customer object based on information provided during the payment flow unless an existing customer was provided when the Session was created.
* #### customer\_emailnullable string

  If provided, this value will be used when the Customer object is created. If not provided, customers will be asked to enter their email address. Use this parameter to prefill customer data if you already have an email on file. To access information about the customer once the payment flow is complete, use the `customer` attribute.
* #### line\_itemsnullable objectExpandable

  The line items purchased by the customer.

  Show child attributes
* #### metadatanullable object

  Set of [key-value pairs](/api/metadata) that you can attach to an object. This can be useful for storing additional information about the object in a structured format.
* #### modeenum

  The mode of the Checkout Session.

  Possible enum values

  |  |
  | --- |
  | `payment`  Accept one-time payments for cards, iDEAL, and more. |
  | `setup`  Save payment details to charge your customers later. |
  | `subscription`  Use Stripe Billing to set up fixed-price subscriptions. |
* #### payment\_intentnullable stringExpandable

  The ID of the PaymentIntent for Checkout Sessions in `payment` mode. You can’t confirm or cancel the PaymentIntent for a Checkout Session. To cancel, [expire the Checkout Session](/api/checkout/sessions/expire) instead.
* #### payment\_statusenum

  The payment status of the Checkout Session, one of `paid`, `unpaid`, or `no_payment_required`. You can use this value to decide when to fulfill your customer’s order.

  Possible enum values

  |  |
  | --- |
  | `no_payment_required`  The Checkout Session is in `setup` mode and doesn’t require a payment at this time, or the Session uses a billing cycle anchor with no proration and payment will be collected at the anchor date. |
  | `paid`  The payment funds are available in your account. For subscriptions with a free trial, this indicates that the $0 trial invoice has been successfully processed. |
  | `unpaid`  The payment funds are not yet available in your account. |
* #### return\_urlnullable string

  Applies to Checkout Sessions with `ui_mode: embedded_page` or `ui_mode: elements`. The URL to redirect your customer back to after they authenticate or cancel their payment on the payment method’s app or site.
* #### statusnullable enum

  The status of the Checkout Session, one of `open`, `complete`, or `expired`.

  Possible enum values

  |  |
  | --- |
  | `complete`  The checkout session is complete. Payment processing may still be in progress |
  | `expired`  The checkout session has expired. No further processing will occur |
  | `open`  The checkout session is still in progress. Payment processing has not started |
* #### success\_urlnullable string

  The URL the customer will be directed to after the payment or subscription creation is successful.
* #### ui\_modenullable enum

  The UI mode of the Session. Defaults to `hosted_page`.

  Possible enum values

  |  |
  | --- |
  | `elements`  The Checkout Session is displayed using [Checkout elements](https://docs.stripe.com/checkout/custom/quickstart) on your website. |
  | `embedded_page`  The Checkout Session is displayed as an embedded form on your website. |
  | `hosted_page`  The Checkout Session is displayed on a hosted page that customers get redirected to. |
* #### urlnullable string

  The URL to the Checkout Session. Applies to Checkout Sessions with `ui_mode: hosted_page`. Redirect customers to this URL to take them to Checkout. If you’re using [Custom Domains](/payments/checkout/custom-domains), the URL will use your subdomain. Otherwise, it’ll use `checkout.stripe.com.` This value is only present when the session is active.

### More attributes Expand all

* #### objectstring
* #### adaptive\_pricingnullable object
* #### after\_expirationnullable object
* #### allow\_promotion\_codesnullable boolean
* #### amount\_subtotalnullable integer
* #### amount\_totalnullable integer
* #### billing\_address\_collectionnullable enum
* #### branding\_settingsnullable object
* #### cancel\_urlnullable string
* #### client\_secretnullable string
* #### collected\_informationnullable object
* #### consentnullable object
* #### consent\_collectionnullable object
* #### createdtimestamp
* #### currency\_conversionnullable object
* #### custom\_fieldsarray of objects
* #### custom\_textobject
* #### customer\_accountnullable string
* #### customer\_creationnullable enum
* #### customer\_detailsnullable object
* #### discountsnullable array of objects
* #### excluded\_payment\_method\_typesnullable array of strings
* #### expires\_attimestamp
* #### integration\_identifiernullable string
* #### invoicenullable stringExpandable
* #### invoice\_creationnullable object
* #### livemodeboolean
* #### localenullable enum
* #### managed\_paymentsnullable object
* #### name\_collectionnullable object
* #### optional\_itemsnullable array of objectsExpandable
* #### origin\_contextnullable enum
* #### payment\_linknullable stringExpandable
* #### payment\_method\_collectionnullable enum
* #### payment\_method\_configuration\_detailsnullable object
* #### payment\_method\_optionsnullable object
* #### payment\_method\_typesarray of strings
* #### permissionsnullable object
* #### phone\_number\_collectionnullable object
* #### presentment\_detailsnullable object
* #### recovered\_fromnullable string
* #### redirect\_on\_completionnullable enum
* #### saved\_payment\_method\_optionsnullable object
* #### setup\_intentnullable stringExpandable
* #### shipping\_address\_collectionnullable object
* #### shipping\_costnullable object
* #### shipping\_optionsarray of objects
* #### submit\_typenullable enum
* #### subscriptionnullable stringExpandable
* #### tax\_id\_collectionnullable object
* #### total\_detailsnullable object
* #### wallet\_optionsnullable object

The Checkout Session object

```
{



"id": "cs_test_a11YYufWQzNY63zpQ6QSNRQhkUpVph4WRmzW0zWJO2znZKdVujZ0N0S22u",



"object": "checkout.session",



"after_expiration": null,



"allow_promotion_codes": null,



"amount_subtotal": 2198,



"amount_total": 2198,



"automatic_tax": {



"enabled": false,



"liability": null,



"status": null



},



"billing_address_collection": null,



"cancel_url": null,



"client_reference_id": null,



"consent": null,



"consent_collection": null,



"created": 1679600215,



"currency": "usd",



"custom_fields": [],



"custom_text": {



"shipping_address": null,



"submit": null



},



"customer": null,



"customer_creation": "if_required",



"customer_details": null,



"customer_email": null,



"expires_at": 1679686615,



"invoice": null,



"invoice_creation": {



"enabled": false,



"invoice_data": {



"account_tax_ids": null,



"custom_fields": null,



"description": null,



"footer": null,



"issuer": null,



"metadata": {},



"rendering_options": null



}



},



"livemode": false,



"locale": null,



"metadata": {},



"mode": "payment",



"payment_intent": null,



"payment_link": null,



"payment_method_collection": "always",



"payment_method_options": {},



"payment_method_types": [



"card"



],



"payment_status": "unpaid",



"phone_number_collection": {



"enabled": false



},



"recovered_from": null,



"setup_intent": null,



"shipping_address_collection": null,



"shipping_cost": null,



"shipping_details": null,



"shipping_options": [],



"status": "open",



"submit_type": null,



"subscription": null,



"success_url": "https://example.com/success",



"total_details": {



"amount_discount": 0,



"amount_shipping": 0,



"amount_tax": 0



},



"url": "https://checkout.stripe.com/c/pay/cs_test_a11YYufWQzNY63zpQ6QSNRQhkUpVph4WRmzW0zWJO2znZKdVujZ0N0S22u#fidkdWxOYHwnPyd1blpxYHZxWjA0SDdPUW5JbmFMck1wMmx9N2BLZjFEfGRUNWhqTmJ%2FM2F8bUA2SDRySkFdUV81T1BSV0YxcWJcTUJcYW5rSzN3dzBLPUE0TzRKTTxzNFBjPWZEX1NKSkxpNTVjRjN8VHE0YicpJ2N3amhWYHdzYHcnP3F3cGApJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl"



}
```

# [Create a Checkout Session](/api/checkout/sessions/create)

Ask about this section

Copy for LLMView as Markdown

POST /v1/checkout/sessions

Creates a Checkout Session object.

### Parameters

* #### automatic\_taxobject

  Settings for automatic tax lookup for this session and resulting payments, invoices, and subscriptions.

  Show child parameters
* #### client\_reference\_idstring

  A unique string to reference the Checkout Session. This can be a customer ID, a cart ID, or similar, and can be used to reconcile the session with your internal systems.

  The maximum length is 200 characters.
* #### customerstring

  ID of an existing Customer, if one exists. In `payment` mode, the customer’s most recently saved card payment method will be used to prefill the email, name, card details, and billing address on the Checkout page. In `subscription` mode, the customer’s [default payment method](/api/customers/update#update_customer-invoice_settings-default_payment_method) will be used if it’s a card, otherwise the most recently saved card will be used. A valid billing address, billing name and billing email are required on the payment method for Checkout to prefill the customer’s card details.

  If the Customer already has a valid [email](/api/customers/object#customer_object-email) set, the email will be prefilled and not editable in Checkout. If the Customer does not have a valid `email`, Checkout will set the email entered during the session on the Customer.

  If blank for Checkout Sessions in `subscription` mode or with `customer_creation` set as `always` in `payment` mode, Checkout will create a new Customer object based on information provided during the payment flow.

  You can set [`payment_intent_data.setup_future_usage`](/api/checkout/sessions/create#create_checkout_session-payment_intent_data-setup_future_usage) to have Checkout automatically attach the payment method to the Customer you pass in for future reuse.
* #### customer\_emailstring

  If provided, this value will be used when the Customer object is created. If not provided, customers will be asked to enter their email address. Use this parameter to prefill customer data if you already have an email on file. To access information about the customer once a session is complete, use the `customer` field.

  The maximum length is 800 characters.
* #### line\_itemsarray of objectsRequired conditionally

  A list of items the customer is purchasing. Use this parameter to pass one-time or recurring [Prices](/api/prices). The parameter is required for `payment` and `subscription` mode.

  For `payment` mode, there is a maximum of 100 line items, however it is recommended to consolidate line items if there are more than a few dozen.

  For `subscription` mode, there is a maximum of 20 line items with recurring Prices and 20 line items with one-time Prices. Line items with one-time Prices will be on the initial invoice only.

  Show child parameters
* #### metadataobject

  Set of [key-value pairs](/api/metadata) that you can attach to an object. This can be useful for storing additional information about the object in a structured format. Individual keys can be unset by posting an empty value to them. All keys can be unset by posting an empty value to `metadata`.
* #### modeenumRequired

  The mode of the Checkout Session. Pass `subscription` if the Checkout Session includes at least one recurring item.

  Possible enum values

  |  |
  | --- |
  | `payment`  Accept one-time payments for cards, iDEAL, and more. |
  | `setup`  Save payment details to charge your customers later. |
  | `subscription`  Use Stripe Billing to set up fixed-price subscriptions. |
* #### return\_urlstringRequired conditionally

  The URL to redirect your customer back to after they authenticate or cancel their payment on the payment method’s app or site. This parameter is required if `ui_mode` is `embedded_page` or `elements` and redirect-based payment methods are enabled on the session.
* #### success\_urlstringRequired conditionally

  The URL to which Stripe should send customers when payment or setup is complete. This parameter is not allowed if ui\_mode is `embedded_page` or `elements`. If you’d like to use information from the successful Checkout Session on your page, read the guide on [customizing your success page](/payments/checkout/custom-success-page).
* #### ui\_modeenum

  The UI mode of the Session. Defaults to `hosted_page`.

  Possible enum values

  |  |
  | --- |
  | `elements`  The Checkout Session is displayed using [Checkout elements](https://docs.stripe.com/checkout/custom/quickstart) on your website. |
  | `embedded_page`  The Checkout Session is displayed as an embedded form on your website. |
  | `hosted_page`  The Checkout Session is displayed on a hosted page that customers get redirected to. |

### More parameters Expand all

* #### adaptive\_pricingobject
* #### after\_expirationobject
* #### allow\_promotion\_codesboolean
* #### billing\_address\_collectionenum
* #### branding\_settingsobject
* #### cancel\_urlstring
* #### consent\_collectionobject
* #### currencyenumRequired conditionally
* #### custom\_fieldsarray of objects
* #### custom\_textobject
* #### customer\_accountstring
* #### customer\_creationenum
* #### customer\_updateobject
* #### discountsarray of objects
* #### excluded\_payment\_method\_typesarray of enums
* #### expires\_attimestamp
* #### integration\_identifierstring
* #### invoice\_creationobject
* #### localeenum
* #### managed\_paymentsobject
* #### name\_collectionobject
* #### optional\_itemsarray of objects
* #### origin\_contextenum
* #### payment\_intent\_dataobject
* #### payment\_method\_collectionenum
* #### payment\_method\_configurationstring
* #### payment\_method\_dataobject
* #### payment\_method\_optionsobject
* #### payment\_method\_typesarray of enums
* #### permissionsobject
* #### phone\_number\_collectionobject
* #### redirect\_on\_completionenum
* #### saved\_payment\_method\_optionsobject
* #### setup\_intent\_dataobject
* #### shipping\_address\_collectionobject
* #### shipping\_optionsarray of objects
* #### submit\_typeenum
* #### subscription\_dataobject
* #### tax\_id\_collectionobject
* #### wallet\_optionsobject

### Returns

Returns a Checkout Session object.

```
curl https://api.stripe.com/v1/checkout/sessions \



-u "sk_test_BQokikJ...2HlWgH4olfQ2sk_test_EXAMPLE_KEY:" \



--data-urlencode "success_url=https://example.com/success" \



-d "line_items[0][price]={{PRICE_ID}}" \



-d "line_items[0][quantity]=2" \



-d mode=payment
```

Response

```
{



"id": "cs_test_a11YYufWQzNY63zpQ6QSNRQhkUpVph4WRmzW0zWJO2znZKdVujZ0N0S22u",



"object": "checkout.session",



"after_expiration": null,



"allow_promotion_codes": null,



"amount_subtotal": 2198,



"amount_total": 2198,



"automatic_tax": {



"enabled": false,



"liability": null,



"status": null



},



"billing_address_collection": null,



"cancel_url": null,



"client_reference_id": null,



"consent": null,



"consent_collection": null,



"created": 1679600215,



"currency": "usd",



"custom_fields": [],



"custom_text": {



"shipping_address": null,



"submit": null



},



"customer": null,



"customer_creation": "if_required",



"customer_details": null,



"customer_email": null,



"expires_at": 1679686615,



"invoice": null,



"invoice_creation": {



"enabled": false,



"invoice_data": {



"account_tax_ids": null,



"custom_fields": null,



"description": null,



"footer": null,



"issuer": null,



"metadata": {},



"rendering_options": null



}



},



"livemode": false,



"locale": null,



"metadata": {},



"mode": "payment",



"payment_intent": null,



"payment_link": null,



"payment_method_collection": "always",



"payment_method_options": {},



"payment_method_types": [



"card"



],



"payment_status": "unpaid",



"phone_number_collection": {



"enabled": false



},



"recovered_from": null,



"setup_intent": null,



"shipping_address_collection": null,



"shipping_cost": null,



"shipping_details": null,



"shipping_options": [],



"status": "open",



"submit_type": null,



"subscription": null,



"success_url": "https://example.com/success",



"total_details": {



"amount_discount": 0,



"amount_shipping": 0,



"amount_tax": 0



},



"url": "https://checkout.stripe.com/c/pay/cs_test_a11YYufWQzNY63zpQ6QSNRQhkUpVph4WRmzW0zWJO2znZKdVujZ0N0S22u#fidkdWxOYHwnPyd1blpxYHZxWjA0SDdPUW5JbmFMck1wMmx9N2BLZjFEfGRUNWhqTmJ%2FM2F8bUA2SDRySkFdUV81T1BSV0YxcWJcTUJcYW5rSzN3dzBLPUE0TzRKTTxzNFBjPWZEX1NKSkxpNTVjRjN8VHE0YicpJ2N3amhWYHdzYHcnP3F3cGApJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl"



}
```
