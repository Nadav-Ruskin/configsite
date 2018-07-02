from werkzeug import datastructures
import os
import json
import shutil
import jsonschema
import exceptions


SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIRECTORY, "jsons", "config.json")
SCHEMA_PATH = os.path.join(SCRIPT_DIRECTORY, "jsons", "schema.json")
DEFAULT_CONFIG_PATH = os.path.join(SCRIPT_DIRECTORY, "jsons", "default_config.json")


class ConfigMaker():
	def __init__(self):
		self.existing_config = self._AcquireConfig()

	def _Validate_Config(self, config):
		with open(SCHEMA_PATH, 'r') as f:
			schema = json.load(f)
		try:
			jsonschema.validate(config, schema)
		except Exception as e:
			raise exceptions.InvalidConfigError("Json invalidates schema. json:\n" + str(config) + "\nError message: " + str(e))
		pass

	def _AcquireDefaultConfig(self):
		with open(DEFAULT_CONFIG_PATH, 'r') as f:
			config = json.load(f)
		with open(CONFIG_PATH, 'w') as f:
			json.dump(config, f, sort_keys=True, indent=4)
		return config

	def _AcquireConfig(self):
		try:
			with open(CONFIG_PATH, 'r') as f:
					config = json.load(f)
					self._Validate_Config(config)
		except Exception as e:
			if os.path.isdir(CONFIG_PATH):
				shutil.rmtree(CONFIG_PATH)
			elif os.path.isfile(CONFIG_PATH):
				os.remove(CONFIG_PATH)
			try:
				config = self._AcquireDefaultConfig()
			except Exception as e:
				raise exceptions.InvalidConfigError("Neither active not default configurations could be loaded.\nError message: " + str(e))
			try:
				self._Validate_Config(config)
			except Exception as e:
				raise exceptions.InvalidConfigError("Tried reverting to default json, but somehow it does not pass schema. json:\n" + str(config) + "\nError message: " + str(e))
			with open(CONFIG_PATH, 'w') as f:
				json.dump(config, f, sort_keys=True, indent=4)
		return config

	def _Config_From_Form(self, form: datastructures.ImmutableMultiDict):
		new_config = dict(self.existing_config)
		new_config["name"] = form["name"]
		new_config["contact"] = form["contact"]
		new_config["car"] = form["car"]
		new_config["fast_results"] = form.get("fast_results") is not None
		new_config["accurate_results"] = form.get("accurate_results") is not None
		new_config["exposure"] = int(form["exposure"])
		return new_config

	def Update_Json(self, form: datastructures.ImmutableMultiDict):
		new_config = self._Config_From_Form(form)
		self._Validate_Config(new_config)
		with open(CONFIG_PATH, 'w') as f:
			json.dump(new_config, f, sort_keys=True, indent=4)
		self.existing_config = new_config
