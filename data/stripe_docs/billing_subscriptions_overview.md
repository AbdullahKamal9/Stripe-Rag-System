# Source: https://docs.stripe.com/billing/subscriptions/overview

# How subscriptions work

## Manage recurring payments and subscription lifecycles.

Ask about this page

Copy for LLMView as Markdown

Install tools

Subscriptions let customers make recurring payments to access a product or service. When you create a subscription, Stripe automatically generates invoices, attempts payment collection, and manages the subscription status throughout its lifecycle. A subscription moves through a predictable set of states, from creation to cancellation.

Unlike one-time payments, subscriptions require storing customer and payment method information for future billing cycles. Stripe handles the payment retry logic, dunning, and status transitions.

## Subscription lifecycle

Each of the following subscription lifecycle phases maps to a status change on the [Subscription object](/api/subscriptions/object). Understanding these statuses helps you know when to provision access, notify customers, and handle errors. You can use [webhook events](/billing/subscriptions/webhooks#state-changes) to monitor and handle transitions between statuses.

### Create the subscription

Create a new subscription in the [Dashboard](https://dashboard.stripe.com/subscriptions?status=active) or with the [Subscriptions API](/api/subscriptions/create). The resulting [Subscription object](/api/subscriptions/object) contains the subscribed customer, [product](/api/products), and [price](/api/prices/object), and the `status` reflecting the subscription’s current lifecycle state.

When you create a subscription that requires an immediate payment, Stripe also creates an [Invoice](/billing/invoices/subscription) and a [PaymentIntent](/payments/payment-intents). The subscription’s initial status is `incomplete`, then becomes `active` after the customer pays the first invoice.

Default subscription payment collection and failure handling depends on the payment method. In the API, you can configure a subscription’s [payment\_behavior](/api/subscriptions/create#create_subscription-payment_behavior) to override the default.

If you create a [trial period](/billing/subscriptions/trials) to delay the first charge for the subscription, the initial status is `trialing`, and the subscription automatically transitions to `active` when the trial ends and payment succeeds.

### Handle the invoice

For subscriptions with `collection_method` set to `charge_automatically`, Stripe creates an [invoice](/billing/invoices/subscription) with the status `open` when you create the subscription. Your customer has 23 hours to pay. During this time, the subscription status is `incomplete` and the invoice status remains `open`. This 23-hour window accommodates customers who pay while on-session. If the customer returns to your application after 23 hours, create a new subscription for them.

For subscriptions with `collection_method` set to `send_invoice`, Stripe emails the customer a link to the invoice with a configurable due date. The subscription remains `incomplete` until the customer pays.

To learn more, see [Subscription invoices](/billing/invoices/subscription).

### Confirm payment

If your customer pays the invoice, the subscription updates to `active` and the invoice to `paid`. Listen for the [invoice.paid](/billing/subscriptions/webhooks#events) event or confirm that the subscription status is `active`.

If the customer doesn’t pay within 23 hours, the subscription updates to `incomplete_expired` and the invoice becomes `void`. To reactivate their access, create a new subscription.

For more details, see [Subscription statuses](#subscription-statuses) and [Payment statuses](#payment-status).

### Provision access to your product

When a subscription becomes `active`, Stripe creates an active [entitlement](/billing/entitlements) for each feature associated with the subscribed product. When a customer accesses your services, use their active entitlements to grant them access to the features included in their subscription.

Alternatively, [track active subscriptions](/billing/subscriptions/webhooks#active-subscriptions) with webhook events and provision the product for the customer based on that activity.

### Update the subscription

You can [modify existing subscriptions](/billing/subscriptions/change) as needed without having to cancel and recreate them. Some of the most significant changes you might make are [upgrading or downgrading](/billing/subscriptions/change-price) the subscription price or [pausing payment collection](/billing/subscriptions/pause-payment) for an active subscription.

For [Stripe Checkout](/payments/checkout) integrations, you can’t update the subscription or its invoice if the session’s subscription is `incomplete`. You can listen to the [checkout.session.completed](/api/events/types#event_types-checkout.session.completed) event to make the update after the session has completed. You can also [expire the session](/api/checkout/sessions/expire) instead if you want to cancel the session’s subscription, void the subscription invoice, or mark the invoice as uncollectible.

### Handle unpaid subscriptions

If the customer doesn’t pay a subscription invoice, Stripe pauses further collection attempts. The subscription continues to generate invoices each billing period, which remain in `draft` status. The subscription’s status (`past_due` or `unpaid`) depends on your [failed payment settings](https://dashboard.stripe.com/settings/billing/automatic) in the Dashboard.

Stripe ignores voided invoices when determining subscription status and uses the most recent non-voided invoice instead.

To learn more, see [Failed subscription payments](/billing/collection-method#failed-subscription-payments).

### Cancel the subscription

You can [cancel](/billing/subscriptions/cancel) a subscription at any time, including at the [end of a billing cycle](/billing/subscriptions/cancel#cancel-at-the-end-of-the-current-billing-period) or after a [set number of billing cycles](/billing/subscriptions/cancel#subscription-schedules).

By default, canceling a subscription disables creating new invoices and [stops automatic collection](/billing/subscriptions/cancel#handle-invoice-items-when-canceling-subscriptions) of all outstanding invoices from the subscription. It also deletes the subscription and you can no longer update it except for its [metadata](/metadata) and `cancellation_details`. If your customer wants to resubscribe, you need to collect new payment information from them and create a new subscription.

## Subscription statuses

Subscriptions can have the following statuses. The actions you can take on a subscription depend on its status.

| Status | Description |
| --- | --- |
| `trialing` | The subscription is currently in a trial period and you can safely provision your product for your customer. The subscription transitions automatically to `active` when a customer makes the first payment. |
| `active` | The subscription is in good standing. For `past_due` subscriptions, paying the latest associated invoice or marking it uncollectible transitions the subscription to `active`. Note that `active` doesn’t indicate that all outstanding invoices associated with the subscription have been paid. You can leave other outstanding invoices open for payment, mark them as uncollectible, or void them as you see fit. |
| `incomplete` | The customer must make a successful payment within 23 hours to activate the subscription. Or the payment [requires action](#requires-action), such as customer authentication. Subscriptions can also be `incomplete` if there’s a pending payment and the PaymentIntent status is `processing`. |
| `incomplete_expired` | The initial payment on the subscription failed and the customer didn’t make a successful payment within 23 hours of subscription creation. These subscriptions don’t bill customers. This status exists so you can track customers that failed to activate their subscriptions. |
| `past_due` | Payment on the latest *finalized* invoice either failed or wasn’t attempted. The subscription continues to create invoices. Your Dashboard [subscription settings](https://dashboard.stripe.com/settings/billing/automatic) determine the subscription’s next status. If the invoice is still unpaid after all attempted [smart retries](/billing/revenue-recovery/smart-retries), you can configure the subscription to move to `canceled`, `unpaid`, or leave it as `past_due`. To reactivate the subscription, have your customer pay the most recent invoice. The subscription status becomes `active` regardless of whether the payment is done before or after the latest invoice due date. |
| `canceled` | The subscription was canceled. During cancellation, automatic collection for all unpaid invoices is disabled (`auto_advance=false`). This is a terminal state that can’t be updated. |
| `unpaid` | The latest invoice hasn’t been paid but the subscription remains in place. The latest invoice remains open and invoices continue to generate, but payments aren’t attempted. Revoke access to your product when the subscription is `unpaid` because payments were already attempted and retried while `past_due`. To move the subscription to `active`, pay the most recent invoice before its due date. |
| `paused` | The subscription has ended its trial period without a default payment method and the [trial\_settings.end\_behavior.missing\_payment\_method](/billing/subscriptions/trials/free-trials#create-free-trials-without-payment) is set to `pause`. Invoices are no longer created for the subscription. After attaching a default payment method to the customer, you can [resume the subscription](/billing/subscriptions/trials/free-trials#resume-a-paused-subscription). |

## Payment statuses

A [PaymentIntent](/payments/payment-intents) tracks the lifecycle of every payment. Whenever a payment is due for a subscription, Stripe generates an [invoice](/billing/invoices/subscription) and a PaymentIntent. The PaymentIntent ID attaches to the invoice and you can access it from the Invoice and Subscription objects.

The status of the PaymentIntent affects the status of the invoice and the subscription. Here’s how the different outcomes of a payment map to the different statuses:

| Payment outcome | PaymentIntent status | Invoice status | Subscription status |
| --- | --- | --- | --- |
| Success | `succeeded` | `paid` | `active` |
| Fails because of a card error | `requires_payment_method` | `open` | `incomplete` |
| Fails because of authentication | `requires_action` | `open` | `incomplete` |

Asynchronous payment methods, such as ACH Direct Debit, handle subscription status transitions differently from immediate payment methods. When you use an asynchronous payment method, a subscription can move directly to `active` after creation and bypass `incomplete`. If the payment fails later, Stripe voids the invoice but the subscription remains `active`. Use this behavior when you design your access control and retry logic.

The following sections explain these statuses and the actions to take for each.

### Payment succeeded

When the customer’s payment is successful:

* The `status` of the PaymentIntent moves to `succeeded`.
* The `status` of the subscription is `active`.
* The `status` of the invoice is `paid`.
* Stripe sends an `invoice.paid` event to your configured webhook endpoints.

For [payment methods](/payments/payment-methods/integration-options) with longer processing periods, subscriptions are immediately activated. In these cases, the status of the PaymentIntent might be `processing` for an `active` subscription until the payment succeeds.

With your subscription now activated, [provision access](#provision-access) to your product.

### Requires payment method

If payment fails because of a [card error](/api/errors#errors-card_error) such as a [decline](/declines#issuer-declines):

* The `status` of the PaymentIntent is `requires_payment_method`.
* The `status` of the subscription is `incomplete`.
* The `status` of the invoice is `open`.

To handle these scenarios:

* Notify the customer.
* Collect new payment information and [confirm the PaymentIntent](/api/payment_intents/confirm).
* Update the [default payment method](/api/subscriptions/object#subscription_object-default_payment_method) on the subscription.
* Stripe re-attempts payment using [Smart Retries](/invoicing/automatic-collection#smart-retries) or based on your custom [retry rules](https://dashboard.stripe.com/account/billing/automatic).
* Use the [invoice.payment\_failed](/billing/revenue-recovery/smart-retries#invoice-payment-failed-webhook) event to monitor subscription payment failure events and retry attempt updates. After a payment attempt on an invoice, its [next\_payment\_attempt](/api#invoice_object-next_payment_attempt) value is set using the current subscription settings in your Dashboard.

Learn how to [handle payment failures for subscriptions](/billing/subscriptions/webhooks#payment-failures).

### Requires action

Some payment methods require customer authentication with [3D Secure](/payments/3d-secure) (3DS). Whether authentication is required depends on your [Radar rules](/payments/3d-secure/authentication-flow#three-ds-radar) and the issuing bank for the card.

If payment fails because the customer needs to authenticate a payment:

* The `status` of the PaymentIntent is `requires_action`.
* The `status` of the subscription is `incomplete`.
* The `status` of the invoice is `open`.

To handle these scenarios:

* Monitor for the `invoice.payment_action_required` event notification with [webhook endpoints](/billing/subscriptions/webhooks). This indicates that authentication is required.
* Notify your customer that they must authenticate.
* Retrieve the client secret for the PaymentIntent and pass it in a call to [stripe.ConfirmCardPayment](/js/payment_intents/confirm_card_payment). This displays an authentication modal to your customers, attempts payment, then closes the modal and returns context to your application.
* Monitor the `invoice.paid` event on your event destination to verify that the payment succeeded. Users can leave your application before `confirmCardPayment()` finishes. Verifying whether the payment succeeded allows you to correctly provision your product.

## See also

* [Design a subscriptions integration](/billing/subscriptions/design-an-integration)
* [Build a subscriptions integration](/billing/subscriptions/build-subscriptions)
* [Subscriptions quickstart](/billing/quickstart)
