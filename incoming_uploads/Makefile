.PHONY: doctor context next test verify firewall manifest package

doctor:
	python tools/rfc.py doctor

context:
	python tools/rfc.py context

next:
	python tools/rfc.py next

test:
	python -m unittest discover -s tests -v

firewall:
	python tools/rfc.py firewall-scan

manifest:
	python tools/build_bundle.py

package:
	python tools/build_bundle.py --output ../3RFC_Execution_Ready_Universe_Builder_20260805.zip

verify: doctor test firewall
