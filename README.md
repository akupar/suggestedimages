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
You can use this bookmarklet to open search results for a Wiktionary page you are currently on.

Add it in your bookmark bar and click it while on any wiktionary page (in any language) to open search results in a new tab.

The bookmarklet extracts the wiktionary code and the article name from the page and sends them to the app in a new tab.

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
