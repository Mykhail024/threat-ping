import QtQuick
import QtQuick.Controls

import Theme

Switch {
    id: control

    implicitWidth: 50
    implicitHeight: 28

    property color trackOn: Colors.accent_primary
    property color trackOff: Colors.surface_hover
    property color thumbOn: "white"
    property color thumbOff: "white"

    indicator: Rectangle {
        id: track
        anchors.fill: parent
        radius: height / 2
        color: control.checked ? control.trackOn : control.trackOff

        Behavior on color { ColorAnimation {duration: 150 } }

        Rectangle {
            id: thumb
            width: parent.height - 6
            height: parent.height - 6
            radius: width / 2
            anchors.verticalCenter: parent.verticalCenter
            x: control.checked ? parent.width - width - 3 : 3
            color: control.checked ? control.thumbOn : control.thumbOff

            Behavior on x { NumberAnimation { duration: 150; easing.type: Easing.InOutQuad } }
            Behavior on color { ColorAnimation {duration: 150 } }
        }
    }

    background: null
}
