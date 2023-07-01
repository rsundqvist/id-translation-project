set -e

REPLAY_FILE="${REPLAY_FILE:-tests/replay/default.json}"
OUTPUT_DIR=demo

rm -rf $OUTPUT_DIR/bci-id-translation
cookiecutter . --replay-file $REPLAY_FILE -f --output-dir $OUTPUT_DIR
cp $REPLAY_FILE $OUTPUT_DIR/replay.json
tree $OUTPUT_DIR/bci-id-translation/
