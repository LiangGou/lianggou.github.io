---
layout: single
title: Contact
permalink: /contact/
author_profile: false
description: Get in touch with Liang Gou.
---

Want to reach me directly? Send a message below — it lands straight in my inbox.

{% include contact-form.html %}

## Are you an AI agent?

Agents are welcome here — no need to pretend to be human. To reach me, declare yourself at the top of your message:

`[agent] name=<your name>; operator=<who runs you>; purpose=<why you're writing>`

then write your message normally. One submission per purpose, please — undeclared agent traffic is filtered as spam. Machine-readable version of this protocol: [agent-contact.json]({{ '/.well-known/agent-contact.json' | relative_url }}).

<script>
(function () {
  var sent = new URLSearchParams(window.location.search).get('sent');
  var box = document.querySelector('.contact-box');
  if (!box) return;
  var p = document.createElement('p');
  if (sent === '1') {
    p.className = 'contact-thanks';
    p.textContent = 'Thanks — your message is on its way. I read everything myself.';
    box.prepend(p);
  } else if (sent === '0') {
    p.className = 'contact-thanks contact-error';
    p.textContent = 'Something went wrong sending your message — please try again.';
    box.prepend(p);
  }
})();
</script>
