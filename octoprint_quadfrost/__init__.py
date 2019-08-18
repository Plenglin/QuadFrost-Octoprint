# coding=utf-8
from __future__ import absolute_import


import octoprint.plugin as opl
import flask

from . import quadfrost

EVENT_STATUS_MAP = {
    'Connected': 1,
    'Disconnected': 7,
    'PrintDone': 5,
    'PrintResumed': 2,
    'PrintStarted': 2,
    'PrintPaused': 6
}

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
            self.quadfrost.set_status(2)
            self.quadfrost.set_progress(progress)
    
    def on_event(self, event, payload):
        if self.quadfrost is not None:
            if event in EVENT_STATUS_MAP:
                code = EVENT_STATUS_MAP[event]
                self._logger.info("Received %s event. Setting status to %s.", event, code)
                self.quadfrost.set_status(code)
            elif event == 'PrintFailed':
                reason = payload['reason']
                code = {'cancelled': 3, 'error': 4}[reason]
                self._logger.info("Received %s event with reason %s. Setting status to %s.", event, reason, code)

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

