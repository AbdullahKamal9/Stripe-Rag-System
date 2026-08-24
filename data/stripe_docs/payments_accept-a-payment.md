# Source: https://docs.stripe.com/payments/accept-a-payment

# Accept a payment

## Securely accept payments online.

Ask about this page

Copy for LLMView as Markdown

Install tools

Build a payment form or use a prebuilt checkout page to start accepting online payments.

#### Not a developer?

Use Stripe’s [no-code options](/no-code) or apps from [our partners](https://stripe.partners/) to get started and do more with your Stripe account—no code required. If you use a third-party platform to build and maintain a website, you can add Stripe payments with a plugin.

Checkout

Elements

Mobile

Stripe-hosted page

Full embedded page

Redirect to a Stripe-hosted payment page using [Stripe Checkout](/payments/checkout). See how this integration [compares to Stripe’s other integration types](/payments/online-payments#compare-features-and-availability).

[![Checkout preview](https://b.stripecdn.com/docs-statics-srv/assets/b2c79a23390b89a7b589d29387f3e2b2.png)](https://checkout.stripe.dev/)

### Integration effort

Low code

### Integration type

Redirect to Stripe-hosted payment page

### UI customization

Limited customization

[Try it out](https://checkout.stripe.dev/)

First, [register](https://dashboard.stripe.com/register) for a Stripe account.

Use our official libraries to access the Stripe API from your application:

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

[## Redirect your customer to Stripe Checkout Client-sideServer-side](#redirect-customers)

Add an endpoint on your server that creates a [Checkout Session](/api/checkout/sessions/create). A Checkout Session is the programmatic representation of what your customer sees when they’re redirected to the payment form. You can configure it with parameters such as:

* [line\_items](/api/checkout/sessions/create#create_checkout_session-line_items) to set the price and currency of what you’re charging
* [success\_url](/api/checkout/sessions/create#create_checkout_session-success_url) to redirect your customer after they complete the payment

Many other parameters are available, such as [customer](/api/checkout/sessions/create#create_checkout_session-customer), which lets you prefill Checkout fields with known contact information and unify your purchase history. See [create a Checkout Session](/api/checkout/sessions/create) for a full list of parameters.

After creating a Checkout Session, redirect your customer to the [URL](/api/checkout/sessions/object#checkout_session_object-url) returned in the response.

#### Note

Checkout Sessions expire 24 hours after creation by default.

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
# This example sets up an endpoint using the Sinatra framework.


require 'json'
require 'sinatra'
require 'stripe'

# Don't put any keys in code. See https://docs.stripe.com/keys-best-practices.
# Find your keys at https://dashboard.stripe.com/apikeys.
client = Stripe::StripeClient.new(

'[REDACTED_API_KEY]'

)

post '/create-checkout-session' do
  session = client.v1.checkout.sessions.create({
    line_items: [{
      price_data: {
        currency: 'usd',
        product_data: {
          name: 'T-shirt',
        },
        unit_amount: 2000,
      },
      quantity: 1,
    }],
    mode: 'payment',
    success_url: 'https://example.com/success',
  })

  redirect session.url, 303
end
```

### Add a checkout button to your website

Create an HTML page with a checkout button that sends your customer to the server-side endpoint you created.

checkout.html

```
<html>
  <head>
    <title>Buy cool new product</title>
  </head>
  <body>
    <!-- Use action="/create-checkout-session.php" if your server is PHP based. -->
    <form action="/create-checkout-session" method="POST">
      <button type="submit">Checkout</button>
    </form>
  </body>
</html>
```

### Payment methods

By default, Stripe enables cards and other common payment methods. You can turn individual payment methods on or off in the [Stripe Dashboard](https://dashboard.stripe.com/settings/payment_methods). In Checkout, Stripe evaluates the currency and any restrictions, then dynamically presents the supported payment methods to the customer.

To see how your payment methods appear to customers, enter a transaction ID or set an order amount and currency in the Dashboard’s [payment methods review](https://dashboard.stripe.com/settings/payment_methods/review) page.

Checkout supports Apple Pay and Google Pay with no integration changes. Learn how to [test wallets](/testing/wallets?ui=embedded-page).

### Verify your integration

You should now have a working checkout button that redirects your customer to Stripe Checkout.

1. Click the checkout button.
2. You’re redirected to the Stripe Checkout payment form.

If your integration isn’t working:

1. Open the Network tab in your browser’s developer tools.
2. Click the checkout button and confirm it sent an XHR request to your server-side endpoint (`POST /create-checkout-session`).
3. Verify the request is returning a 200 status.
4. Use `console.log(session)` inside your button click listener to confirm the correct data returned.

[## Show a success page Client-sideServer-side](#success-page)

It’s important for your customer to see a success page after they submit the payment form. Host this success page on your site.

Create a minimal success page:

success.html

```
<html>
  <head><title>Thanks for your order!</title></head>
  <body>
    <h1>Thanks for your order!</h1>
    <p>
      We appreciate your business!
      If you have any questions, please email
      <a href="mailto:orders@example.com">orders@example.com</a>.
    </p>
  </body>
</html>
```

Next, update the [success\_url](/api/checkout/sessions/create#create_checkout_session-success_url) parameter in your Checkout Session creation endpoint to point to this new page (for example, `http://localhost:4242/success.html`).

#### Note

If you want to customize your success page, read the [custom success page](/payments/checkout/custom-success-page) guide.

[## Handle post-payment events Server-side](#post-payment)

Stripe sends a [checkout.session.completed](/api/events/types#event_types-checkout.session.completed) event when a customer completes a Checkout Session payment. Use the [Dashboard webhook tool](https://dashboard.stripe.com/webhooks) or follow the [webhook guide](/webhooks/quickstart) to receive and handle these events, which might trigger you to:

* Send an order confirmation email to your customer.
* Log the sale in a database.
* Start a shipping workflow.

Listen to events rather than waiting for your customer to be redirected back to your website. Triggering fulfillment only from your Checkout success page is unreliable.

Learn more in our [fulfillment guide for Checkout](/checkout/fulfillment).

[## Test your integration](#additional-testing-resources)

To test your Stripe-hosted payment form integration:

1. Create a Checkout Session.
2. Fill out the payment details with a method from the following table.
   * Enter any future date for card expiry.
   * Enter any 3-digit number for CVC.
   * Enter any billing postal code.
3. Click **Pay**. You’re redirected to your `success_url`.
4. Go to the Dashboard and look for the payment on the [Transactions page](https://dashboard.stripe.com/test/payments?status%5B0%5D=successful). If your payment succeeded, you’ll see it in that list.
5. Click your payment to see more details, like a Checkout summary with billing information and the list of purchased items. You can use this information to fulfill the order.
6. Confirm that your webhook endpoint successfully received and processed the `checkout.session.completed` event.

Cards

Wallets

Bank redirects

Bank debits

Vouchers

| Card number | Scenario | How to test |
| --- | --- | --- |
| 4242424242424242 | The card payment succeeds and doesn’t require authentication. | Fill out the credit card form using the credit card number with any expiration, CVC, and postal code. |
| 4000002500003155 | The card payment requires [authentication](/strong-customer-authentication). | Fill out the credit card form using the credit card number with any expiration, CVC, and postal code. |
| 4000000000009995 | The card is declined with a decline code like `insufficient_funds`. | Fill out the credit card form using the credit card number with any expiration, CVC, and postal code. |
| 6205500000000000004 | The UnionPay card has a variable length of 13-19 digits. | Fill out the credit card form using the credit card number with any expiration, CVC, and postal code. |

See [Testing](/testing) for additional information to test your integration.

[## OptionalCreate products and prices Server-side](#create-product-prices-upfront)

[## OptionalPrefill customer data Server-side](#prefill-customer-data)

[## OptionalSave payment method details Server-side](#save-payment-method-details)

[## OptionalSeparate authorization and capture Server-side](#auth-and-capture)

## See also

* [Add discounts](/payments/checkout/discounts)
* [Collect taxes](/payments/checkout/taxes)
* [Collect tax IDs](/tax/checkout/tax-ids)
* [Add shipping](/payments/collect-addresses?payment-ui=checkout)
* [Customize your branding](/payments/checkout/customization)
