# Source: https://docs.stripe.com/payments/online-payments

# Online payments

## Learn about your integration options for accepting payments online.

Use the Optimized Checkout Suite for your payments integration, which includes [payment UIs](#payment-uis), [dynamic payment methods](#payment-methods), and [faster checkout with Link](#link). To get started, [find the integration](/payments/use-cases/get-started) that meets your business needs.

[Explore the demo](https://checkout.stripe.dev/)

## Payment UIs

Use prebuilt payment UIs to accept payments online.

[No code![](https://b.stripecdn.com/docs-statics-srv/assets/link.f0b2a66175b477e86a89e39eba75fb6c.svg)

Shareable payment links](/payment-links "Shareable payment links")Use Payment Links to embed or share a link to a Stripe payment page to accept payments without a website.

Integration effort:

[Recommended![](https://b.stripecdn.com/docs-statics-srv/assets/checkout.4abfc4af6b46ecac81ce96bc8ff0213e.svg)

Full page](/checkout/quickstart "Full page")Embed or redirect to a prebuilt payment page on your website.

Integration effort:

[Private preview![](https://b.stripecdn.com/docs-statics-srv/assets/checkout-form.17e9a55c9db50e0d65dc5e92d8720896.svg)

Embedded form](/payments/checkout/how-checkout-works?payment-ui=checkout-form "Embedded form")Embed a prebuilt payment form on your website.

Integration effort:

[![](https://b.stripecdn.com/docs-statics-srv/assets/elements.750bc8af6d17414b54dc09ae8acb8efb.svg)

Custom payment flow](/payments/quickstart-checkout-sessions "Custom payment flow")Use Stripe Elements to design a custom page to collect payments.

Integration effort:

[![](https://b.stripecdn.com/docs-statics-srv/assets/ios-landing.35eb3fe43605b2b982353f4bdac95840.png)

In-app payments](/payments/quickstart?platform=ios "In-app payments")Use the Mobile Payment Element to accept payments in your iOS, Android, or React Native app.

Integration effort:

[Private preview![](https://b.stripecdn.com/docs-statics-srv/assets/checkout.4abfc4af6b46ecac81ce96bc8ff0213e.svg)

Checkout studio](/payments/checkout-studio "Checkout studio")Launch, configure, and monitor Checkout integrations from the Dashboard without writing code.

Integration effort:

## Payment APIs

Choose the API to address your payments use case.

### Choose your API

We recommend the Checkout Sessions API for most integrations. Checkout Sessions allows you to build both a basic payment collection integration and complex checkout flows.

If you use PaymentIntents, you must manually build equivalent features in your code, including discount logic, tax calculation, and currency conversion. Some features, such as Adaptive Pricing, require significant effort to replicate with PaymentIntents. Choose PaymentIntents only if you want to own every part of your checkout, and rebuild these capabilities yourself.

|  | [Checkout Sessions](/api/checkout/sessions) | [Payment Intents](/api/payment_intents) |
| --- | --- | --- |
| **Recommended for** | Any businesses that wants to accept payments with less code and less maintenance. Checkout Sessions covers similar use cases as Payment Intents (basic payment collection using `price_data` or full checkout with line items, tax, discounts, shipping, subscriptions, and [Adaptive Pricing](/payments/currencies/localize-prices/adaptive-pricing). | Businesses that want to own their checkout state and build their own discount, tax, subscription, and currency conversion logic. This requires significantly more code and ongoing maintenance. |
| **Integration** | Use code to add a checkout page and integrate additional products. For example, enable Stripe Tax by setting [automatic\_tax.enabled = true](/api/checkout/sessions/create#create_checkout_session-automatic_tax-enabled), compared to the Payment Intents API which requires you to manually call the Tax API and link calculations. Some features, such as [Adaptive Pricing](/payments/currencies/localize-prices/adaptive-pricing), are only available with Checkout Sessions. | The Payment Intents API is a lower-level API that allows you to build everything yourself, including tax calculation, discounts, subscriptions, and currency conversion. When you use this API, you calculate the final amount and manage the entire checkout lifecycle in your own code. |
| **User interface** | * Full page * Embedded form Private preview * Elements | Elements |
| **Complexity** | Scales with your business from simple payment collection to complex checkout flows. It covers similar use cases as Payment Intents. | Requires building and maintaining checkout features included with Checkout Sessions. Be deliberate about choosing this path. |

### Feature comparison

| Feature | Checkout Sessions API | Payment Intents API |
| --- | --- | --- |
| **Design** | Use for complete checkout flows, including one-time payments or complex flows with line items, taxes, shipping, and subscriptions. | A lower-level API for building your own payment flow from scratch. You must implement all checkout logic yourself. |
| **Tax calculation** | Built-in tax calculation with [Stripe Tax](/tax). | Requires a separate integration with the [Tax API](/api/tax/settings). |
| **Subscriptions** | Built-in [subscription creation](/payments/advanced/build-subscriptions). | Requires a separate integration with [Subscriptions](/billing/subscriptions/overview). |
| **Coupons and discounts** | Built-in [coupon and discount](/payments/advanced/discounts?payment-ui=embedded-components) handling. | Requires calculating discounts manually. |
| **Shipping costs** | Built-in shipping cost calculation. | Requires calculating shipping costs manually. |
| **UI flexibility** | Hosted checkout page, embedded forms, and custom UI. | Custom UI only. |
| **Address collection** | Built-in [customer, billing, and shipping address](/payments/advanced/collect-addresses) collection. | Requires handling addresses manually. |
| **Order tracking** | Built-in order summary and [receipt](/payments/advanced/receipts) functionality. | Requires implementing custom order tracking. |
| **Amount updates** | [Dynamic inventory and line item updates](/payments/advanced/dynamic-updates). | Requires manually updating the amount. |
| **Session expiration** | Automatic expiration after 24 hours. | No automatic expiration. |
| **Webhook events** | [Webhook events](/webhooks) for the complete checkout lifecycle. | Payment status events only. |

## Add payment methods

Accept more payment methods to help your business expand its global reach and improve checkout conversion.

[Dynamic payment methods

Simplify your payment methods code by dynamically ordering and displaying payment methods.](/payments/payment-methods/dynamic-payment-methods "Dynamic payment methods")

[Configure payment methods in Checkout studio

Use Checkout studio to manage the payment methods you use in your Checkout integration.

Private preview](/payments/checkout-studio/how-it-works "Configure payment methods in Checkout studio")

[A/B test payment methods

Launch an A/B test for a new payment method in the Dashboard.](/payments/a-b-testing "A/B test payment methods")

[Payment method rules

Control when payment methods are available to your customers.](/payments/payment-method-rules "Payment method rules")

[Payment method configurations

Create different sets of payment methods to display to customers based on specific checkout scenarios.](/payments/payment-method-configurations "Payment method configurations")

## Add Link for faster checkout

Use [Link](/payments/link) to let your customers select a saved payment method at checkout instead of entering payment information. Your customers can save their credit cards, debit cards, or US bank accounts for faster checkout at any Link-enabled business. Link also lets you accept [Instant Bank Payments](/payments/link/instant-bank-payments) and [Klarna](/payments/link/klarna).

[Link with Checkout

Use Link with the Stripe prebuilt payment page.](/payments/link/checkout-link "Link with Checkout")

[Link with Web Elements

Embed Link into your custom payment page for faster checkout.](/payments/link/elements-link "Link with Web Elements")

[Link with Mobile Elements

Add Link to your native iOS, Android, and React Native apps.](/payments/link/mobile-payment-element-link "Link with Mobile Elements")

## Integrate with a platform or a plugin

Stripe partners with thousands of popular platforms and supports plugins to bring Stripe payments into your website. See [all of our integration solutions](https://stripe.partners) in our online directory.

[![](https://b.stripecdn.com/docs-statics-srv/assets/shopify.46be6c6d99d048cf3e474fd714e4ab2d.svg)

Shopify

Sell online, on social media, and in person with a multichannel commerce platform.](https://stripe.com/partners/shopify "Shopify")

[![](https://b.stripecdn.com/docs-statics-srv/assets/squarespace.76289d1522a38199e1cff8bb5cebe8b3.svg)

Squarespace

Use Stripe payments on a single platform to sell your products.](https://stripe.com/partners/squarespace "Squarespace")

[![](https://b.stripecdn.com/docs-statics-srv/assets/adobe-commerce.b487cea9173211c13486b56ed545f11b.svg)

Adobe Commerce

Use the Stripe app for Adobe Commerce for accepting payments on Adobe Commerce.](/use-stripe-apps/adobe-commerce "Adobe Commerce")
