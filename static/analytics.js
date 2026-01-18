/**
 * Read-through tracking for PostHog
 * Tracks: scroll depth, active reading time, completion
 */
(function() {
  // Config
  const POSTHOG_KEY = 'phc_cnUad9BXndQu5MKPPsBpkVPuNb82WniZMeTZl7xKacN';
  const POSTHOG_HOST = 'https://us.i.posthog.com';

  // State
  let maxScroll = 0;
  let activeTime = 0;
  let lastActivity = Date.now();
  let startTime = Date.now();
  let timerInterval = null;

  // Calculate expected reading time from word count
  const article = document.querySelector('article');
  const wordCount = article ? article.textContent.split(/\s+/).length : 0;
  const expectedTime = Math.round((wordCount / 250) * 1000); // 250 wpm, in ms

  // Init PostHog
  !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.async=!0,p.src=s.api_host+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys onSessionId".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);

  posthog.init(POSTHOG_KEY, {
    api_host: POSTHOG_HOST,
    capture_pageview: true,
    capture_pageleave: false, // We'll do custom
    autocapture: false,
    disable_session_recording: true
  });

  // Track scroll depth
  function updateScroll() {
    const scrolled = (window.scrollY + window.innerHeight) / document.documentElement.scrollHeight;
    maxScroll = Math.max(maxScroll, Math.round(scrolled * 100));
  }

  // Track activity
  function onActivity() {
    lastActivity = Date.now();
  }

  // Active time counter (only counts when tab visible + recent activity)
  function startTimer() {
    timerInterval = setInterval(() => {
      if (!document.hidden && Date.now() - lastActivity < 5000) {
        activeTime += 1000;
      }
    }, 1000);
  }

  // Calculate read-through score
  function getReadScore() {
    const timeScore = Math.min(1, activeTime / expectedTime);
    const scrollScore = maxScroll / 100;

    // Fast scroll without reading time = skimming
    if (scrollScore > 0.9 && timeScore < 0.3) {
      return Math.round(timeScore * 50);
    }

    return Math.round((timeScore * 0.6 + scrollScore * 0.4) * 100);
  }

  // Send final event
  function trackLeave() {
    const readScore = getReadScore();
    const totalTime = Math.round((Date.now() - startTime) / 1000);
    const activeTimeSec = Math.round(activeTime / 1000);

    posthog.capture('article_read', {
      read_score: readScore,
      max_scroll_depth: maxScroll,
      active_time_sec: activeTimeSec,
      total_time_sec: totalTime,
      expected_time_sec: Math.round(expectedTime / 1000),
      word_count: wordCount,
      completed: maxScroll >= 90 && readScore >= 70,
      path: location.pathname
    });
  }

  // Bind events
  window.addEventListener('scroll', updateScroll, { passive: true });
  window.addEventListener('scroll', onActivity, { passive: true });
  window.addEventListener('mousemove', onActivity, { passive: true });
  window.addEventListener('touchmove', onActivity, { passive: true });
  window.addEventListener('click', onActivity, { passive: true });

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      trackLeave();
    }
  });

  window.addEventListener('beforeunload', trackLeave);

  // Start
  updateScroll();
  startTimer();
})();
