(function () {
  var input = document.getElementById('search');
  if (!input) return;

  var browse = document.getElementById('browse');
  var output = document.getElementById('search-output');
  var countEl = document.getElementById('search-count');
  var resultsEl = document.getElementById('search-results');

  var indexPromise = null;
  var prepared = null;
  var debounceTimer = null;

  function norm(s) {
    return (s || '').toLowerCase().replace(/ё/g, 'е');
  }

  function loadIndex() {
    if (!indexPromise) {
      indexPromise = fetch('/searchindex.json')
        .then(function (r) {
          if (!r.ok) throw new Error('HTTP ' + r.status);
          return r.json();
        })
        .then(function (docs) {
          prepared = docs.map(function (doc, i) {
            return {
              doc: doc,
              i: i,
              title: norm(doc.title),
              tags: norm((doc.tags || []).join(' ')),
              description: norm(doc.description),
              content: norm(doc.content)
            };
          });
          return prepared;
        });
    }
    return indexPromise;
  }

  function tokenize(q) {
    return norm(q).split(/\s+/).filter(Boolean);
  }

  function scoreDoc(p, tokens) {
    var score = 0;
    for (var t = 0; t < tokens.length; t++) {
      var tok = tokens[t];
      var matched = false;
      if (p.title.indexOf(tok) !== -1) {
        score += 8;
        matched = true;
      }
      if (p.tags.indexOf(tok) !== -1) {
        score += 5;
        matched = true;
      }
      if (p.description.indexOf(tok) !== -1) {
        score += 3;
        matched = true;
      }
      if (p.content.indexOf(tok) !== -1) {
        score += 1;
        matched = true;
      }
      if (!matched) return -1;
    }
    return score;
  }

  function snippetAround(contentNorm, contentRaw, token) {
    var idx = contentNorm.indexOf(token);
    if (idx === -1) return null;
    var start = Math.max(0, idx - 50);
    var end = Math.min(contentRaw.length, idx + token.length + 50);
    return {
      before: contentRaw.slice(start, idx),
      match: contentRaw.slice(idx, idx + token.length),
      after: contentRaw.slice(idx + token.length, end)
    };
  }

  function renderResults(matches, tokens) {
    resultsEl.textContent = '';
    var limit = Math.min(50, matches.length);
    for (var m = 0; m < limit; m++) {
      var doc = matches[m].doc;
      var li = document.createElement('li');

      var dateSpan = document.createElement('span');
      dateSpan.className = 'date';
      dateSpan.textContent = doc.date;
      li.appendChild(dateSpan);

      var link = document.createElement('a');
      link.href = doc.url;
      link.textContent = doc.title;
      li.appendChild(link);

      if (tokens.length && doc.content) {
        var snip = snippetAround(matches[m].contentNorm, doc.content, tokens[0]);
        if (snip) {
          var snipEl = document.createElement('span');
          snipEl.className = 'search-snippet';
          snipEl.appendChild(document.createTextNode(snip.before));
          var mark = document.createElement('mark');
          mark.textContent = snip.match;
          snipEl.appendChild(mark);
          snipEl.appendChild(document.createTextNode(snip.after));
          li.appendChild(snipEl);
        }
      }

      resultsEl.appendChild(li);
    }
  }

  function showBrowse() {
    browse.hidden = false;
    output.hidden = true;
    resultsEl.textContent = '';
    countEl.textContent = '';
    var url = new URL(window.location.href);
    url.searchParams.delete('q');
    history.replaceState(null, '', url.pathname + url.search + url.hash);
  }

  function showSearchUI() {
    browse.hidden = true;
    output.hidden = false;
  }

  function runSearch(query) {
    var tokens = tokenize(query);
    if (!tokens.length) {
      showBrowse();
      return;
    }

    var url = new URL(window.location.href);
    url.searchParams.set('q', query);
    history.replaceState(null, '', url.pathname + '?' + url.searchParams.toString() + url.hash);

    loadIndex()
      .then(function () {
        var matches = [];
        for (var i = 0; i < prepared.length; i++) {
          var p = prepared[i];
          var sc = scoreDoc(p, tokens);
          if (sc >= 0) {
            matches.push({
              doc: p.doc,
              score: sc,
              i: p.i,
              contentNorm: p.content
            });
          }
        }
        matches.sort(function (a, b) {
          if (b.score !== a.score) return b.score - a.score;
          return a.i - b.i;
        });

        showSearchUI();
        if (!matches.length) {
          countEl.textContent = 'Ничего не найдено';
          resultsEl.textContent = '';
          return;
        }
        countEl.textContent = 'Найдено: ' + matches.length;
        renderResults(matches, tokens);
      })
      .catch(function (err) {
        console.error(err);
        countEl.textContent = 'Поиск недоступен';
        resultsEl.textContent = '';
        browse.hidden = false;
        output.hidden = false;
      });
  }

  function onInput() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(function () {
      runSearch(input.value);
    }, 120);
  }

  function ensureIndex() {
    loadIndex().catch(function (err) {
      console.error(err);
    });
  }

  input.addEventListener('focus', ensureIndex);
  input.addEventListener('input', function () {
    ensureIndex();
    onInput();
  });
  input.addEventListener('search', onInput);

  var initialQ = new URL(window.location.href).searchParams.get('q');
  if (initialQ) {
    input.value = initialQ;
    runSearch(initialQ);
  }
})();