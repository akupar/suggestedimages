# Suggested Images

Image suggestion utility for wiktionaries.

## Setup
Create an environment for the requirements.

    python3 -m venv venv

Activate it.

    source venv/bin/activate

Install requirements.

    pip install -r requirements.txt


## Run in development mode
In the environment.

    flask run

or

    flask run --debug

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
