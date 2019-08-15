# coding=utf-8
from __future__ import absolute_import


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
    def endpoint_lamp(self):
        r = int(flask.request.values['red'])
        g = int(flask.request.values['green'])
        b = int(flask.request.values['blue'])
        if self.quadfrost is not None:
            self._logger.info("Setting lamp to %s %s %s", r, g, b)
            self.quadfrost.set_mode(quadfrost.MODE_LAMP).set_color(r, g, b)
            return "", 204
        else:
            self._logger.warn("Failed to set Arduino: not connected")
            return "", 503

    @octoprint.plugin.BlueprintPlugin.route("/filter", methods=["POST"])
    def endpoint_filter(self):
        power = int(flask.request.values['power'])
        if self.quadfrost is not None:
            self._logger.info("Setting filter to %s", power)
            self.quadfrost.set_filter(power)
        else:
            self._logger.warn("Failed to set Arduino: not connected")
        return ""

    def on_shutdown(self):
        if self.quadfrost is not None:
            self._logger.info("Closing serial")
            self.quadfrost.close()


__plugin_name__ = "Quadfrost"
__plugin_implementation__ = QuadfrostPlugin()

