clean:
	rm -r wampproto

gen-py:
	flatc -p flatbuffers/message.fbs --gen-all
