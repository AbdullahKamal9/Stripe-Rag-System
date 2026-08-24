# Source: https://docs.stripe.com/refunds

# Refund and cancel payments

## Learn how to cancel or refund a payment.

Ask about this page

Copy for LLMView as Markdown

Install tools

You can [cancel a payment](/refunds#cancel-payment) before it’s completed at no cost. Or you can refund all or part of a payment after it succeeds, which might incur a fee. Stripe’s processing fees from the original transaction aren’t returned. Go to our [pricing page](https://stripe.com/pricing/local-payment-methods) for more information.

Refunds use your available Stripe balance (not including pending amounts). If your available balance doesn’t cover the amount of the refund, Stripe holds the refund as pending for card transactions (refunds for other payment method types will fail) until your Stripe balance becomes sufficient. You can resolve a negative Stripe balance by collecting payments or topping up your account balance. In regions where applicable, Stripe might debit your bank accounts automatically to recover a negative Stripe balance.

## Refund requests

We submit refund requests to your customer’s bank or card issuer. Successful refunds appear on the bank statement of your customers in real time, depending on the card network and issuing bank. Disputes and chargebacks aren’t possible on credit card charges that are fully refunded.

If all of the following conditions apply, we send an email to your customer notifying them of the refund:

* The original charge was created on a customer in your Stripe account.
* The customer has a stored email address.
* You enabled **Email customers for refunds** in the [Dashboard](https://dashboard.stripe.com/account/emails).

You can [view your refunded payments in the Dashboard](https://dashboard.stripe.com/test/payments?status%5B0%5D=refunded&status%5B1%5D=refund_pending&status%5B2%5D=partially_refunded).

## Issue refunds

You can issue refunds by using the [Refunds API](/api/refunds) or the [Dashboard](https://dashboard.stripe.com/test/payments). You can issue more than one refund against a charge, but you can’t refund a total greater than the original charge amount.

Dashboard

API

To refund a payment using the Dashboard:

1. Find the payment you want to refund in the [Payments](https://dashboard.stripe.com/payments) page.
2. Click the overflow menu () to the right of the payment, then select **Refund payment**.
3. By default, you’ll issue a full refund. For a partial refund, enter a different refund amount.
4. Select a reason for the refund. If you select **Other**, you must add a note that explains the reason for the refund. Click **Refund**.

Alternatively, you can click a specific payment and issue a refund from its details page. You can also send [refund receipts](/receipts#refund-receipts) automatically or manually send a receipt for each refund.

#### Bulk refunds

The Dashboard supports the bulk refunding of full payments. Select what payments you want to refund by checking the box to the left of each payment—even over multiple pages of results. Then, click **Refund** and select a reason. You can only issue full refunds in this way; partial refunds must be issued individually.

### Refunds through a Connect platform

Refund behavior depends on the [Connect charge type](/connect/charges#refund-creation) used in your integration.

* Stripe debits the connected account directly for refunds to [direct charge](/connect/direct-charges#issue-refunds) payments.
* Stripe debits your platform for refunds to [destination charge](/connect/destination-charges#issue-refunds) or [separate charge and transfer](/connect/separate-charges-and-transfers#issue-refunds) (with or without `on_behalf_of`) payments. Reverse the transfers associated with these charge types to recover the refund amount from your connected accounts.

Connect platforms can enable their connected accounts to provide refunds to customers from their site by using Connect embedded components such as the [payments](/connect/supported-embedded-components/payments) or the [payment details](/connect/supported-embedded-components/payment-details) component.

## Refund destinations

Refunds can only be sent back to the original payment method used in a charge. You can’t send a refund to a different destination, such as another card or bank account.

Refunds to expired or canceled cards are handled by the customer’s card issuer and, in most cases, credited to the customer’s replacement card. If no replacement exists, the card issuer usually delivers the refund to the customer using an alternate method (for example, check or bank account deposit). In rare cases, a refund back to a card might [fail](#failed-refunds).

For other payment methods, like [ACH](/payments/ach-direct-debit) and [iDEAL](/payments/ideal), refund handling varies from bank to bank. If a customer has closed their method of payment, the bank might return the refund to us—at which point it’s marked as [failed](#failed-refunds).

#### Bank debit payment methods

For bank debit payment methods such as [SEPA Direct Debit](/payments/sepa-debit#refunds), [Bacs Direct Debit](/payments/payment-methods/bacs-debit#refunds), [ACH Direct Debit](/payments/ach-direct-debit#refunds), [ACSS (Canadian PADs)](/payments/acss-debit#refunds), [AU BECS Direct Debit](/payments/au-becs-debit#refunds), and [NZ bank account debits](/payments/nz-bank-account#refunds), there’s a risk of double refund. If you proactively issue a refund while the customer’s bank also initiates a dispute, the customer might receive two credits for the same transaction. Refer to the refund guidelines for each payment method to avoid this situation.

## Handle failed refunds

A refund can fail if the customer’s bank or card issuer can’t process it. For example, a closed bank account or a problem with the card can cause a refund to fail. When this happens, the bank returns the refunded amount to us and we add it back to your Stripe account balance. This process can take up to 30 days from the post date.

When using the API, a [Refund](/api#refund_object) object’s status transitions to `failed` and includes these attributes:

* `failure_balance_transaction`: The ID of the [balance transaction](/api#balance_transaction_object) representing the amount returned to your Stripe balance.
* `failure_reason`: The reason why the refund failed. These reasons include:

  | Failure reason | Description |
  | --- | --- |
  | `charge_for_pending_refund_disputed` | A customer disputed the charge while the refund is pending. In this case, we recommend [accepting or challenging](/disputes/responding#decide) the dispute instead of refunding to avoid duplicate reimbursements to the customer. |
  | `declined` | Refund declined by our financial partners. |
  | `expired_or_canceled_card` | Payment method is canceled by a customer or expired by the partner. |
  | `insufficient_funds` | Refund is pending due to insufficient funds and has crossed the pending refund expiry window. |
  | `lost_or_stolen_card` | Refund has failed due to loss or theft of the original card. |
  | `merchant_request` | Refund failed upon the business’s request. |
  | `unknown` | Refund has failed due to an unknown reason. |

For some payment methods, the decline code provided by our financial partners, which indicates the reason the refund failed, is available in the `network_decline_code` field of the `destination_details` hash:

```
{
  id: "pyr_1234",
  destination_details: {
    blik: {
      network_decline_code: "decline_code"
    },
    type: 'blik',
  }
}
```

In the rare instance that a refund fails, we notify you using the `refund.failed` [event](/event-destinations) (see [all refund-related events](#refund-events)). If this occurs, you need to arrange an alternative way to provide your customer with a refund.

If your platform uses [Connect with destination charges](/connect/destination-charges#issue-refunds), funds from a failed refund deposit to your platform account’s Stripe balance.

## Cancel a refund

Depending on the type of refund, you might be able to cancel a refund before it reaches the customer. Some card refunds support cancellation for a short period of time. The refund must not have been processed as a charge reversal. Only Dashboard cancellations are currently supported for card refunds.

For some [payment methods](/payments/bank-transfers#refunds), Stripe reaches out to the customer to collect banking information [before processing the refund](#requires-action). You can cancel these refunds while banking information hasn’t been collected. Both the API and Dashboard cancellations are supported for this type of refund.

Canceled refunds transition to a `canceled` status. As cancellations are a type of refund failure, the attributes `failure_reason` and `failure_balance_transaction` are included on the [Refund](/api#refund_object).

If your platform uses [Connect with destination charges](/connect/destination-charges#issue-refunds), funds from a canceled refund deposit to your platform account’s Stripe balance.

To cancel a refund using the Dashboard:

1. Find the payment associated with the refund in the [Payments](https://dashboard.stripe.com/payments) page.
2. Click the overflow menu () to the right of the payment, then select **Cancel refund**.
3. If there are multiple partial refunds, select the correct refund in the dropdown.
4. Confirm the refund cancellation by selecting **Yes, cancel refund**.

Alternatively, you can click a specific payment and cancel the refund from its details page.

## Refunds that require action

For some payment methods without native refund support (for example, Konbini, PromptPay, Boleto, and bank transfers), Stripe needs to collect bank account details from your customer before it can process the refund. In these cases, the refund enters the `requires_action` status and Stripe emails your customer to request their bank information.

When a refund has a status of `requires_action`, the [Refund](/api/refunds/object) object’s `next_action` property describes what the refund needs to continue processing. The `next_action` object contains these fields:

* `next_action.type`: The type of next action (for example, `display_details`).
* `next_action.display_details.email_sent`: Information about the email sent to the customer, including:
  + `email_sent_at`: The timestamp when the email was sent.
  + `email_sent_to`: The recipient’s email address.
* `next_action.display_details.expires_at`: The timestamp when the refund request expires if the customer doesn’t respond.

The refund status transitions as follows:

| Event | Refund status |
| --- | --- |
| Refund is created and customer is emailed | `requires_action` |
| Customer submits bank account details, and Stripe begins processing the refund | `pending` |
| Refund is expected to arrive in customer’s bank | `succeeded` |
| Customer’s bank returns the funds back to Stripe | `requires_action` |
| Customer doesn’t respond before the expiration threshold | `failed` |
| Refund is canceled while in `requires_action` state | `canceled` |

If the customer’s bank can’t successfully complete the transfer (for example, the account holder’s name doesn’t match or the bank account number has a typo), the funds are returned to Stripe and the refund transitions back to `requires_action`. In this case, Stripe emails the customer again to request corrected bank account details.

You can [cancel a refund](#cancel-refund) while it’s in the `requires_action` state. For example, if you want to arrange an alternative way to return funds to the customer.

## Refund and reversal

Some refunds—those issued shortly after the original charge—appear in the form of a reversal instead of a refund. In the case of a reversal, the original charge drops off the customer’s statement, and a separate credit isn’t issued.

[IC+](https://support.stripe.com/questions/understanding-blended-interchange-pricing) users might see a difference in cost between reversals and refunds because reversals usually incur lower network fees.

Dashboard

API

To verify if a refund goes through as a reversal on the Dashboard:

1. Open the payment details page of the payment associated with the refund.
2. In the Timeline, click **View Details** on the refund entry.
3. If it’s a reversal, a corresponding message displays.

## Trace a refund

After you initiate a refund, Stripe submits refund requests to your customer’s bank or card issuer. Your customer sees the refund as a credit approximately 5-10 business days later, depending upon the bank. A customer might contact you if they don’t see the refund. A refund might not be visible to the customer for several reasons:

* Refunds issued shortly after the original charge appear in the form of a reversal instead of a refund. In the case of a reversal, the original charge drops off the customer’s statement, and a separate credit isn’t issued.
* Refunds can fail if the customer’s bank or card issuer has been unable to process it correctly. The bank returns the refunded amount to us and we add it back to your Stripe account balance. This process can take up to 30 days from requesting the refund.

If a customer is asking about a refund, it can be helpful to give them the primary reference number corresponding to the refund. For card refunds, it can be an **Acquirer Reference Number (ARN)**, **System Trace Audit Number (STAN)**, or **Retrieval Reference Number (RRN)**. An ARN, STAN, or RRN is a reference number assigned to a card transaction as it moves through the payment flow. For local payment method refunds, it can be a reference number generated by Stripe or our financial partners which is propagated to the beneficiary banks or institutions. Your customer can then take this reference to their bank, which can provide more information about when the refund is available. Having a reference number can also increase your customer’s confidence that the refund has been initiated.

Refund references are available under the following conditions:

* They’re supported for some financial partners, and marked as unavailable otherwise.
* It takes up to 7 business days after initiating the refund to receive the ARN from downstream banking partners.
* An ARN isn’t available in the case of a reversal, since the original charge isn’t processed. For card networks that don’t support ARNs, we attempt to provide other references such as System Trace Audit Number (STAN) or Retrieval Reference Number (RRN).

Dashboard

API

To find the reference of a refund using the Dashboard:

1. Open the payment details page of the payment associated with the refund.
2. In the Timeline, click **View Details** on the refund entry.
3. Where available, Stripe shows the ARN or STAN on the clipboard.

## Cancel a payment

You can cancel a payment using the Dashboard when its status is `uncaptured`, or when it’s a debit payment that hasn’t been posted to the bank yet. To cancel a payment with other statuses, you must use the API.

Dashboard

API

To cancel payments using the Dashboard:

1. Find the payment you want to cancel in the [Payments](https://dashboard.stripe.com/payments) page.
2. Click the payment, then select **Cancel**.
3. Select a reason for canceling, then click **Yes**. If you select **Other**, you must add a note that explains the reason for canceling the payment.

You can cancel a payment from the Dashboard when:

* The payment status is `uncaptured`.
* The payment is a debit payment that hasn’t been posted to the bank yet.

## Refund events

Stripe triggers [events](/api/events#events) every time a refund is created or changed. Some other actions, like reviews closing, also trigger events that are relevant to refunds.

Make sure that your integration is set up to [handle events](/webhooks/handling-payment-events) and that you [verify webhook signatures](/webhooks#verify-events) to confirm that incoming events are from Stripe. You must also build internal logic for notifying customers or your team about the state of the refund process. At a minimum, Stripe recommends that you listen for the `refund.created` event.

The following table describes the most common events related to refunds.

| Event | Description |
| --- | --- |
|  | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| `refund.created` | Sent when a refund is created. |
| `refund.updated` | Sent when the refund is updated. Updates include adding metadata and providing details like the [ARN as a reference number to trace refunds](#tracing-refunds). |
| `refund.failed` | Sent when a [refund has failed](#failed-refunds). |
| `charge.dispute.funds_reinstated` | Sent when funds are reinstated to your account after a dispute is closed, including [partially refunded payments](/disputes/best-practices#partial-refund-bp). |
| `charge.refunded` | Sent when a charge is refunded, including partial refunds. Listen to `refund.created` for information about the refund. |
| `review.closed` | Sent when a [review](/api/events/types#review_object) is closed. See the `reason` field to understand why it was closed, one of: `approved`, `disputed`, `canceled`, `refunded`, or `refunded_as_fraud`. |
| `source.refund_attributes_required` Deprecated | Sent when the receiver source requires refund attributes to process a refund or a mispayment. |
| `charge.refund.updated` Deprecated | Sent when the refund is updated, only for refunds with a corresponding charge. Listen to `refund.updated` for updates on all refunds instead. |

## Cost optimization

If your business processes a large volume of refunds close to the time of transaction, we recommend using [manual authorization and capture](/payments/place-a-hold-on-a-payment-method) to reduce your refund costs. Manual authorization and capture lets you better control costs by canceling payments before they’re captured, or by reducing your captured amount rather than processing a refund.

## See also

* [Add funds to your Stripe balance](/get-started/account/add-funds)
* [Add funds to your platform balance](/connect/top-ups)
* [Localize prices](/payments/currencies/localize-prices)
