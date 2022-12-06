import os
import flask
# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)  # pylint: disable=invalid-name
# Read settings from config module (insta485/config.py)
# Overlay settings read from a Python file whose path is set in the environment
# variable INSTA485_SETTINGS. Setting this environment variable is optional.
# Docs: http://flask.pocoo.org/docs/latest/config/
#
# EXAMPLE:
# $ export INSTA485_SETTINGS=secret_key_config.py
import index.api  # noqa: E402  pylint: disable=wrong-import-position
# Load inverted index, stopwords, and pagerank into memory
app.config["INDEX_PATH"] = os.getenv("INDEX_PATH", "inverted_index_1.txt")
index.api.load_index()


print(app.config["INDEX_PATH"])
