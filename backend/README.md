# fwordle-backend

fwordle: Wordle, but with friends!

Python backend server component. Essentially a simple websockets server with a Wordle game interface.

## Installation

```
$ git clone https://github.com/aspin/fwordle.git
$ pip install -r requirements.txt
```

## Usage

**Run**

```
$ PYTHONPATH=./ python fwordle/main.py --dictionary-path data_files/words_alpha.txt
```

- App served @ `http://localhost:9000` / `ws://localhost:9000`

**Test**

```
$ pytest
```

**Lint**

```
$ flake8 . --count
```

**Format**

```
$ black .
```

## Protocol

Documentation may or may not be written in the future.
