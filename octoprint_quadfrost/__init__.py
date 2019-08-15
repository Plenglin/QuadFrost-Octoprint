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
import flask

from . import quadfrost

class QuadfrostPlugin(
    octoprint.plugin.BlueprintPlugin,
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.ShutdownPlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin):

    def on_after_startup(self):
        port = self._settings.get(['port'])
        self._logger.info('Connecting to Arduino at %s', port)
        self.quadfrost = None
        try:
            self.quadfrost = quadfrost.QuadFrost(port)
            self._logger.info("Successfully connected to Arduino at %s", port)
        except Exception as e:
            self._logger.error("Error while initializing Arduino", exc_info=True)
    
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

    @octoprint.plugin.BlueprintPlugin.route("/lamp", methods=["POST"])
    def lamp(self):
        r = int(flask.request.values['red'])
        g = int(flask.request.values['green'])
        b = int(flask.request.values['blue'])
        self._logger.info("Setting lamp to %s %s %s", r, g, b)
        if self.quadfrost is not None:
            self.quadfrost.set_mode(quadfrost.MODE_LAMP).set_color(r, g, b)
        else:
            self._logger.warn("Failed to set Arduino: not connected")
        return ""

    def on_shutdown(self):
        if self.quadfrost is not None:
            self.quadfrost.close()


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Quadfrost Plugin"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = QuadfrostPlugin()

