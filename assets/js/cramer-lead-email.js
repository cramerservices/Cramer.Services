(function () {
  'use strict';

  const endpoint = 'https://qsiimareoiyrkompuobi.supabase.co/functions/v1/website-lead';
  const anonKey = 'sb_publishable_msZgwZ5Sascz_SYnTXQuQw_Km1k62pX';

  async function send(payload) {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        apikey: anonKey,
        Authorization: `Bearer ${anonKey}`,
      },
      body: JSON.stringify({
        ...payload,
        source: payload.source || document.body?.dataset?.leadSource || 'website_form',
        pageUrl: window.location.href,
      }),
    });

    const result = await response.json().catch(() => ({}));
    if (!response.ok || !result.success) {
      throw new Error(result.error || 'Your request could not be sent.');
    }
    return result;
  }

  window.CramerEmail = { send };
})();
