# coding=utf-8
from __future__ import absolute_import


import octoprint.plugin as opl
import flask

from . import quadfrost

class QuadfrostPlugin(
    opl.BlueprintPlugin,
    opl.StartupPlugin,
    opl.ShutdownPlugin,
    opl.ProgressPlugin,
    opl.SettingsPlugin,
    opl.AssetPlugin,
    opl.EventHandlerPlugin,
    opl.TemplatePlugin):
    
    quadfrost = None

    def on_after_startup(self):
        port = self._settings.get(['port'])
        self._logger.info('Connecting to Arduino at %s', port)
        try:
            self.quadfrost = quadfrost.QuadFrost(port)
            self._logger.info("Successfully connected to Arduino at %s", port)
        except Exception as e:
            self._logger.error("Error while initializing Arduino", exc_info=True)
    
    def on_print_progress(self, storage, path, progress):
        if self.quadfrost is not None:
            self.quadfrost.set_progress(progress)
    
    def on_event(self, event, payload):
        if self.quadfrost is not None:
            if event == 'Connected':
                self.quadfrost.set_status(1).set_lamp_mode().set_color(255, 255, 255)
            elif event == 'PrintDone':
                self.quadfrost.set_status(5).set_progress(100).set_lamp_mode().set_color(0, 255, 0)
            elif event == 'PrintStarted':
                self.quadfrost.set_status(2).set_progress(0).set_hue_mode().set_hue_range(0, 64).set_rate(1, 50).set_sat_val(128, 255)
            elif event == 'PrintPaused':
                self.quadfrost.set_status(6).set_empty_mode()
            elif event == 'PrintResumed':
                self.quadfrost.set_status(2).set_hue_mode()
            elif event == 'Disconnected':
                self.quadfrost.set_status(7).set_lamp_mode().set_color(128, 192, 0)
            elif event == 'PrintFailed':
                code = {'cancelled': 3, 'error': 4}[payload['reason']]
                self.quadfrost.set_status(code).set_lamp_mode().set_color(255, 0, 0)

    def get_template_configs(self):
        return [
            dict(type="tab", custom_bindings=False)
        ]

    def get_settings_defaults(self):
        return dict(
            port='/dev/ttyUSB0'
        )

    def get_assets(self):
        return dict(
            js=["js/quadfrost.js"],
            css=["css/quadfrost.css"],
            less=["less/quadfrost.less"]
        )

    @opl.BlueprintPlugin.route("/lamp", methods=["POST"])
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

    @opl.BlueprintPlugin.route("/filter", methods=["POST"])
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

