clean:
	rm -rf go python dart kotlin

gen: clean gen-py gen-go gen-dart gen-kotlin

gen-py:
	flatc -o python --python flatbuffers/message.fbs --gen-all

gen-go:
	flatc -o go --go flatbuffers/message.fbs --gen-all

gen-dart:
	flatc -o dart --dart flatbuffers/message.fbs --gen-all

gen-kotlin:
	flatc -o kotlin --kotlin flatbuffers/message.fbs --gen-all

verify:
	./.venv/bin/python create.py
