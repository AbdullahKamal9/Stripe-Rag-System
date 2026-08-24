# Source: https://docs.stripe.com/payments/payment-intents/migration

# Migrate to the Payment Intents API

Ask about this page

Copy for LLMView as Markdown

Install tools

#### Payment Element integration features

You can integrate with the Payment Element to manage subscriptions, tax, discounts, shipping, and currency conversion. To learn more, see the [Build a checkout page](/payments/quickstart-checkout-sessions) guide.

Learn how to migrate your existing cards and Charges API integration.

Migrating your payment flow can be daunting. It’s safe to incrementally adopt the Payment Intents API and use it in parallel with the Charges API. To this end, you can split up the migration into the following steps:

1. [Update your API version and your client library](#api-version).
2. If applicable, [migrate code that reads from Charge properties](/payments/payment-intents/migration/charges) so that you have a consistent read path between charges created by the Charges API and charges created by the Payment Intents API. This ensures a read-side integration that works for both your old and new payments integrations.
3. Migrate your existing Charges API integration on [Web](#web), [iOS](/payments/accept-a-payment?payment-ui=mobile&platform=ios), and [Android](/payments/accept-a-payment?payment-ui=mobile&platform=android) to use the Payment Intents API.
4. Migrate your integration that [saves cards on Customer objects](#saved-cards).
5. [Test with regulatory test cards](/testing#regulatory-cards) to ensure your upgraded integration handles authentication correctly.

## Update your API version and your client library

While the Payment Intents API works on all API versions, we recommend that you [upgrade to the latest API version](/upgrades#how-can-i-upgrade-my-api). If you decide to use an API version older than [2019-02-11](/upgrades#2019-02-11), note the following two changes as you go through the code examples:

* `requires_source` has been renamed to `requires_payment_method`
* `requires_source_action` has been renamed to `requires_action`

In addition, if you use one of our [SDKs](/sdks), upgrade to the latest version of the library to use the Payment Intents API.

## Migrate your one-time payment flows

Elements

Payment Request Button

Legacy Checkout

Stripe.js v2

An integration built with Stripe.js & Elements consists of the following steps:

1. Register your intent to collect payment on the server side
2. Collect payment details on the client side
3. Initiate creation of the payment
4. Fulfill the customer’s order on the server side

### Step 1: Register intent to collect payment on the server side

[Create a PaymentIntent](/payments/payment-intents) on your server and make it [accessible on the client side](/payments/payment-intents#passing-to-client).

curl

Ruby

Python

PHP

Java

Node.js

Go

.NET

Before

After

Not possible before

Command Line

```
curl https://api.stripe.com/v1/payment_intents \
  -u

sk_test_EXAMPLE_KEY

: \
  -d "amount"=1099 \
  -d "currency"="usd"
```

### Step 2: Collect payment details on the client side

Use the [confirmCardPayment](/js#stripe-confirm-card-payment) function, which collects the payment information and submits it directly to Stripe.

JavaScript

Javascript (ESNext)

Before

After

```
stripe.createToken(
  cardElement
).then(function(token) {
  // Send token to server
});
```

```
stripe.confirmCardPayment(
  INTENT_SECRET_FROM_STEP_1,
  {
    payment_method: {card: cardElement}
  }
).then(function(result) {
  if (result.error) {
    // Display error.message in your UI.
  } else {
    // The payment has succeeded
    // Display a success message
  }
});
```

### Step 3: Initiate creation of the payment

In your existing integration, the final step is using tokenized payment information to create a charge on your server. This is no longer necessary, as the `confirmCardPayment` function—called in the previous step—initiates creation of the charge.

curl

Ruby

Python

PHP

Java

Node.js

Go

.NET

Before

After

Command Line

```
curl https://api.stripe.com/v1/charges \
  -u

sk_test_EXAMPLE_KEY

: \
  -d "source"="{{FROM_PREVIOUS_STEP}}" \
  -d "amount"=1099 \
  -d "currency"="usd"
```

Completed in previous step

### Step 4: Fulfill the customer’s order

With automatic confirmation, the charge is created for you asynchronously based on customer action on the client side, so you must [monitor webhooks](/payments/payment-intents/verifying-status) to determine when the payment completes successfully. To perform steps like order fulfillment after a customer’s payment is successful, implement support for webhooks and monitor the `payment_intent.succeeded` event.

Before

After

If charge succeeds, fulfill.

Subscribe to the `payment_intent.succeeded` webhook and fulfill in the webhook handler.

Now that you have migrated, use the test cards in the following section to verify your upgraded integration handles 3D Secure authentication.

## Migrate your integration that saves cards on Customer objects

Saving cards in checkout flow

Saving cards outside checkout flow

Paying with saved cards

A Payment Intents API integration that collects card information in the checkout flow consists of the following steps:

1. Register your intent to collect payment on the server side
2. Collect payment details on the client side
3. Initiate creation of the payment
4. Fulfill the customer’s order on the server side

### Step 1: Register intent to collect payment on the server side

[Create a PaymentIntent](/payments/payment-intents) on your server. Set [setup\_future\_usage](/api/payment_intents/create#create_payment_intent-setup_future_usage) to `off_session` if you primarily intend to charge users when they’re outside of your application, or `on_session` if you plan to charge them in the application. If you plan to use the card for both on and off session payments use `off_session`. Providing the `setup_future_usage` parameter along with a Customer ID will save the resulting PaymentMethod to that Customer after the PaymentIntent has been confirmed and any required actions from the customer are complete. Next, make the PaymentIntent [accessible on the client side](/payments/payment-intents#passing-to-client).

curl

Ruby

Python

PHP

Java

Node.js

Go

.NET

Before

After

Not possible before

Command Line

```
curl https://api.stripe.com/v1/payment_intents \
  -u

sk_test_EXAMPLE_KEY

: \
  -d "setup_future_usage"="off_session" \
  -d "amount"=1099 \
  -d "currency"="usd"
```

### Step 2: Collect payment details on the client side

Use the [confirmCardPayment](/js#stripe-confirm-card-payment) function, which collects the payment information and submits it directly to Stripe.

JavaScript

Javascript (ESNext)

Before

After

```
stripe.createToken(
// or stripe.createSource
  cardElement
).then(function(token) {
  // Send token to server
});
```

```
stripe.confirmCardPayment(
  '{{INTENT_SECRET_FROM_STEP_1}}',
  {
    payment_method: {card: cardElement},
  }
).then(function(result) {
  if (result.error) {
    // Display error.message in your UI.
  } else {
    // The payment has succeeded
    // Display a success message
  }
});
```

Finally, attach the payment method (`paymentIntent.payment_method`) to the customer.

curl

Ruby

Python

PHP

Java

Node.js

Go

.NET

Before

After

Command Line

```
curl https://api.stripe.com/v1/customers/{{CUSTOMER_ID}}/sources \
  -u

sk_test_EXAMPLE_KEY

: \
  -d "source"="{{TOKEN_OR_SOURCE}}"
```

Command Line

```
curl https://api.stripe.com/v1/payment_method/{{PAYMENT_METHOD_ID}}/attach \
  -u

sk_test_EXAMPLE_KEY

: \
  -d "customer"="{{CUSTOMER_ID}}"
```

### Step 3: Initiate creation of the payment

In your existing integration, the final step is using tokenized payment information to create a charge on your server. This is no longer necessary, as the `confirmCardPayment` function—called in the previous step—initiates creation of the charge.

curl

Ruby

Python

PHP

Java

Node.js

Go

.NET

Before

After

Command Line

```
curl https://api.stripe.com/v1/charges \
  -u

sk_test_EXAMPLE_KEY

: \
  -d "source"="{{FROM_PREVIOUS_STEP}}" \
  -d "customer"="{{CUSTOMER_ID}}" \
  -d "amount"=1099 \
  -d "currency"="usd"
```

Completed in previous step

### Step 4: Fulfill the customer’s order

With automatic confirmation, the charge is created for you asynchronously based on customer action on the client side, so you must [monitor webhooks](/payments/payment-intents/verifying-status) to determine when the payment completes successfully. To perform steps like order fulfillment after a customer’s payment is successful, implement support for webhooks and monitor the `payment_intent.succeeded` event.

Before

After

If charge succeeds, fulfill.

Subscribe to the `payment_intent.succeeded` webhook and fulfill in the webhook handler.

Now that you have migrated, use the test cards in the following section to verify your upgraded integration handles 3D Secure authentication.

## Access saved payment methods

To display the customer’s previously saved Cards, Sources, and PaymentMethods, [list the payment methods](/api/payment_methods/list) instead of reading the [sources](/api/customers/object#customer_object-sources) property of the customer object. This is required because new PaymentMethods added to a customer won’t be duplicated in the sources property of the customer object.

curl

Ruby

Python

PHP

Java

Node.js

Go

.NET

Before

After

Command Line

```
customer.sources
```

Command Line

```
curl https://api.stripe.com/v1/payment_methods?customer={{CUSTOMER_ID}}&type=card \
  -u

sk_test_EXAMPLE_KEY

:
```

## Test the integration

It’s important to thoroughly test your integration to make sure you’re correctly handling cards that require additional authentication and cards that don’t. Use these card numbers in a [sandbox](/keys#test-live-modes) with any expiration date in the future and any three digit CVC code to validate your integration when authentication is required and when it’s not required.

| Number | Authentication | Description |
| --- | --- | --- |
| 4000002500003155 | Required on setup or first transaction | This test card requires authentication for [one-time payments](/payments/accept-a-payment?platform=web). However, if you set up this card using the [Setup Intents API](/payments/save-and-reuse) and use the saved card for subsequent payments, no further authentication is needed. |
| 4000002760003184 | Required | This test card requires authentication on all transactions. |
| 4000008260003178 | Required | This test card requires authentication, but payments will be declined with an `insufficient_funds` failure code after successful authentication. |
| 4000000000003055 | Supported | This test card supports authentication through 3D Secure 2, but doesn’t require it. Payments using this card don’t require additional authentication in a sandbox unless your [sandbox Radar rules](/payments/3d-secure/authentication-flow#three-ds-radar) request authentication. |

Use these cards in your application or the [payments demo](https://stripe-payments-demo.appspot.com) to see the different behavior.

## See also

* [PaymentIntents on iOS](/payments/accept-a-payment?payment-ui=mobile&platform=ios)
* [PaymentIntents on Android](/payments/accept-a-payment?payment-ui=mobile&platform=android)
