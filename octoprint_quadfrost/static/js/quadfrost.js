/*
 * View model for OctoPrint-Quadfrost
 *
 * Author: You
 * License: AGPLv3
 */
$(function() {
    function QuadfrostViewModel(parameters) {
        console.log("binding quadfrost")
        var self = this;
        self.settings = parameters[0];
        self.serialPort = ko.observable();
        self.lampState = ko.observable();

        self.connectToSerial = function() {
            self.currentSerialPort(self.newSerialPort);
        };

        self.setLampState = function() {
            var state = self.lampState();
            console.log("Setting lamp state", state)
            if (state) {
                $.post('/plugin/quadfrostplugin/lamp', {
                    red: 255,
                    green: 255,
                    blue: 255,
                });
            } else {
                $.post('/plugin/quadfrostplugin/lamp', {
                    red: 0,
                    green: 0,
                    blue: 0,
                });
            }
        }

        self.onBeforeBinding = function() {
            self.serialPort(self.settings.settings.plugins.quadfrost.port());
        };
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: QuadfrostViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: ["settingsViewModel"],
        // Elements to bind to, e.g. #settings_plugin_quadfrost, #tab_plugin_quadfrost, ...
        elements: [ "#tab-quadfrost" ]
    });
});
