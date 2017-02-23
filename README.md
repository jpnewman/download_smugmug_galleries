# Download SmugMug galleries

This script downloads pictures from SmugMug galleries and demonstrates handling web pages that are rendered with Javascripts. By using Selenium

> BeautifulSoup can't wait for javascript to finish loading the page so using Selenium Webdriver instead.

# Requirements

- Firefox

# Install geckodriver for Selenium (Firefox)

~~~bash
brew install geckodriver
~~~

# Install Python requirements

~~~bash
pip install -r requirements.txt
~~~

# Run

~~~bash
python download_pics.py https://fotoeffects.smugmug.com/My-Personal-Favorites/i-wLjbH7r
~~~

> Starting URL should be in the gallery view, without the size suffix. e.g. ```/A```
