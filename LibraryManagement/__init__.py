import sys


def _configure_utf8_stdout():
	try:
		if hasattr(sys.stdout, "reconfigure"):
			sys.stdout.reconfigure(encoding="utf-8")
	except (AttributeError, ValueError, OSError):
		pass

	try:
		if hasattr(sys.stderr, "reconfigure"):
			sys.stderr.reconfigure(encoding="utf-8")
	except (AttributeError, ValueError, OSError):
		pass


_configure_utf8_stdout()
