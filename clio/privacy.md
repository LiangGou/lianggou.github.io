---
layout: single
title: Clio — Privacy Policy
permalink: /clio/privacy/
author_profile: false
sitemap: false
---

Clio is a personal AI assistant operated by its owner for his own use. This policy describes how Clio handles information obtained from Google APIs, in particular the Gmail API, when the owner connects his Google account.

## Information Clio accesses

When the owner connects a Google account, Clio receives OAuth authorization to use the Gmail API scopes listed on the consent screen. Using that access, and only in response to the owner's own requests in the assistant interface, Clio may read email messages and their metadata (sender, recipients, subject, date, labels, snippets and body text), read message threads, count messages matching a query, download attachments the owner asks for, and — where the owner has granted the corresponding scopes and confirms the action — create drafts, send mail, and modify labels or message state.

## How the information is used

Gmail data is used solely to carry out the owner's requests in the assistant (for example: summarizing unread mail, searching the mailbox, reading a thread, drafting a reply). Clio does not use Gmail data for advertising, does not build advertising or credit profiles, does not sell or transfer Gmail data to third parties, and does not use Gmail data to train artificial-intelligence or machine-learning models. No human other than the owner reads the data; the service is operated for a single user, the owner himself.

## Storage and protection

OAuth credentials (access and refresh tokens) are stored encrypted at rest (Fernet/AES encryption with a key held only in the server's environment configuration) in a dedicated directory on the service's private persistent storage, with restrictive file permissions, and are never written to logs or exposed through the assistant's file tools. Email content is fetched on demand and processed in memory to answer the owner's current request; it is not indexed, cached in a database, or retained beyond the conversation records the owner himself keeps in the app. When the owner asks for an attachment, the file is saved into the owner's own workspace at his direction. Traffic between Clio and Google APIs uses HTTPS.

## Sharing

Clio does not share Google user data with any third party, except the model provider that powers the assistant's replies, which receives the message content the owner asked the assistant to work on, solely to generate that reply, under that provider's API terms; and except as required by law.

## Retention and deletion

The owner may disconnect Gmail at any time from inside Clio (Settings > Connectors > Gmail > Disconnect), which deletes the stored OAuth credentials from the service. The owner may also revoke Clio's access at any time from his Google Account's third-party access page, which immediately invalidates the stored credentials. To request deletion of any remaining data associated with the connection, contact the address below.

## Limited Use disclosure

Clio's use and transfer of information received from Google APIs adheres to the Google API Services User Data Policy, including the Limited Use requirements.

## Contact

Questions about this policy or the app's handling of Google user data: gogo430@gmail.com

Last updated: October 17, 2026
