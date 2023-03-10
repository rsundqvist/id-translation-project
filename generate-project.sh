set -e

REPLAY_FILE=tests/replay/default.json

rm -rf ute-id-translation/*.*  ute-id-translation/src ute-id-translation/tests
cookiecutter . --replay-file $REPLAY_FILE -f --output-dir demo
cp $REPLAY_FILE demo/replay.json
tree demo/ute-id-translation/
