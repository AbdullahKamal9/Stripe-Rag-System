# Source: https://docs.stripe.com/billing/subscriptions/build-subscriptions

# Build a subscriptions integration

## Create and manage subscriptions to accept recurring payments.

Ask about this page

Copy for LLMView as Markdown

Install tools

Checkout

Elements

Mobile

Stripe-hosted page

Full embedded page

![Checkout subscription page](https://b.stripecdn.com/docs-statics-srv/assets/checkout-subs-preview.d409ee79bf1f3280b9dfd3968b314c21.png)

### Integration effort

Low code

### UI customization

Limited customization

### Integration type

Use prebuilt hosted pages to collect payments and manage your [subscriptions](/billing/subscriptions/creating).

[Try it out](https://checkout.stripe.dev/)

## What you’ll build

This guide describes how to sell fixed-price monthly subscriptions using [Stripe Checkout](/payments/checkout).

This guide shows you how to:

* Model your business by building a product catalog.
* Add a Checkout session to your site, including a button and success and cancellation pages.
* Monitor subscription events and provision access to your service.
* Set up the [customer portal](/customer-management).
* Add a customer portal session to your site, including a button and redirect.
* Let customers manage their subscription through the portal.
* Learn how to use [flexible billing mode](/billing/subscriptions/billing-mode) to access enhanced billing behavior and additional features.

If you aren’t ready to code an integration, you can set up basic subscriptions [manually in the Dashboard](/no-code/subscriptions) or use [Payment Links](/payment-links) to set up subscriptions without writing any code.

Learn more about [designing an integration](/billing/subscriptions/design-an-integration) to understand the decisions and required resources for a full integration.

After you complete the integration, you can extend it to:

* Display [taxes](/payments/checkout/taxes)
* Apply [discounts](/billing/subscriptions/coupons#using-coupons-in-checkout)
* Offer customers a [free trial period](/billing/subscriptions/trials)
* Add [payment methods](/payments/payment-methods/integration-options)
* Integrate the [hosted invoice page](/invoicing/hosted-invoice-page)
* Use Checkout in [setup mode](/payments/save-and-reuse)
* Set up [usage-based billing](/products-prices/pricing-models#usage-based-pricing), [pricing tiers](/products-prices/pricing-models#tiered-pricing), and [usage-based pricing](/products-prices/pricing-models#usage-based-pricing)
* Manage [prorations](/billing/subscriptions/prorations)
* Allow customers to [subscribe to multiple products](/billing/subscriptions/quantities#multiple-product-sub)
* Integrate [entitlements](/billing/entitlements) to manage access to your product’s features

[## Set up Stripe](#set-up-stripe)

Install the Stripe client of your choice:

Command Line

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
# Available as a gem
sudo gem install stripe
```

Gemfile

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
# If you use bundler, you can add this line to your Gemfile
gem 'stripe'
```

Optionally, install the Stripe CLI. The CLI provides [webhook](/webhooks#test-webhook) testing, and you can run it to create your products and prices.

Command Line

Select a language

homebrew

Install from source

No results

```
# Install Homebrew to run this command: https://brew.sh/
brew install stripe/stripe-cli/stripe

# Connect the CLI to your dashboard
stripe login
```

For additional install options, see [Get started with the Stripe CLI](/stripe-cli).

[## Create the pricing model Dashboard or Stripe CLI](#create-pricing-model)

[Recurring pricing models](/products-prices/pricing-models) represent the products or services you sell, how much they cost, what currency you accept for payments, and the service period for subscriptions. To build the pricing model, create [products](/api/products) (what you sell) and [prices](/api/prices) (how much and how often to charge for your products).

This example uses flat-rate pricing with two different service-level options: Basic and Premium. For each service-level option, you need to create a product and a recurring price. To add a one-time charge for something like a setup fee, create a third product with a one-time price.

Each product bills at monthly intervals. The price for the Basic product is 5 USD. The price for the Premium product is 15 USD. See the [flat rate pricing](/subscriptions/pricing-models/flat-rate-pricing) guide for an example with three tiers.

Dashboard

API

Go to the [Add a product](https://dashboard.stripe.com/test/products/create) page and create two products. Add one price for each product, each with a monthly recurring billing period:

* Premium product: Premium service with extra features

  + Price: Flat rate | 15 USD
* Basic product: Basic service with minimum features

  + Price: Flat rate | 5 USD

After you create the prices, record the price IDs so you can use them in other steps. Price IDs look like this: `price_G0FvDp6vZvdwRZ`.

When you’re ready, use the **Copy to live mode** button at the top right of the page to clone your product from [a sandbox to live mode](/keys#test-live-modes).

If you offer multiple billing periods, use Checkout to [upsell](/payments/checkout/upsells) customers on longer billing periods and collect more revenue upfront.

For other pricing models, see [Billing examples](/products-prices/pricing-models).

[## Create a Checkout Session Client and Server](#create-session)

Add a checkout button to your website that calls a server-side endpoint to create a Checkout Session.

index.html

[View full sample](https://github.com/stripe-samples/checkout-single-subscription/blob/master/client/index.html "View full sample on GitHub")

```
<html>
  <head>
    <title>Checkout</title>
  </head>
  <body>
    <form action="/create-checkout-session" method="POST">
      <!-- Note: If using PHP set the action to /create-checkout-session.php -->

      <input type="hidden" name="priceId" value="price_G0FvDp6vZvdwRZ" />
      <button type="submit">Checkout</button>
    </form>
  </body>
</html>
```

On the back end of your application, define an endpoint that [creates the session](/api/checkout/sessions/create) for your front end to call. You need these values:

* The price ID of the subscription the customer is signing up for (your front end passes this value)
* Your `success_url`, which is a page on your website that Checkout returns your customer to after they complete the payment

You can optionally:

* Configure a [billing cycle anchor](/billing/subscriptions/billing-cycle) to your subscription in this call.
* Use [custom text](/payments/checkout/custom-components?platform=web&payment-ui=stripe-hosted#customize-text) to include your subscription and cancellation terms, and a link to where your customers can update or cancel their subscription. We recommend configuring [email reminders and notifications](/invoicing/send-email#email-configuration) for your subscribers.

If you created a one-time price in [step 2](/billing/subscriptions/build-subscriptions#create-pricing-model), pass that price ID as well. After creating a Checkout Session, redirect your customer to the [URL](/api/checkout/sessions/object#checkout_session_object-url) returned in the response.

You can enable more accurate and predictable subscription behavior when you create a Checkout Session by setting the [billing mode](/billing/subscriptions/billing-mode) type to `flexible`. You must use the [Stripe API version 2025-06-30.basil](/upgrades) or later.

#### Note

You can use [lookup\_keys](/products-prices/manage-prices#lookup-keys) to fetch prices rather than price IDs. For an example, see the [sample application](https://github.com/stripe-samples/subscription-use-cases/tree/main/fixed-price-subscriptions).

server.rb

Select a language

Ruby

Python

PHP

Java

Node.js

Go

.NET

No results

[View full sample](https://github.com/stripe-samples/checkout-single-subscription/blob/master/server/ruby/server.rb "View full sample on GitHub")

```
# Don't put any keys in code. See https://docs.stripe.com/keys-best-practices.
# Find your keys at https://dashboard.stripe.com/apikeys.
client = Stripe::StripeClient.new(

'[REDACTED_API_KEY]'

)

# The price ID passed from the front end.
#   price_id = params['priceId']
price_id = '{{PRICE_ID}}'

session = client.v1.checkout.sessions.create({
  success_url: 'https://example.com/success.html?session_id={CHECKOUT_SESSION_ID}',
  mode: 'subscription',
  line_items: [{
    # For usage-based billing, don't pass quantity
    quantity: 1,
    price: price_id
  }],
  subscription_data: {
    billing_mode: { type: 'flexible' }
  }
})

# Redirect to the URL returned on the session
#   redirect session.url, 303
```

This example customizes the `success_url` by appending the session ID. Learn more about [customizing your success page](/payments/checkout/custom-success-page).

From your [Dashboard](https://dashboard.stripe.com/settings/payment_methods), enable the payment methods you want to accept from your customers. Checkout supports [several payment methods](/payments/payment-methods/payment-method-support#product-support).

[## Provision and monitor subscriptions Server](#provision-and-monitor)

After the subscription signup succeeds, the customer returns to your website at the `success_url`, which initiates a `checkout.session.completed` [webhook](/webhooks). When you receive a `checkout.session.completed` event, use [entitlements](/billing/entitlements) to provision the subscription. Continue to provision each month (if billing monthly) as you receive `invoice.paid` events. If you receive an `invoice.payment_failed` event, notify your customer and send them to the customer portal to update their payment method.

To determine the next step for your system’s logic, check the event type and parse the payload of each [event object](/api/events/object), such as `invoice.paid`. Store the IDs of the `Subscription` and `Customer` or `Account` objects in your database for verification.

For testing purposes, you can monitor events in the [Events tab](https://dashboard.stripe.com/workbench/events) of [Workbench](/workbench). For production, set up a webhook endpoint and subscribe to appropriate event types. If you don’t know your `STRIPE_WEBHOOK_SECRET` key, go to the destination details view of the [Webhooks tab](https://dashboard.stripe.com/workbench/webhooks) in Workbench to view it.

server.rb

Select a language

Ruby

Python

PHP

Java

Node.js

Go

.NET

No results

[View full sample](https://github.com/stripe-samples/checkout-single-subscription/blob/master/server/ruby/server.rb "View full sample on GitHub")

```
# Don't put any keys in code. See https://docs.stripe.com/keys-best-practices.
# Find your keys at https://dashboard.stripe.com/apikeys.
client = Stripe::StripeClient.new(

'[REDACTED_API_KEY]'

)

post '/webhook' do
  webhook_secret =

'{{STRIPE_WEBHOOK_SECRET}}'

payload = request.body.read
  if !webhook_secret.empty?
    # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
    sig_header = request.env['HTTP_STRIPE_SIGNATURE']
    event = nil

    begin
      event = Stripe::Webhook.construct_event(
        payload, sig_header, webhook_secret
      )
    rescue JSON::ParserError => e
      # Invalid payload
      status 400
      return
    rescue Stripe::SignatureVerificationError => e
      # Invalid signature
      puts '⚠️  Webhook signature verification failed.'
      status 400
      return
    end
  else
    data = JSON.parse(payload, symbolize_names: true)
    event = Stripe::Event.construct_from(data)
  end
  # Get the type of webhook event sent
  event_type = event['type']
  data = event['data']
  data_object = data['object']

  case event_type
  when 'checkout.session.completed'
    # Payment is successful and the subscription is created.
    # Provision the subscription and save the customer ID to your database.
  when 'invoice.paid'
    # Continue to provision the subscription as payments continue to be made.
    # Store the status in your database and check when a customer accesses your service.
    # This approach helps you avoid hitting rate limits.
  when 'invoice.payment_failed'
    # The payment failed or the customer doesn't have a valid payment method.
    # The subscription becomes past_due. Notify your customer and send them to the
    # customer portal to update their payment information.
  else
    puts "Unhandled event type: #{event.type}"
  end

  status 200
end
```

The minimum event types to monitor:

| Event name | Description |
| --- | --- |
| `checkout.session.completed` | Sent when a customer successfully completes the Checkout Session, informing you of a new purchase. |
| `invoice.paid` | Sent each billing period when a payment succeeds. |
| `invoice.payment_failed` | Sent each billing period if there’s an issue with your customer’s payment method. |

For even more events to monitor, see [Subscription webhooks](/billing/subscriptions/webhooks).

[## Configure the customer portal Dashboard](#configure-portal)

The [customer portal](/customer-management) lets your customers directly manage their existing subscriptions and invoices.

Use the [Dashboard](https://dashboard.stripe.com/test/settings/billing/portal) to configure the portal. At a minimum, make sure to [configure the portal](/customer-management) so that customers can update their payment methods.

[## Create a portal session Server](#create-portal-session)

Define an endpoint that [creates the customer portal session](/api/customer_portal/sessions/create) for your front end to call. Include the ID of the customer created by the Checkout Session that you saved while processing the `checkout.session.completed` webhook. You can also set a default redirect link for the portal in the Dashboard.

Pass an optional `return_url` value for the page on your site to redirect your customer to after they finish managing their subscription:

Accounts v2

Customers v1

server.rb

Select a language

Ruby

Python

PHP

Java

Node.js

Go

.NET

No results

[View full sample](https://github.com/stripe-samples/checkout-single-subscription/blob/master/server/ruby/server.rb "View full sample on GitHub")

```
# Don't put any keys in code. See https://docs.stripe.com/keys-best-practices.
# Find your keys at https://dashboard.stripe.com/apikeys.
client = Stripe::StripeClient.new(

'[REDACTED_API_KEY]'

)

# This is the URL that users are redirected to after they're done
# managing their billing.
return_url =

'{{DOMAIN_URL}}'

customer_account_id =

'{{CUSTOMER_ACCOUNT_ID}}'

session = Stripe::BillingPortal::Session.create({
  customer_account: customer_account_id,
  return_url: return_url,
})

# Redirect to the URL for the session
#   redirect session.url, 303
```

[## Send customers to the customer portal Client](#send-to-portal)

On your front end, add a button to the page at the `success_url` that provides a link to the customer portal:

success.html

[View full sample](https://github.com/stripe-samples/checkout-single-subscription/blob/master/client/success.html "View full sample on GitHub")

```
<html>
  <head>
    <title>Manage Billing</title>
  </head>
  <body>
    <form action="/customer-portal" method="POST">
      <!-- Note: If using PHP set the action to /customer-portal.php -->
      <button type="submit">Manage Billing</button>
    </form>
  </body>
</html>
```

After exiting the customer portal, the customer returns to your website at the `return_url`. Continue to [monitor events](/billing/subscriptions/webhooks) to track the status of the customer’s subscription.

If you configure the customer portal to allow actions such as canceling a subscription, [monitor additional events](/customer-management/integrate-customer-portal#webhooks).

[## Test your integration](#test)

### Test payment methods

Use the following table to test different payment methods and scenarios.

| Payment method | Scenario | How to test |
| --- | --- | --- |
| BECS Direct Debit | Your customer successfully pays with BECS Direct Debit. | Fill out the form using the account number `900123456` and BSB `000000`. The confirmed PaymentIntent initially transitions to `processing`, then transitions to the `succeeded` status three minutes later. |
| BECS Direct Debit | Your customer’s payment fails with an `account_closed` error code. | Fill out the form using the account number `111111113` and BSB `000000`. |
| Credit card | The card payment succeeds and doesn’t require authentication. | Fill out the credit card form using the credit card number `4242 4242 4242 4242` with any expiration, CVC, and postal code. |
| Credit card | The card payment requires [authentication](/strong-customer-authentication). | Fill out the credit card form using the credit card number `4000 0025 0000 3155` with any expiration, CVC, and postal code. |
| Credit card | The card is declined with a decline code like `insufficient_funds`. | Fill out the credit card form using the credit card number `4000 0000 0000 9995` with any expiration, CVC, and postal code. |
| SEPA Direct Debit | Your customer successfully pays with SEPA Direct Debit. | Fill out the form using the account number `AT321904300235473204`. The confirmed PaymentIntent initially transitions to processing, then transitions to the succeeded status three minutes later. |
| SEPA Direct Debit | Your customer’s PaymentIntent status transitions from `processing` to `requires_payment_method`. | Fill out the form using the account number `AT861904300235473202`. |

### Monitor events

Set up webhooks to listen to subscription change events, such as upgrades and cancellations. You can view [subscription webhook events](/billing/subscriptions/webhooks) in the [Dashboard](https://dashboard.stripe.com/test/events) or with the [Stripe CLI](/webhooks#test-webhook).

Learn more about [testing your Billing integration](/billing/testing).

## See also

* [Offer customers a free trial period](/billing/subscriptions/trials)
* [Apply discounts](/billing/subscriptions/coupons#using-coupons-in-checkout)
* [Manage prorations](/billing/subscriptions/prorations)
* [Integrate entitlements to manage access to your product’s features](/billing/entitlements)
