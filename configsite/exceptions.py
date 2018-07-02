class ConfigError(Exception):
	"""Basic exception for errors raised by configmaker"""
	def __init__(self, msg=None):
		if msg is None:
			# Set some default useful error message
			msg = "An error occured with the configuring the json"
		super(ConfigError, self).__init__(msg)


class InvalidConfigError(ConfigError):
	"""When you drive too fast"""
	def __init__(self, msg=None):
		message = "Could not set configuration. Seek help from an administrator.\n" + (msg or "")
		super(InvalidConfigError, self).__init__(msg=message)
