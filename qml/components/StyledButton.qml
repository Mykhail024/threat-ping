import QtQuick
import QtQuick.Controls

import Theme

Button {
    id: control

    padding: 12

    contentItem: Text {
        text: control.text
        color: control.enabled ? Colors.text_primary : Colors.text_secondary

        font.pixelSize: Typography.body_size
        font.weight: Typography.body_weight

        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight

        Behavior on color { 
            ColorAnimation {duration: 150}
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
            ColorAnimation {duration: 150}
        }

        Behavior on opacity { 
            NumberAnimation {duration: 150}
        }
    }
}
