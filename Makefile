clean:
	rm -r wampproto

gen-py:
	flatc --python flatbuffers/*.fbs
