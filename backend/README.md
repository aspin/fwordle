# fwordle-backend

fwordle: Wordle, but with friends!

Python backend server component. Essentially a simple websockets server with a
Wordle game interface.

## Get Started

Start:

```
$ pip install -r requirements.txt
$ PYTHONPATH=./ python fwordle/main.py --dictionary-path data_files/words_alpha.txt
```

Test:

```
$ pytest
```

Lint:

```
$ flake8 . --count
```

Format:

```
$ black .
```

## Protocol

Documentation needs to be written!