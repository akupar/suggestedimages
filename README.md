# Suggested Images

Image suggestion utility for wiktionaries.

## Setup

    . venv/bin/activate
    pip install -r requirements.txt

## Run in development mode

    flask --app suggestedimages run

## Bookmarklet
Add this bookmarklet to your browsers bookmark bar, and click it on a wiktionary page to see suggestios.

```javascript
javascript:(function () {
      if ( !window.location.hostname.endsWith(".wiktionary.org") ) {
          alert("This bookmarklet only works on a wiktionary page.");
          return;
      }
       window.open("https://imgs-for-wikt.toolforge.org/?" + $.param({
          "wikt": window.location.hostname.split('.')[0],
          "title": mw.config.get("wgTitle")
      }));
}());
```
