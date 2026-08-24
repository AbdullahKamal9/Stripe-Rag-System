# Source: https://docs.stripe.com/payments/checkout

# Build a payments page

## Create a payments page with prebuilt UIs using the Checkout Sessions API.

[CHECKOUT](/payments/checkout)

Accept payments on your website

Accept one-time and subscription payments from more than 125 local payment methods.

[Start building your checkout integration](/checkout/quickstart)

![](https://b.stripecdn.com/docs-statics-srv/assets/checkout-ui-breakdown.c80c7d5de0ab96ef9ad7e3d6f160f237.png)

## Stripe Checkout

You can use three payment UIs with the Checkout Sessions API. The following images highlight which parts of the checkout UI Stripe hosts for each option. To build and manage these integrations, use [Checkout studio](/payments/checkout-studio).

![Full page](https://b.stripecdn.com/docs-statics-srv/assets/checkout-hosted-hover.6ee5a154986ffc216c034a47b7b0d65e.png)

[Full page](/checkout/quickstart): Customers enter their payment details in a fully-featured payment page, either embedded on your site or via a redirect to a Stripe-hosted page.

![Embedded form](https://b.stripecdn.com/docs-statics-srv/assets/checkout-form-hover.31c41716c4857e5e01f77978530fc573.png)

[Embedded form](/payments/checkout/how-checkout-works?payment-ui=checkout-form): Customers enter their payment details in an embedded form on your site without redirection.

![Elements](https://b.stripecdn.com/docs-statics-srv/assets/checkout-elements-hover.28148f5be39600e85ef4784ab9e873e7.png)

[Elements](/payments/quickstart-checkout-sessions): Build a fully customized payment page using elements

|  | [FULL PAGE](/payments/accept-a-payment?payment-ui=checkout&ui=stripe-hosted) Recommended | [EMBEDDED FORM](/payments/checkout/how-checkout-works?payment-ui=checkout-form) Private preview | [ELEMENTS](/payments/accept-a-payment?payment-ui=elements&api-integration=checkout) |
| --- | --- | --- | --- |
| **API** | [Checkout Sessions](/api/checkout/sessions) | [Checkout Sessions](/api/checkout/sessions) | [Checkout Sessions](/api/checkout/sessions) |
| **Feature list** | Built-in UI support for Billing, Tax, Adaptive Pricing, Stripe Managed Payments, Link, dynamic payment methods, Surcharging, Split-tender | Built-in UI support for Billing, Tax, Adaptive Pricing, Stripe Managed Payments, Link, dynamic payment methods, Surcharging | Built-in UI support for Adaptive Pricing, Link, dynamic payment methods |
| **Order summary** | Includes full order summary with subtotals (including tax and shipping costs), cross-sells & upsells, free trials, discounts and promo codes | Limited order summary with subtotals (including tax and shipping costs), discounts and promo codes | No order summary |
| **Ongoing maintenance required** |  |  |  |
| **Hosting** | Hosted or Embedded | Embedded | Embedded |
| **Complexity** | Low | Some | Most |
| **Customization** | 15 configurable settings via brand settings | 70 configurable settings via the Appearance API | Full CSS customization via the Appearance API |

## Customize checkout

[Customize the look and feel

Customize the appearance and behavior of the checkout flow.](/payments/checkout/customization "Customize the look and feel")

[Collect additional information

Collect shipping details and other customer information during checkout.](/payments/checkout/collect-additional-info "Collect additional information")

[Collect taxes

Collect taxes for one-time payments in Stripe Checkout.](/payments/checkout/taxes "Collect taxes")

[Dynamically update checkout

Make updates while your customer checks out.](/payments/checkout/dynamic-updates "Dynamically update checkout")

[Extend checkout with custom components

Add custom components to your payment form.](/payments/checkout/custom-components "Extend checkout with custom components")

[Add trials, discounts, and upsells

Add promotions, such as trials, discounts, and optional items.](/payments/checkout/promotions "Add trials, discounts, and upsells")

## Change when and how you collect payment

[Set up subscriptions

Create a subscription with recurring payments for your customers.](/payments/subscriptions "Set up subscriptions")

[Set up future payments

Save your customers’ payment details to charge them later.](/payments/checkout/save-and-reuse "Set up future payments")

[Save payment details during payment

Accept a payment and save your customer’s payment details for future purchases.](/payments/checkout/save-during-payment "Save payment details during payment")

[Let customers pay in their local currency

Use Adaptive Pricing to allow customers to pay in their local currency.](/payments/currencies/localize-prices/adaptive-pricing "Let customers pay in their local currency")

[Set up Managed Payments

Let Stripe handle sales tax and VAT compliance in more than 80 countries, including customer support, and help with fraud and disputes.](/payments/managed-payments/how-it-works "Set up Managed Payments")

## Manage your business

[Manage your product catalog

Handle your inventory and fulfillment with Checkout.](/payments/checkout/product-catalog "Manage your product catalog")

[Migrate payment methods to the Dashboard

Migrate the management of your payment methods to the Dashboard.](/payments/dashboard-payment-methods "Migrate payment methods to the Dashboard")

[After the payment

Customize the post-payment checkout process.](/payments/checkout/after-the-payment "After the payment")
