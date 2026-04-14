pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects

import Theme
import ThreatPing
import "components"

ApplicationWindow {
    id: root

    visible: true
    width: 540
    height: 490
    title: "Threat Ping"
    color: "transparent"

    // Block resize
    minimumWidth: width
    minimumHeight: height
    maximumWidth: width
    maximumHeight: height

    // Disable window decoration
    flags: Qt.FramelessWindowHint | Qt.Window

    property var onboarding: ({
        location: null,
        notificationsEnabled: false,
        startupEnabled: false
    })

    Component {
        id: locationSelect

        ColumnLayout {
            spacing: Sizes.s3
            anchors.fill: parent

            Item { Layout.fillHeight: true }

            Rectangle {
                Layout.alignment: Qt.AlignCenter
                implicitWidth: 120
                implicitHeight: 120
                color: Colors.surface_elevated
                radius: Sizes.radius_md
                border.color: Colors.border_strong

                Image {
                    id: mapIcon
                    anchors.centerIn: parent
                    width: 52
                    height: 52

                    source: "assets/icons/lucide--map-pin.svg"
                    sourceSize.width: width // SVG render size
                    sourceSize.height: height

                    visible: false
                }
                MultiEffect {
                    source: mapIcon
                    anchors.fill: mapIcon
                    colorization: 1.0
                    colorizationColor: Colors.accent_primary
                }
            }

            Label {
                Layout.alignment: Qt.AlignCenter
                Layout.topMargin: 12
                text: "Where are you?"

                color: Colors.text_primary
                font.pixelSize: Typography.hero_size
                font.weight: Typography.hero_weight
                font.letterSpacing: Typography.hero_spacing
            }

            Label {
                Layout.alignment: Qt.AlignCenter
                text: "Threat Ping will prioritize alerts for your location."

                color: Colors.text_secondary
                font.pixelSize: Typography.body_small_size
                font.weight: Typography.body_small_weight
                font.letterSpacing: Typography.body_small_spacing
            }


            SearchComboBox {
                id: searchCountry
                Layout.leftMargin: parent.width * 0.20
                Layout.rightMargin: Layout.leftMargin
                Layout.fillWidth: true
                currentIndex: -1

                placeholderText: "Select your region..."

                textRole: "display"

                model: LocationSearchModel {
                    id: locationSearchModel
                }

                onSearchTextChanged: (text) => {
                    locationSearchModel.search(text)
                }

            }

            Item { Layout.fillHeight: true }

            StyledButton {
                Layout.leftMargin: width * 0.05
                Layout.rightMargin: Layout.leftMargin
                Layout.fillWidth: true
                text: qsTr("Next →")

                enabled: searchCountry.currentIndex != -1
                onClicked: {
                    root.onboarding.location = locationSearchModel.get_location(searchCountry.currentIndex)
                    stack.push(notificationSelect)
                }
            }

            Label {
                Layout.alignment: Qt.AlignCenter
                Layout.bottomMargin: 20
                text: "You can change this later in Settings."

                color: Colors.text_disabled
                font.pixelSize: Typography.body_small_size
                font.weight: Typography.body_small_weight
                font.letterSpacing: Typography.body_small_spacing
            }
        }
    }

    Component {
        id: notificationSelect
        ColumnLayout {
            spacing: Sizes.s3
            Item { Layout.fillHeight: true }

            Rectangle {
                Layout.alignment: Qt.AlignCenter
                implicitWidth: 120
                implicitHeight: 120
                color: Colors.surface_elevated
                radius: width / 2
                border.color: Colors.border_strong

                Image {
                    id: icon
                    anchors.centerIn: parent
                    width: 52
                    height: 52

                    source: "assets/icons/lucide--bell.svg"
                    sourceSize.width: width // SVG render size
                    sourceSize.height: height

                    visible: false
                }
                MultiEffect {
                    source: icon
                    anchors.fill: icon
                    colorization: 1.0
                    colorizationColor: Colors.accent_primary
                }
            }

            Label {
                Layout.alignment: Qt.AlignCenter
                Layout.topMargin: 12
                text: "Stay informed"

                color: Colors.text_primary
                font.pixelSize: Typography.hero_size
                font.weight: Typography.hero_weight
                font.letterSpacing: Typography.hero_spacing
            }

            Label {
                Layout.alignment: Qt.AlignCenter
                text: "Choose how you want to be alerted."

                color: Colors.text_secondary
                font.pixelSize: Typography.body_small_size
                font.weight: Typography.body_small_weight
                font.letterSpacing: Typography.body_small_spacing
            }


            RowLayout {
                Layout.topMargin: 12
                Layout.alignment: Qt.AlignHCenter
                spacing: 64
                Label {
                    text: "Sound alerts"
                    color: Colors.text_primary
                    font.pixelSize: Typography.body_small_size
                    font.weight: Typography.body_small_weight
                    font.letterSpacing: Typography.body_small_spacing
                }
                StyledSwitch {
                    id: alertsSwitch
                }
            }

            Item { Layout.fillHeight: true }

            StyledButton {
                Layout.leftMargin: width * 0.05
                Layout.rightMargin: Layout.leftMargin
                Layout.fillWidth: true
                text: qsTr("Next →")

                onClicked: {
                    root.onboarding.notificationsEnabled = alertsSwitch.checked
                    if (root.onboarding.startupEnabled) {
                        console.log("Nitifications enabled")
                    }
                    stack.push(startupSetup)
                }
            }

            Label {
                Layout.alignment: Qt.AlignCenter
                Layout.bottomMargin: 20
                text: "You can change this later in Settings."

                color: Colors.text_disabled
                font.pixelSize: Typography.body_small_size
                font.weight: Typography.body_small_weight
                font.letterSpacing: Typography.body_small_spacing
            }
        }
    }

    // To-Do
    Component {
        id: startupSetup
        ColumnLayout {
            spacing: Sizes.s3
            Item { Layout.fillHeight: true }

            Rectangle {
                Layout.alignment: Qt.AlignCenter
                implicitWidth: 120
                implicitHeight: 120
                // color: Colors.surface_elevated
                // radius: width / 2
                // border.color: Colors.border_strong
                color: "transparent"

                Image {
                    id: icon
                    anchors.centerIn: parent
                    width: 72
                    height: 72

                    source: "assets/icons/lucide--shield-check.svg"
                    sourceSize.width: width // SVG render size
                    sourceSize.height: height

                    visible: false
                }
                MultiEffect {
                    source: icon
                    anchors.fill: icon
                    colorization: 1.0
                    colorizationColor: Colors.threat_all_clear
                }
            }

            Label {
                Layout.alignment: Qt.AlignCenter
                Layout.topMargin: 12
                text: "Threat Ping is ready"

                color: Colors.text_primary
                font.pixelSize: Typography.hero_size
                font.weight: Typography.hero_weight
                font.letterSpacing: Typography.hero_spacing
            }

            Label {
                Layout.alignment: Qt.AlignCenter
                text: "The app will run quietly in your system tray."

                color: Colors.text_secondary
                font.pixelSize: Typography.body_small_size
                font.weight: Typography.body_small_weight
                font.letterSpacing: Typography.body_small_spacing
            }


            RowLayout {
                Layout.topMargin: 12
                Layout.alignment: Qt.AlignHCenter
                spacing: 64
                Label {
                    text: "Launch automatically on startup"
                    color: Colors.text_primary
                    font.pixelSize: Typography.body_small_size
                    font.weight: Typography.body_small_weight
                    font.letterSpacing: Typography.body_small_spacing
                }
                StyledSwitch {
                    id: startupSwitch
                }
            }

            Item { Layout.fillHeight: true }

            StyledButton {
                Layout.leftMargin: width * 0.05
                Layout.rightMargin: Layout.leftMargin
                Layout.fillWidth: true
                Layout.bottomMargin: 20
                text: qsTr("Launch in tray")

                onClicked: {
                    root.onboarding.startupEnabled = startupSwitch.checked
                    if (root.onboarding.startupEnabled) {
                        console.log("Autostart enabled")
                    }
                    root.close()
                }
            }
        }

    }

    Rectangle {
        anchors.fill: parent
        radius: Sizes.radius_lg
        color: Colors.surface

        layer.enabled: true
        clip: true

        StackView {
            id: stack
            anchors.fill: parent
            initialItem: locationSelect

            pushEnter: Transition {
                XAnimator { from: stack.width; to: 0; duration: 280; easing.type: Easing.OutCubic }
            }
            pushExit: Transition {
                XAnimator { from: 0; to: -stack.width; duration: 280; easing.type: Easing.OutCubic }
            }
            popEnter: Transition {
                XAnimator { from: -stack.width; to: 0; duration: 280; easing.type: Easing.OutCubic }
            }
            popExit: Transition {
                XAnimator { from: 0; to: stack.width; duration: 280; easing.type: Easing.OutCubic }
            }
        }
    }
}
