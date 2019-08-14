# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin

class QuadfrostPlugin(
	octoprint.plugin.StartupPlugin,
	octoprint.plugin.ShutdownPlugin,
	octoprint.plugin.SettingsPlugin,
	octoprint.plugin.AssetPlugin,
	octoprint.plugin.TemplatePlugin):

	def on_startup(self, host, port):
		pass
	
	def get_template_configs(self):
		return [
			dict(type="tab", custom_bindings=False)
		]

	def get_settings_defaults(self):
		return dict(
			port='/dev/ttyACM0'
		)

	def get_assets(self):
		return dict(
			js=["js/quadfrost.js"],
			css=["css/quadfrost.css"],
			less=["less/quadfrost.less"]
		)
	
	def on_shutdown(self):
		pass


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Quadfrost Plugin"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = QuadfrostPlugin()

