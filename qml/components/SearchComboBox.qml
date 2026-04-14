pragma ComponentBehavior: Bound

import QtQuick
import QtQuick.Controls

import Theme

ComboBox {
    id: control

    property string placeholderText
    property int debounceMsec: 500

    signal searchTextChanged(string text)

    background: Rectangle {
        implicitWidth: 140
        implicitHeight: 40

        color: Colors.surface_elevated
        radius: Sizes.radius_sm
        border.width: 1
        border.color: Colors.border_subtle
    }

    contentItem: Text {
        text: control.displayText === "" ? control.placeholderText : control.displayText

        elide: Text.ElideRight
        clip: true
        maximumLineCount: 1

        color: Colors.text_primary
        font.pixelSize: Typography.body_size
        font.weight: Typography.body_weight
        font.letterSpacing: Typography.body_spacing
        verticalAlignment: Text.AlignVCenter
        padding: 12
    }

    popup: Popup {
        id: popup

        y: control.height + 2
        width: control.width
        implicitHeight: contentItem.implicitHeight
        padding: 1

        onOpened: {
            searchText.forceActiveFocus()
            searchText.selectAll()
        }

        background: Rectangle {
            color: Colors.surface_elevated

            border.width: 1
            border.color: Colors.border_subtle
        }

        Timer {
            id: debounce
            interval: control.debounceMsec
            repeat: false
            property string pending: ""
            onTriggered: control.searchTextChanged(pending)
        }

        contentItem: Column {
            width: parent.width

            TextField {
                id: searchText

                width: parent.width

                implicitHeight: 40
                padding: 10

                focus: false

                selectByMouse: true
                hoverEnabled: true

                wrapMode: TextField.WrapAnywhere

                placeholderText: qsTr("Search...")

                background: Rectangle {
                    color: "transparent"
                }

                onTextChanged: {
                    if(text.length > 0) {
                        debounce.pending = text
                        debounce.restart()
                    } else {
                        debounce.stop()
                    }
                }
            }

            ListView {
                clip: true
                width: parent.width

                height: Math.min(contentHeight, 80)

                model: control.popup.visible ? control.delegateModel : null
                currentIndex: control.highlightedIndex

                ScrollIndicator.vertical: ScrollIndicator {}
            }
        }
    }

    delegate: ItemDelegate {
        id: delegate_

        width: control.width
        height: control.height

        required property int index
        required property var modelData

        contentItem: Text {
            text: typeof delegate_.modelData === "string"
                ? delegate_.modelData
                : (delegate_.modelData?.[control.textRole] ?? "")

            elide: Text.ElideRight
            clip: true
            maximumLineCount: 1

            color: Colors.text_primary
            font.pixelSize: Typography.body_size
            font.weight: Typography.body_weight
            font.letterSpacing: Typography.body_spacing
            verticalAlignment: Text.AlignVCenter
        }

        background: Rectangle {
            color: delegate_.highlighted ? Colors.surface_hover : Colors.surface_elevated
        }
        highlighted: control.highlightedIndex === index
    }
}
