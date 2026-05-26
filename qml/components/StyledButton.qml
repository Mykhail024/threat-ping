import QtQuick
import QtQuick.Controls

import Theme

Button {
    id: control

    padding: 12

    contentItem: Item {
        implicitWidth: contentRow.implicitWidth
        implicitHeight: contentRow.implicitHeight

        Row {
            id: contentRow
            anchors.centerIn: parent
            spacing: 8

            Image {
                visible: control.icon.source.toString() !== ""
                source: control.icon.source
                width: 18
                height: 18
                fillMode: Image.PreserveAspectFit
                smooth: true
            }

            Text {
                visible: control.text.length > 0
                text: control.text
                color: control.enabled ? Colors.text_primary : Colors.text_secondary

                font.pixelSize: Typography.body_size
                font.weight: Typography.body_weight

                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                elide: Text.ElideRight

                Behavior on color {
                    ColorAnimation { duration: 150 }
                }
            }
        }
    }

    background: Rectangle {
        color: control.hovered ? Colors.accent_hover : Colors.accent_primary
        border.width: 0
        radius: Sizes.radius_sm

        opacity: control.enabled ? 1.0 : 0.6

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
        }

        Behavior on color {
            ColorAnimation { duration: 150 }
        }

        Behavior on opacity {
            NumberAnimation { duration: 150 }
        }
    }
}
