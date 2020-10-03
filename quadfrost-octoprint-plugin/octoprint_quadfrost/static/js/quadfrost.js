/*
 * View model for OctoPrint-Quadfrost
 *
 * Author: Plenglin
 * License: AGPLv3
 */
$(function() {
    function QuadfrostViewModel(parameters) {
        console.log("binding quadfrost")
        var self = this;
        self.loginState = parameters[0];
        self.settings = parameters[1];

        self.newSerialPort = ko.observable();
        self.lampState = ko.observable();
        self.filterState = ko.observable();

        self.lampState.subscribe(function(state) {
            console.log("Changing lamp state to", state)
            if (state) {
                $.post('/plugin/quadfrost/lamp', {
                    red: 255,
                    green: 255,
                    blue: 255,
                });
            } else {
                $.post('/plugin/quadfrost/lamp', {
                    red: 0,
                    green: 0,
                    blue: 0,
                });
            }
        });

        self.filterState.subscribe(function(state) {
            console.log("Changing filter state to", state)
            if (state) {
                $.post('/plugin/quadfrost/filter', {
                    power: 255
                });
            } else {
                $.post('/plugin/quadfrost/filter', {
                    power: 0
                });
            }
        });

        self.connectToSerial = function() {
            var port = self.newSerialPort();
            console.info("Attempting to connect to serial port", port);
            $.post('/plugin/quadfrost/serialport', {
                serialport: port
            });
        };

        self.onBeforeBinding = function() {
            console.log(self.settings);
            self.newSerialPort(self.settings.settings.plugins.quadfrost.port());
        };
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: QuadfrostViewModel,
        dependencies: ["loginStateViewModel", "settingsViewModel"],
        elements: ["#tab_quadfrost"]
    });
});
