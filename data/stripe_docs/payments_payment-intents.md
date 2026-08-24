# Source: https://docs.stripe.com/payments/payment-intents

# The Payment Intents API

## Learn how to use the Payment Intents API for Stripe payments.

Ask about this page

Copy for LLMView as Markdown

Install tools

Use the [Payment Intents](/api/payment_intents) API to build an integration that can handle complex payment flows with a status that changes over the [PaymentIntent’s lifecycle](/payments/paymentintents/lifecycle). It tracks a payment from creation through checkout, and triggers additional authentication steps when required.

Some of the advantages of using the [Payment Intents](/api/payment_intents) API include:

* Automatic authentication handling
* No double charges
* No [idempotency key](/api/idempotent_requests) issues
* Support for [Strong Customer Authentication](/strong-customer-authentication) (SCA) and similar regulatory changes

## A complete set of APIs

Use the [Payment Intents](/api/payment_intents) API together with the [Setup Intents](/api/setup_intents) and [Payment Methods](/api/payment_methods) APIs. These APIs help you handle dynamic payments (for example, additional authentication like [3D Secure](/payments/3d-secure)) and prepare you for expansion to other countries while allowing you to support new regulations and regional payment methods.

Building an integration with the Payment Intents API involves two actions: creating and [confirming](/api/payment_intents/confirm) a PaymentIntent. Each PaymentIntent typically correlates with a single shopping cart or customer session in your application. The PaymentIntent encapsulates details about the transaction, such as the supported payment methods, the amount to collect, and the desired currency.

## Creating a PaymentIntent

To get started, see the [accept a payment guide](/payments/accept-a-payment?ui=elements). It describes how to create a PaymentIntent on the server and pass its [client secret](/api/payment_intents/object#payment_intent_object-client_secret) to the client instead of passing the entire PaymentIntent object.

When you [create the PaymentIntent](/api/payment_intents/create), you can specify options like the amount and currency:

Command Line

Select a language

cURL

Stripe CLI

Ruby

Python

PHP

Java

Node.js

Go

.NET

No results

```
curl https://api.stripe.com/v1/payment_intents \
  -u "

[REDACTED_API_KEY]

:" \
  -d amount=1099 \
  -d currency=usd
```

### Best practices

* We recommend creating a PaymentIntent as soon as you know the amount, such as when the customer begins the checkout process, to help track your [purchase funnel](https://en.wikipedia.org/wiki/Purchase_funnel). If the amount changes, you can [update](/api#update_payment_intent) its [amount](/api#payment_intent_object-amount). For example, if your customer backs out of the checkout process and adds new items to their cart, you might need to update the amount when they start the checkout process again.
* If the checkout process is interrupted and resumes later, attempt to reuse the same PaymentIntent instead of creating a new one. Each PaymentIntent has a unique ID that you can use to [retrieve](/api#retrieve_payment_intent) it if you need it again. In the data model of your application, you can store the ID of the PaymentIntent on the customer’s shopping cart or session to facilitate retrieval. The benefit of reusing the PaymentIntent is that the [object state](/payments/paymentintents/lifecycle) helps track any failed payment attempts for a given cart or session.
* Remember to provide an [idempotency key](/api/idempotent_requests) to prevent the creation of duplicate PaymentIntents for the same purchase. This key is typically based on the ID that you associate with the cart or customer session in your application.

## Passing the client secret to the client side

The PaymentIntent contains a [client secret](/api/payment_intents/object#payment_intent_object-client_secret), a key that’s unique to the individual PaymentIntent. On the client side of your application, Stripe.js uses the client secret as a parameter when invoking functions (such as [stripe.confirmCardPayment](/js#stripe-confirm-card-payment) or [stripe.handleCardAction](/js#stripe-handle-card-action)) to complete the payment.

### Retrieve the client secret

The PaymentIntent includes a [client secret](/api/payment_intents/object#payment_intent_object-client_secret) that the client side uses to securely complete the payment process. You can use different approaches to pass the client secret to the client side.

Single-page application

Server-side rendering

Retrieve the client secret from an endpoint on your server, using the browser’s `fetch` function. This approach is best if your client side is a single-page application, particularly one built with a modern frontend framework like React. Create the server endpoint that serves the client secret:

main.rb

Select a language

Ruby

Python

PHP

Java

Node.js

Go

.NET

No results

```
get '/secret' do
  intent = # ... Create or retrieve the PaymentIntent
  {client_secret: intent.client_secret}.to_json
end
```

And then fetch the client secret with JavaScript on the client side:

```
(async () => {
  const response = await fetch('/secret');
  const {client_secret: clientSecret} = await response.json();
  // Render the form using the clientSecret
})();
```

#### Caution

You can use the client secret to complete the payment process with the amount specified on the PaymentIntent. Don’t log it, embed it in URLs, or expose it to anyone other than the customer. Make sure that you have [TLS](/security/guide#tls) on any page that includes the client secret.

## After the payment

After the client confirms the payment, it’s a best practice for your server to [monitor webhooks](/payments/payment-intents/verifying-status#webhooks) to detect when the payment successfully completes or fails.

A `PaymentIntent` might have more than one [Charge](/api/charges) object associated with it if there were multiple payment attempts. For example, retries can create multiple `Charges`. For each charge you can inspect the [outcome](/api/charges/object#charge_object-outcome) and [details of the payment method](/api/charges/object#charge_object-payment_method_details) used.

## Optimizing payment methods for future payments

The [setup\_future\_usage](/api/payment_intents/object#payment_intent_object-setup_future_usage) parameter saves payment methods to use again in the future. For cards, it also optimizes authorization rates in compliance with regional legislation and network rules, such as [SCA](/strong-customer-authentication). To determine which value to use, consider how you want to use this payment method in the future.

| How you intend to use the payment method | setup\_future\_usage enum value to use |
| --- | --- |
| On-session payments only | `on_session` |
| Off-session payments only | `off_session` |
| Both on and off-session payments | `off_session` |

You can still accept off-session payments with a card set up for on-session payments, but the bank is more likely to reject the off-session payment and require authentication from the cardholder.

The following example shows how to create a PaymentIntent and specify `setup_future_usage`:

Command Line

Select a language

cURL

Stripe CLI

Ruby

Python

PHP

Java

Node.js

Go

.NET

No results

```
curl https://api.stripe.com/v1/payment_intents \
  -u "

[REDACTED_API_KEY]

:" \
  -d amount=1099 \
  -d currency=usd \
  -d setup_future_usage=off_session
```

#### Caution

Setups for off-session payments are more likely to incur additional friction. Use on-session setup if you don’t intend to accept off-session payments with the saved card.

## Dynamic statement descriptor

By default, your Stripe account’s [statement descriptor](/get-started/account/set-up#public-business-information) appears on customer statements whenever you charge their card. To provide a different description on a per-payment basis, use the [statement\_descriptor](/api/payment_intents/object#payment_intent_object-statement_descriptor) parameter.

Command Line

Select a language

cURL

Stripe CLI

Ruby

Python

PHP

Java

Node.js

Go

.NET

No results

```
curl https://api.stripe.com/v1/payment_intents \
  -u "

[REDACTED_API_KEY]

:" \
  -d amount=1099 \
  -d currency=usd \
  -d "statement_descriptor_suffix=Custom descriptor"
```

#### Note

Use the `statement_descriptor` parameter for non-card charges and `statement_descriptor_suffix` for card charges.

[Statement descriptors](/get-started/account/statement-descriptors) are limited to 22 characters, can’t use the special characters `<`, `>`, `'`, `"`, or `*`, and must not consist solely of numbers. When using dynamic statement descriptors, the dynamic text is appended to the [statement descriptor prefix](https://dashboard.stripe.com/settings/public) set in the Stripe Dashboard. An asterisk (`*`) and an empty space are also added to separate the default statement descriptor from the dynamic portion. These 2 characters count towards the 22 character limit.

## Storing information in metadata

Stripe supports adding [metadata](/api#metadata) to the most common requests you make, such as processing payments. Metadata isn’t shown to customers or factored into whether or not a payment is declined or blocked by our fraud prevention system.

Through metadata, you can associate information that’s meaningful to you with Stripe activity.

Any metadata you include is viewable in the Dashboard (for example, when looking at the page for an individual payment), and is also available in common reports. As an example, you can attach the order ID for your store to the PaymentIntent for that order. Doing so allows you to easily reconcile payments in Stripe to orders in your system.

If you’re using [Radar for Fraud Teams](/radar), consider passing additional customer information and order information as metadata. Then you can write [Radar rules using metadata attributes](/radar/rules/reference#metadata-attributes) and have more information available within the Dashboard, which can expedite your review process.

When a PaymentIntent creates a charge, the PaymentIntent copies its metadata to the charge. Subsequent updates to the PaymentIntent’s metadata won’t modify the metadata of charges previously created by the PaymentIntent.

Command Line

Select a language

cURL

Stripe CLI

Ruby

Python

PHP

Java

Node.js

Go

.NET

No results

```
curl https://api.stripe.com/v1/payment_intents \
  -u "

sk_test_EXAMPLE_KEY

:" \
  -d amount=1099 \
  -d currency=usd \
  -d "metadata[order_id]=6735"
```

#### Caution

Don’t store any sensitive information (personally identifiable information, card details, and so on) as metadata or in the `description` parameter of the PaymentIntent.

## See also

* [Accept a payment online](/payments/accept-a-payment?platform=web)
* [Accept a payment in an iOS app](/payments/accept-a-payment?payment-ui=mobile&platform=ios)
* [Accept a payment in an Android app](/payments/accept-a-payment?payment-ui=mobile&platform=android)
* [Set up future payments](/payments/save-and-reuse)
