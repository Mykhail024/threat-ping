import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects

import Theme 1.0
import "components"

ApplicationWindow {
    visible: true
    width: 480
    height: 440
    title: "Threat Ping"
    color: "transparent"

    // Block resize
    minimumWidth: width
    minimumHeight: height
    maximumWidth: width
    maximumHeight: height

    // Disable window decoration
    flags: Qt.FramelessWindowHint | Qt.Window

    Rectangle {
        anchors.fill: parent
        radius: Sizes.radius_lg
        color: Colors.surface

        layer.enabled: true
        clip: true

        ColumnLayout {
            anchors.centerIn: parent
            Rectangle {
                Layout.alignment: Qt.AlignCenter
                implicitWidth: 120
                implicitHeight: 120
                color: Colors.surface_elevated
                radius: Sizes.radius_md
                border.color: Colors.border_strong

                Image {
                    id: icon
                    anchors.centerIn: parent
                    width: 52
                    height: 52

                    source: "assets/icons/lucide--map-pin.svg"
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
                Layout.fillWidth: true
                currentIndex: -1
                // displayText: currentIndex === -1 ? "Select your region..." : currentText
                editable: true

                placeholderText: "Select your region..."

                model: ["Kyiv, Ukraine", "Lviv, Ukraine", "Odesa, Ukraine", "Ternopil, Ukraine"]

            }

            Item { Layout.fillHeight: true }
        }
    }
}
