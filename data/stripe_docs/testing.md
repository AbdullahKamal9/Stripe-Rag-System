# Source: https://docs.stripe.com/testing

# Testing

## Simulate payments to test your integration.

Ask about this page

Copy for LLMView as Markdown

Install tools

Test your integration in a [sandbox](/sandboxes) by simulating transactions with test values—these transactions don’t move funds.

You can access your sandboxes using the account picker in the [Dashboard](https://dashboard.stripe.com/sandboxes).

Test cards act as “fake” credit cards, and allow you to simulate the following scenarios:

* Successful payments by [card brand](#cards) or [country](#international-cards)
* Card errors due to [declines](#declined-payments), [fraud](#fraud-prevention), or [invalid data](#trigger-an-error-with-invalid-data)
* [Disputes](#disputes) and [refunds](/testing#refunds)
* Authentication with [3D Secure](#regulatory-cards) and [PINs](#terminal)

You can also test non-card payments in a sandbox. Non-card payments are payment methods that aren’t credit or debit cards. Stripe supports various non-card payment options, such as digital wallets and bank transfers. [Each payment method](#non-card-payments) has its own special values.

Don’t use testing environments to load test your integration because you might hit [rate limits](/testing#rate-limits). To load test your integration, see [load testing](/rate-limits#load-testing).

## How to use test cards

When you work with a test card, use [test API keys](/keys#obtain-api-keys) in all API calls. This is true whether you’re serving a payment form to test interactively or writing test code.

#### Don't use real card details

Don’t use real card details. The [Stripe Services Agreement](https://stripe.com/legal/ssa#1-your-stripe-account) prohibits testing in live mode using real payment method details. Use your test API keys and the card numbers below.

### Testing interactively

When testing interactively, use a card number, such as [4242 4242 4242 4242](/testing?testing-method=card-numbers#visa). Enter the card number in the Dashboard or in any payment form.

* Use a valid future date, such as **12/34**.
* Use any three-digit CVC (four digits for American Express cards).
* Use any value you like for other form fields.

### Test code

When writing test code, use a `PaymentMethod` such as [pm\_card\_visa](/testing?testing-method=payment-methods#visa) instead of a card number. We don’t recommend using card numbers directly in API calls or server-side code, even in testing environments. If you use them, your code might not be PCI-compliant when you go live. By default, a `PaymentMethod` isn’t attached to a [Customer](/api/customers).

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
  -d amount=500 \
  -d currency=gbp \
  -d payment_method=pm_card_visa \
  -d "payment_method_types[]=card"
```

When you’re ready to take your integration live, replace your test publishable and secret [API keys](/keys) with live ones.

You can’t process live payments if your integration is still using your test API keys. Store live API keys in a secrets vault or environment variables. Don’t store keys in source code or configuration files checked into version control. To learn how to use live keys safely, see [Best practices for managing secret API keys](/keys-best-practices).

## Simulate a payment by card brand

To simulate a successful payment for a specific card brand, use test cards from the following list.

Cross-border fees are assessed based on the country of the card issuer. Cards where the issuer country isn’t the US (such as JCB and UnionPay) might be subject to a cross-border fee, even in testing environments.

Card numbers

PaymentMethods

Tokens

| Brand | Number | CVC | Date |
| --- | --- | --- | --- |
|  | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| Visa | 4242424242424242 | Any 3 digits | Any future date |
| Visa (debit) | 4000056655665556 | Any 3 digits | Any future date |
| Mastercard | 5555555555554444 | Any 3 digits | Any future date |
| Mastercard (2-series) | 2223003122003222 | Any 3 digits | Any future date |
| Mastercard (debit) | 5200828282828210 | Any 3 digits | Any future date |
| Mastercard (prepaid) | 5105105105105100 | Any 3 digits | Any future date |
| American Express | 378282246310005 | Any 4 digits | Any future date |
| American Express | 371449635398431 | Any 4 digits | Any future date |
| Discover | 6011111111111117 | Any 3 digits | Any future date |
| Discover | 6011000990139424 | Any 3 digits | Any future date |
| Discover (debit) | 6011981111111113 | Any 3 digits | Any future date |
| Diners Club | 3056930009020004 | Any 3 digits | Any future date |
| Diners Club (14-digit card) | 36227206271667 | Any 3 digits | Any future date |
| BCcard and DinaCard | 6555900000604105 | Any 3 digits | Any future date |
| JCB | 3566002020360505 | Any 3 digits | Any future date |
| UnionPay | 6200000000000005 | Any 3 digits | Any future date |
| UnionPay (debit) | 6200000000000047 | Any 3 digits | Any future date |
| UnionPay (19-digit card) | 6205500000000000004 | Any 3 digits | Any future date |

Most Cartes Bancaires and eftpos cards are co-branded with either Visa or Mastercard. The test cards in the following table simulate successful payments with co-branded cards.

Card numbers

PaymentMethods

Tokens

| Brand/Co-brand | Number | CVC | Date |
| --- | --- | --- | --- |
| Cartes Bancaires/Visa | 4000002500001001 | Any 3 digits | Any future date |
| Cartes Bancaires/Mastercard | 5555552500001001 | Any 3 digits | Any future date |
| eftpos Australia/Visa | 4000050360000001 | Any 3 digits | Any future date |
| eftpos Australia/Mastercard | 5555050360000080 | Any 3 digits | Any future date |

## Simulate a payment by country

To simulate successful payments from specific countries, use test cards from the following sections.

#### Security tip

[Strong Customer Authentication](/strong-customer-authentication) regulations require [3D Secure](/payments/3d-secure) authentication for online payments within the [European Economic Area](https://en.wikipedia.org/wiki/European_Economic_Area). The test cards in the Europe and Middle East section simulate a payment that succeeds without authentication. We also recommend testing authentication scenarios using [3D Secure test cards](/testing#regulatory-cards).

Card numbers

PaymentMethods

Tokens

| Country | Number | Brand |
| --- | --- | --- |
|  | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| **AMERICAS** | | |
| United States (US) | 4242424242424242 | Visa |
| Argentina (AR) | 4000000320000021 | Visa |
| Brazil (BR) | 4000000760000002 | Visa |
| Canada (CA) | 4000001240000000 | Visa |
| Chile (CL) | 4000001520000001 | Visa |
| Colombia (CO) | 4000001700000003 | Visa |
| Costa Rica (CR) | 4000001880000005 | Visa |
| Ecuador (EC) | 4000002180000000 | Visa |
| Mexico (MX) | 4000004840008001 | Visa |
| Mexico (MX) | 5062210000000009 | Carnet |
| Panama (PA) | 4000005910000000 | Visa |
| Paraguay (PY) | 4000006000000066 | Visa |
| Peru (PE) | 4000006040000068 | Visa |
| Uruguay (UY) | 4000008580000003 | Visa |
| **EUROPE and MIDDLE EAST** | | |
| United Arab Emirates (AE) | 4000007840000001 | Visa |
| United Arab Emirates (AE) | 5200007840000022 | Mastercard |
| Austria (AT) | 4000000400000008 | Visa |
| Belgium (BE) | 4000000560000004 | Visa |
| Bulgaria (BG) | 4000001000000000 | Visa |
| Belarus (BY) | 4000001120000005 | Visa |
| Croatia (HR) | 4000001910000009 | Visa |
| Cyprus (CY) | 4000001960000008 | Visa |
| Czech Republic (CZ) | 4000002030000002 | Visa |
| Denmark (DK) | 4000002080000001 | Visa |
| Estonia (EE) | 4000002330000009 | Visa |
| Finland (FI) | 4000002460000001 | Visa |
| France (FR) | 4000002500000003 | Visa |
| Germany (DE) | 4000002760000016 | Visa |
| Gibraltar (GI) | 4000002920000005 | Visa |
| Greece (GR) | 4000003000000030 | Visa |
| Hungary (HU) | 4000003480000005 | Visa |
| Ireland (IE) | 4000003720000005 | Visa |
| Italy (IT) | 4000003800000008 | Visa |
| Latvia (LV) | 4000004280000005 | Visa |
| Liechtenstein (LI) | 4000004380000004 | Visa |
| Lithuania (LT) | 4000004400000000 | Visa |
| Luxembourg (LU) | 4000004420000006 | Visa |
| Malta (MT) | 4000004700000007 | Visa |
| Netherlands (NL) | 4000005280000002 | Visa |
| Norway (NO) | 4000005780000007 | Visa |
| Poland (PL) | 4000006160000005 | Visa |
| Portugal (PT) | 4000006200000007 | Visa |
| Romania (RO) | 4000006420000001 | Visa |
| Saudi Arabia (SA) | 4000006820000007 | Visa |
| Slovenia (SI) | 4000007050000006 | Visa |
| Slovakia (SK) | 4000007030000001 | Visa |
| Spain (ES) | 4000007240000007 | Visa |
| Sweden (SE) | 4000007520000008 | Visa |
| Switzerland (CH) | 4000007560000009 | Visa |
| United Kingdom (GB) | 4000008260000000 | Visa |
| United Kingdom (GB) | 4000058260000005 | Visa (debit) |
| United Kingdom (GB) | 5555558265554449 | Mastercard |
| **ASIA PACIFIC**  Regional considerations India  To test subscriptions that require mandates and pre-debit notifications, see [India recurring payments](/india-recurring-payments?integration=paymentIntents-setupIntents#testing). | | |
| Australia (AU) | 4000000360000006 | Visa |
| China (CN) | 4000001560000002 | Visa |
| Hong Kong (HK) | 4000003440000004 | Visa |
| India (IN) | 4000003560000008 | Visa |
| Japan (JP) | 4000003920000003 | Visa |
| Japan (JP) | 3530111333300000 | JCB |
| Malaysia (MY) | 4000004580000002 | Visa |
| New Zealand (NZ) | 4000005540000008 | Visa |
| Singapore (SG) | 4000007020000003 | Visa |
| Taiwan (TW) | 4000001580000008 | Visa |
| Thailand (TH) | 4000007640000003 | Visa (credit) |
| Thailand (TH) | 4000057640000008 | Visa (debit) |

### Simulate customer location with email

When testing [Checkout Sessions](/payments/checkout), [Payment Links](/payment-links), or [pricing tables](/payments/checkout/pricing-table), you can simulate a customer’s geographic location by using a location-formatted email address. Add a `+location_XX` suffix to the local part of any email address, where `XX` is a valid two-letter [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) country code.

For example, to simulate a customer located in the United States, pass `test+location_US@example.com` as the `customer_email` parameter when creating a Checkout Session and as the `prefilled_email` [URL parameter](/payment-links/customize#customize-checkout-with-url-parameters) when creating a Payment Link.

When you visit the resulting Checkout Session URL, you see the same currency and payment methods that a customer in the specified country would see. Learn more about [testing with location-formatted emails](/payments/currencies/localize-prices/adaptive-pricing#testing).

## Simulate an HSA or FSA card payment

Below are test card numbers for simulating transactions using a health savings account (HSA) and a flexible spending account (FSA). These accounts are commonly used for medical expenses, and testing with them ensures proper handling of healthcare-related transactions within your application.

Card numbers

PaymentMethods

| Brand/Type | Number | CVC | Date |
| --- | --- | --- | --- |
| Visa FSA | 4000051230000072 | Any 3 digits | Any future date |
| Visa HSA | 4000051230000072 | Any 3 digits | Any future date |
| Mastercard FSA | 5200828282828897 | Any 3 digits | Any future date |

## Simulate a declined payment

To test your integration’s error-handling logic by simulating payments that the issuer declines for various reasons, use test cards from this section. These cards return a [card error](/error-handling#payment-errors) with the listed [error code](/error-codes) and [decline code](/declines/codes).

Provide a CVC when you test CVC behavior. Stripe skips the CVC check if you omit it, so the check can’t fail. To simulate an incorrect CVC, use the “Incorrect CVC decline” test card listed in the following table and provide any three-digit CVC.

Card numbers

PaymentMethods

Tokens

| Description | Number | Error code | Decline code |
| --- | --- | --- | --- |
|  | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| Generic decline | 4000000000000002 | [card\_declined](/error-codes#card-declined) | [generic\_decline](/declines/codes#generic_decline) |
| Insufficient funds decline | 4000000000009995 | [card\_declined](/error-codes#card-declined) | [insufficient\_funds](/declines/codes#insufficient_funds) |
| Lost card decline | 4000000000009987 | [card\_declined](/error-codes#card-declined) | [lost\_card](/declines/codes#lost_card) |
| Stolen card decline | 4000000000009979 | [card\_declined](/error-codes#card-declined) | [stolen\_card](/declines/codes#stolen_card) |
| Expired card decline | 4000000000000069 | [expired\_card](/error-codes#expired-card) | n/a |
| Incorrect CVC decline | 4000000000000127 | [incorrect\_cvc](/declines/codes#incorrect_cvc) | n/a |
| Processing error decline | 4000000000000119 | [processing\_error](/error-codes#processing-error) | n/a |
| Incorrect number decline | 4242424242424241 | [incorrect\_number](/declines/codes#incorrect_number) | n/a |
| Exceeding velocity limit decline | 4000000000006975 | [card\_declined](/error-codes#card-declined) | [card\_velocity\_exceeded](/declines/codes#card_velocity_exceeded) |

You can’t attach cards that simulate issuer declines to a `Customer` object. To simulate a declined payment with an attached card, use the “Decline after attaching” test card listed in the following table.

| Description | Number | Details |
| --- | --- | --- |
| Decline after attaching | 4000000000000341 | Attaching this card to a [Customer](/api/customers) object succeeds, but attempts to charge the customer fail. |

## Fraud prevention

Stripe’s fraud prevention system, Radar, can block payments when they have a high risk level or fail verification checks. You can use the cards in this section to test your Radar settings. You can also use them to test how your integration responds to blocked payments.

Each card simulates specific risk factors. Your Radar settings determine which risk factors cause it to block a payment. Blocked payments result in [card errors with an error code of fraud](/error-handling).

To trigger a failed CVC check, include a CVC (any three-digit number). To trigger a failed postal code check, include any valid postal code. If you omit these fields, Radar skips those checks, so they can’t fail.

Card numbers

PaymentMethods

Tokens

| Description | Number | Details |
| --- | --- | --- |
|  | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| Always blocked | 4100000000000019 | The charge has a [risk level of “highest”](/radar/risk-evaluation#high-risk)  Radar always blocks it. |
| Highest risk | 4000000000004954 | The charge has a [risk level of “highest”](/radar/risk-evaluation#high-risk)  Radar might block it [depending on your settings](/radar/risk-settings). |
| Elevated risk | 4000000000009235 | The charge has a [risk level of “elevated”](/radar/risk-evaluation#elevated-risk)  If you use Radar for Fraud Teams, Radar might [queue it for review](/radar/reviews). |
| High fraud dispute score | 4000008400000407 | This charge has a high fraud dispute score.  Radar might block it [depending on your settings](/radar/risk-settings). |
| High early fraud warning score | 4000008400000159 | This charge has a high early fraud warning score.  Radar might block it [depending on your settings](/radar/risk-settings). |
| Dynamic risk threshold | 4000008400001017 | This charge triggers the Radar Dynamic risk threshold control, when enabled.  Radar blocks the transaction if you enable the [Dynamic risk threshold](/radar/risk-settings#dynamic-risk-threshold). |
| Adaptive 3DS | 4000008405600003 | This charge triggers the Radar Adaptive 3DS risk control, when enabled.  If you enable Adaptive 3DS, Radar requests 3DS authentication when using this test card. |
| CVC check fails | 4000000000000101 | If you provide a CVC number, the CVC check fails.  Radar might block it [depending on your settings.](/radar/rules#traditional-bank-checks) |
| Postal code check fails | 4000000000000036 | If you provide a postal code, the postal code check fails.  Radar might block it [depending on your settings.](/radar/rules#traditional-bank-checks) |
| CVC check fails with elevated risk | 4000058400307872 | If you provide a CVC number, the CVC check fails with a [risk level of “elevated”](/radar/risk-evaluation#elevated-risk)  Radar might block it [depending on your settings.](/radar/rules#traditional-bank-checks) |
| Postal code check fails with elevated risk | 4000058400306072 | If you provide a postal code, the postal code check fails with a [risk level of “elevated”](/radar/risk-evaluation#elevated-risk)  Radar might block it [depending on your settings](/radar/rules#traditional-bank-checks). |
| Line1 check fails | 4000000000000028 | The address line 1 check fails.  The payment succeeds unless you [block it with a custom Radar rule](/radar/rules/reference#post-authorization-attributes). |
| Address checks fail | 4000000000000010 | The address postal code check and address line 1 check both fail.  Radar might block it [depending on your settings.](/radar/rules#traditional-bank-checks) |
| Address unavailable | 4000000000000044 | The address postal code check and address line 1 check are both unavailable.  The payment succeeds unless you [block it with a custom Radar rule](/radar/rules/reference#post-authorization-attributes). |

## Trigger an error with invalid data

To test errors resulting from invalid data, provide invalid details. You don’t need a special test card for this. Any invalid value works. For instance:

* [invalid\_expiry\_month](/declines/codes#invalid_expiry_month): Use an invalid month, such as **13**.
* [invalid\_expiry\_year](/declines/codes#invalid_expiry_year): Use a year up to 50 years in the past, such as **95**.
* [invalid\_cvc](/declines/codes#invalid_cvc): Use a two-digit number, such as **99**.
* [incorrect\_number](/declines/codes#incorrect_number): Use a card number that fails the [Luhn check](https://en.wikipedia.org/wiki/Luhn_algorithm), such as `4242424242424241`.

## Simulate a dispute

To simulate a [disputed transaction](/disputes), use the test cards in this section. Then, to simulate winning or losing the dispute, provide [winning or losing evidence](#evidence).

Card numbers

PaymentMethods

Tokens

| Description | Number | Details |
| --- | --- | --- |
| Fraudulent | 4000000000000259 | With default account settings, charge succeeds, only to be disputed as [fraudulent](/disputes/categories). This type of dispute is [protected](/payments/3d-secure/authentication-flow#disputed-payments) after 3D Secure authentication. |
| Not received | 4000000000002685 | With default account settings, charge succeeds, only to be disputed as [product not received](/disputes/categories). This type of dispute [isn’t protected](/payments/3d-secure/authentication-flow#disputed-payments) after 3D Secure authentication. |
| Inquiry | 4000000000001976 | With default account settings, charge succeeds, only to be disputed as [an inquiry](/disputes/how-disputes-work#inquiries). |
| Warning | 4000000000005423 | With default account settings, charge succeeds, only to receive [an early fraud warning](/disputes/how-disputes-work#early-fraud-warnings). |
| Multiple disputes | 4000000404000079 | With default account settings, charge succeeds, only to be disputed [multiple times](/disputes/how-disputes-work#multiple-disputes). |
| Visa Compelling Evidence 3.0 | 4000000404000038 | With default account settings, charge succeeds, only to be disputed as a [Visa Compelling Evidence 3.0 eligible dispute](/disputes/api/visa-ce3#testing). |
| Visa compliance | 4000008400000779 | With default account settings, charge succeeds, only to be disputed as a [Visa compliance dispute](/disputes/api/visa-compliance#testing). |
| Mastercard compliance | 5105008400000002 | With default account settings, charge succeeds, only to be disputed as a [Mastercard compliance dispute](/disputes/api/mastercard-compliance#testing). |
| Smart disputes | 4000000001000043 | With default account settings, charge succeeds, only to be disputed as a [Smart Disputes](/disputes/smart-disputes) eligible dispute. |

### Evidence

To simulate winning or losing the dispute, respond with one of the evidence values from the table below.

* If you [respond using the API](/disputes/api), pass the value from the table as [uncategorized\_text](/api/disputes/update#update_dispute-evidence-uncategorized_text).
* If you [respond in the Dashboard](/disputes/responding) or in [Connect embedded components](/connect/supported-embedded-components/disputes-list), enter the value from the table in the **Additional information** field. Then, click **Submit evidence**.

| Evidence | Description |
| --- | --- |
| `winning_evidence` | Closes the dispute as won and credits your account for the amount of the charge and related fees. |
| `losing_evidence` | Closes the dispute as lost without crediting your account. For inquiries, this closes the inquiry without escalation. |
| `escalate_inquiry_evidence` | Escalates the inquiry to a chargeback. This transitions the inquiry to a full dispute and debits your account for the amount of the dispute and related fees. |

### Dispute prevention

[Dispute prevention](/disputes/prevention) helps resolve or block disputes before they become chargebacks. To simulate prevented disputes in test mode, use the test cards in this section. If your account has [Dispute Resolution or Dispute Deflection](https://dashboard.stripe.com/settings/disputes) enabled, the dispute on the transaction is either blocked or resolved. Otherwise, the transaction is successfully disputed.

Card numbers

PaymentMethods

Tokens

| Description | Number | Details |
| --- | --- | --- |
| Visa Rapid Dispute Resolution | 4000000404004816 | Charge succeeds, then Visa RDR prevents the dispute if the account is enrolled in Dispute Resolution. Otherwise, creates a dispute. |
| Verifi CE3 block | 4000000404005649 | Charge succeeds, then Compelling Evidence 3.0 blocks the dispute if the account is enrolled in Dispute Deflection. Otherwise, creates a dispute. |
| Ethoca alert | 5105000300000018 | Charge succeeds, then Ethoca Alerts prevents the dispute if the account is enrolled in Dispute Resolution. Otherwise, creates a dispute. |

## Simulate an asynchronous refund

In live mode, refunds are asynchronous: a refund can appear to succeed and later fail, or can appear as `pending` at first and later succeed. To simulate refunds with those behaviors, use the test cards in this section. With all other test cards, refunds succeed immediately and don’t change status after that.

Card numbers

PaymentMethods

Tokens

| Description | Number | Details |
| --- | --- | --- |
| Asynchronous success | 4000000000007726 | The charge succeeds. If you initiate a refund, its status begins as `pending`. Some time later, its status transitions to `succeeded` and sends a `refund.updated` [event](/api/events/types#event_types-refund.updated). |
| Asynchronous failure | 4000000000005126 | The charge succeeds. If you initiate a refund, its status begins as `succeeded`. Some time later, its status transitions to `failed` and sends a `refund.failed` [event](/api/events/types#event_types-refund.failed). |

You can cancel a card refund only by using the Dashboard. In live mode, you can cancel a card refund within a short but nonspecific period of time. Testing environments simulate that period by allowing you to cancel a card refund within 30 minutes.

## Send funds to your available balance

To send the funds from a test transaction directly to your available balance, use the test cards in this section. Other test cards send funds from a successful payment to your pending balance.

Card numbers

PaymentMethods

Tokens

| Description | Number | Details |
| --- | --- | --- |
| Bypass pending balance | 4000000000000077 | The US charge succeeds. Funds are added directly to your available balance, bypassing your pending balance. |
| Bypass pending balance | 4000003720000278 | The international charge succeeds. Funds are added directly to your available balance, bypassing your pending balance. |

## Test 3D Secure authentication

3D Secure requires an additional layer of authentication for credit card transactions. The test cards in this section allow you to simulate triggering authentication in different payment flows.

Only cards in this section effectively test your 3D Secure integration by simulating defined 3DS behavior, such as a challenge flow or an unsupported card. Other Stripe testing cards might still trigger 3DS, but we return `attempt_acknowledged` to bypass the additional steps since 3DS testing isn’t the objective for those cards.

#### Dashboard not supported

3D Secure redirects won’t occur for payments created directly in the Stripe Dashboard. Instead, use your integration’s own frontend or an API call.

### Authentication and setup

To simulate payment flows that include authentication, use the test cards in this section. Some of these cards can also be [set up](/payments/save-and-reuse) for future payments, or have already been.

Card numbers

PaymentMethods

| Description | Number | Details |
| --- | --- | --- |
|  | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| Authenticate unless set up | 4000002500003155 | This card requires authentication for off-session payments unless you [set it up](/payments/save-and-reuse) for future payments. After you set it up, off-session payments no longer require authentication. However, on-session payments with this card always require authentication. |
| Always authenticate | 4000002760003184 | This card requires authentication on all transactions, regardless of how the card is set up. |
| Already set up | 4000003800000446 | This card is already set up for off-session use. It requires authentication for [one-time](/payments/accept-a-payment?platform=web) and other [on-session](/payments/existing-customers?platform=web&ui=elements) payments. However, all off-session payments succeed as if the card has been previously [set up](/payments/save-and-reuse). |
| Insufficient funds | 4000008260003178 | This card requires authentication for [one-time payments](/payments/accept-a-payment?platform=web). All payments are declined with an `insufficient_funds` failure code even after being successfully authenticated or previously [set up](/payments/save-and-reuse). |

### Support and availability

Stripe requests authentication when required by regulation or when triggered by your Radar rules or custom code. Even if authentication is requested, it can’t always be performed—for instance, the customer’s card might not be enrolled, or an error might occur. Use the test cards in this section to simulate various combinations of these factors.

All 3DS references indicate [3D Secure 2](https://stripe.com/guides/3d-secure-2).

Card numbers

PaymentMethods

Tokens

| 3D Secure usage | Outcome | Number | Details |
| --- | --- | --- | --- |
|  | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| 3DS Required | OK | 4000000000003220 | 3D Secure authentication must be completed for the payment to be successful. By default, your Radar rules request 3D Secure authentication for this card. Ireland-issued (`IE`). |
| 3DS Required | OK | 4000008400000027 | 3D Secure authentication must be completed for the payment to be successful. By default, your Radar rules request 3D Secure authentication for this card. US-issued (`US`). |
| 3DS Required | Declined | 4000008400001629 | 3D Secure authentication is required, but payments are declined with a `card_declined` failure code after authentication. By default, your Radar rules request 3D Secure authentication for this card. |
| 3DS Required | Error | 4000008400001280 | 3D Secure authentication is required, but the 3D Secure lookup request fails with a processing error. Payments are declined with a `card_declined` failure code. By default, your Radar rules request 3D Secure authentication for this card. |
| 3DS Supported | OK | 4000000000003055 | 3D Secure authentication might still be performed, but isn’t required. By default, your Radar rules don’t request 3D Secure authentication for this card. |
| 3DS Supported | Error | 4000000000003097 | 3D Secure authentication might still be performed, but isn’t required. However, attempts to perform 3D Secure result in a processing error. By default, your Radar rules don’t request 3D Secure authentication for this card. |
| 3DS Supported | Unenrolled | 4242424242424242 | 3D Secure is supported for this card, but this card isn’t enrolled in 3D Secure. Even if your Radar rules request 3D Secure, the customer won’t be prompted to authenticate. By default, your Radar rules don’t request 3D Secure authentication for this card. |
| 3DS Not supported | | 378282246310005 | 3D Secure isn’t supported on this card and can’t be invoked. The PaymentIntent or SetupIntent proceeds without performing authentication. |
| 3DS Frictionless flow | OK | 4000000032200000 | 3D Secure authentication is required on all transactions, regardless of how the card is set up. The authentication proceeds through a frictionless flow, and succeeds. |

### 3D Secure mobile challenge flows

In a mobile payment, several challenge flows for authentication—where the customer has to interact with prompts in the UI—are available. Use the test cards in this section to trigger a specific challenge flow for test purposes. These cards aren’t useful in browser-based payment forms or in API calls. In those environments, they work but don’t trigger any special behavior. Because they’re not useful in API calls, we don’t provide any `PaymentMethod` or `Token` values to test with.

| Challenge flow | Number | Details |
| --- | --- | --- |
|  | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | | |
| Out of band | 4000582600000094 | 3D Secure 2 authentication must be completed on all transactions. Triggers the challenge flow with Out of Band UI. |
| One time passcode | 4000582600000045 | 3D Secure 2 authentication must be completed on all transactions. Triggers the challenge flow with One Time Passcode UI. |
| Single select | 4000582600000102 | 3D Secure 2 authentication must be completed on all transactions. Triggers the challenge flow with single-select UI. |
| Multi select | 4000582600000110 | 3D Secure 2 authentication must be completed on all transactions. Triggers the challenge flow with multi-select UI. |

## Simulate a captcha challenge

To prevent fraud, Stripe might display a captcha challenge to the user on the payment page. Use the test cards below to simulate this flow.

| Description | Number | Details |
| --- | --- | --- |
| Captcha challenge | 4000000000001208 | The charge succeeds if the user correctly answers the captcha challenge. |
| Captcha challenge | 4000000000003725 | The charge succeeds if the user correctly answers the captcha challenge. |

## Simulate an in-person payment with a PIN

Use the test cards in this section to simulate successful in-person payments where a PIN is involved. There are many other options for testing in-person payments, including a simulated reader and physical test cards. See [Test Stripe Terminal](/terminal/references/testing) for more information.

Card numbers

PaymentMethods

| Description | Number | Details |
| --- | --- | --- |
| Offline PIN | 4001007020000002 | This card simulates a payment where the cardholder is prompted for and enters an offline PIN. The resulting charge has [cardholder\_verification\_method](/api/charges/object#charge_object-payment_method_details-card_present-receipt-cardholder_verification_method) set to `offline_pin`. |
| Offline PIN retry | 4000008260000075 | Simulates an SCA-triggered retry flow where a cardholder’s initial contactless charge fails and the reader then prompts the user to insert their card and enter their offline PIN. The resulting charge has [cardholder\_verification\_method](/api/charges/object#charge_object-payment_method_details-card_present-receipt-cardholder_verification_method) set to `offline_pin`. |
| Online PIN | 4001000360000005 | This card simulates a payment where the cardholder is prompted for and enters an online PIN. The resulting charge has [cardholder\_verification\_method](/api/charges/object#charge_object-payment_method_details-card_present-receipt-cardholder_verification_method) set to `online_pin`. |
| Online PIN retry | 4000002760000008 | Simulates an SCA-triggered retry flow where a cardholder’s initial contactless charge fails and the reader then prompts the user to insert their card and enter their online PIN. The resulting charge has [cardholder\_verification\_method](/api/charges/object#charge_object-payment_method_details-card_present-receipt-cardholder_verification_method) set to `online_pin`. |

## Test a webhook or event destination

To test your webhook endpoint or [event destination](/event-destinations), choose one of these two options:

1. Perform actions in a sandbox that send legitimate events to your event destination. For example, to trigger the [charge.succeeded](/api#event_types-charge.succeeded) event, you can use a [test card that produces a successful charge](#cards).
2. [Trigger events using the Stripe CLI](/webhooks#test-webhook) or [using Stripe for Visual Studio Code](/stripe-vscode#webhooks).

## Rate limits

If your requests in your testing environments begin to receive `429` HTTP errors, make them less frequently. These errors come from our [rate limiter](/rate-limits), which is more strict in testing environments than in live mode.

We don’t recommend load testing your integration using the Stripe API in testing environments. Because the load limiter is stricter in testing environments, you might see errors that you wouldn’t see in production. See [load testing](/rate-limits#load-testing) for an alternative approach.

## Test a non-card payment method

When you use a test non-card payment method, use [test API keys](/keys#obtain-api-keys) in all API calls. This is true whether you’re serving a payment form you can test interactively or writing test code.

Different payment methods have different test procedures:

ACH Direct Debit

SEPA Direct Debit

BACS Direct Debit

AU BECS Direct Debit

Others

Learn how to test scenarios with instant verifications using [Financial Connections](/financial-connections/testing#web-how-to-use-test-accounts).

### Send transaction emails in a sandbox

After you collect the bank account details and accept a mandate, send the mandate confirmation and microdeposit verification emails in a [sandbox](/sandboxes).

If your domain is **{domain}** and your username is **{username}**, use the following email format to send test transaction emails: **{username}+test\_email@{domain}**.

For example, if your domain is **example.com** and your username is **info**, use the format **info+test\_email@example.com** for testing ACH Direct Debit payments. This format ensures that emails route correctly. If you don’t include the **+test\_email** suffix, we won’t send the email.

#### Common mistake

You must [set up your Stripe account](/get-started/account/set-up) before you can trigger these emails while testing.

### Test account numbers

Stripe provides several test account numbers and corresponding tokens you can use to make sure your integration for manually-entered bank accounts is ready for production.

| Account number | Token | Routing number | Behavior |
| --- | --- | --- | --- |
| `000123456789` | `pm_usBankAccount_success` | `110000000` | The payment succeeds. |
| `000111111113` | `pm_usBankAccount_accountClosed` | `110000000` | The payment fails because the account is closed. |
| `000000004954` | `pm_usBankAccount_riskLevelHighest` | `110000000` | The payment is blocked by Radar due to a [high risk of fraud](/radar/risk-evaluation#high-risk). |
| `000111111116` | `pm_usBankAccount_noAccount` | `110000000` | The payment fails because no account is found. |
| `000222222227` | `pm_usBankAccount_insufficientFunds` | `110000000` | The payment fails due to insufficient funds. |
| `000333333335` | `pm_usBankAccount_debitNotAuthorized` | `110000000` | The payment fails because debits aren’t authorized. |
| `000444444440` | `pm_usBankAccount_invalidCurrency` | `110000000` | The payment fails due to invalid currency. |
| `000666666661` | `pm_usBankAccount_failMicrodeposits` | `110000000` | The payment fails to send microdeposits. |
| `000555555559` | `pm_usBankAccount_dispute` | `110000000` | The payment triggers a dispute. |
| `000000000009` | `pm_usBankAccount_processing` | `110000000` | The payment stays in processing indefinitely. Useful for testing [PaymentIntent cancellation](/api/payment_intents/cancel). |
| `000777777771` | `pm_usBankAccount_weeklyLimitExceeded` | `110000000` | The payment fails due to payment amount causing the account to exceed its weekly payment volume limit. |
| `000888888885` |  | `110000000` | The payment fails because of a deactivated [tokenized account number](/financial-connections/tokenized-account-numbers). |

Before test transactions can complete, you need to verify all test accounts that automatically succeed or fail the payment. To do so, use the test microdeposit amounts or descriptor codes below.

### Test microdeposit amounts and descriptor codes

To mimic different scenarios, use these microdeposit amounts *or* 0.01 descriptor code values.

| Microdeposit values | 0.01 descriptor code values | Scenario |
| --- | --- | --- |
| `32` and `45` | SM11AA | Simulates verifying the account. |
| `10` and `11` | SM33CC | Simulates exceeding the number of allowed verification attempts. |
| `40` and `41` | SM44DD | Simulates a microdeposit timeout. |

### Test settlement behavior

Test transactions settle instantly and are added to your available test balance. This behavior differs from livemode, where transactions can take [multiple days](#timing) to settle in your available balance.

## Test Link

#### Caution

Don’t store real user data in [sandbox](/sandboxes) Link accounts. Treat them as if they’re publicly available, because these test accounts are associated with your publishable key.

Currently, Link only works with credit cards, debit cards, and qualified US bank account purchases. Link requires [domain registration](/payments/payment-methods/pmd-registration).

You can create sandbox accounts for Link using any valid email address. The following table shows the fixed one-time passcode values that Stripe accepts for authenticating sandbox accounts:

| Value | Outcome |
| --- | --- |
| Any other 6 digits not listed below | Success |
| 000001 | Error, code invalid |
| 000002 | Error, code expired |
| 000003 | Error, max attempts exceeded |

### Multiple funding sources

As Stripe adds additional funding source support, you don’t need to update your integration. Stripe automatically supports them with the same transaction settlement time and guarantees as card and bank account payments.

## Test a redirect-based flow

To test your integration’s redirect-handling logic by simulating a payment that uses a redirect flow (for example, iDEAL), use a supported payment method that [requires redirects](/payments/payment-methods/payment-method-support#additional-api-supportability).

To create a test `PaymentIntent` that either succeeds or fails:

1. Go to the [payment methods settings in the Dashboard](https://dashboard.stripe.com/settings/payment_methods) and enable a supported payment method by clicking **Turn on** in your testing environment.
2. Collect payment details.
3. Submit the payment to Stripe.
4. Authorize or fail the test payment.

Make sure that the page (corresponding to `return_url`) on your website provides the status of the payment.

## See also

* [Testing your Connect integration](/connect/testing)
* [Testing your Billing integration](/billing/testing)
* [Testing your Terminal integration](/terminal/references/testing)
* [Load testing](/rate-limits#load-testing)
