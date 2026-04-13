import QtQuick
import QtQuick.Controls

ComboBox {
    id: root

    property string placeholderText: "Search city..."

    // Do not use built-in ComboBox model; model is passed only to custom popup
    model: null
    textRole: ""
    editable: true

    popup: Popup {
        y: root.height
        width: root.width
        implicitHeight: contentItem.implicitHeight
        padding: 1
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

        contentItem: ListView {
            id: listView
            clip: true
            implicitHeight: contentHeight
            model: searchModel
            delegate: ItemDelegate {
                width: root.width
                highlighted: listView.currentIndex === index
                onClicked: {
                    root.currentIndex = index
                    root.activated(index)
                    root.popup.close()
                }

                contentItem: Text {
                    text: model.cityName ? model.cityName : "Bug!"
                    color: highlighted ? "lightblue" : "white"
                    font: root.font
                    verticalAlignment: Text.AlignVCenter
                    elide: Text.ElideRight
                }

                background: Rectangle {
                    color: highlighted ? "#2a5a8c" : "transparent"
                }
            }
        }
    }

    Timer {
        id: typingTimer
        interval: 600
        repeat: false
        onTriggered: {
            if (root.editText.length >= 3) {
                console.log("Search triggered: " + root.editText)
                searchModel.search(root.editText)
            }
        }
    }

    contentItem: TextField {
        text: root.editText
        placeholderText: root.placeholderText
        font: root.font
        verticalAlignment: Text.AlignVCenter

        onTextEdited: typingTimer.restart()
    }

    Connections {
        target: searchModel
        function onModelReset() {
            console.log("Model updated, row count:", searchModel.rowCount())
            if (searchModel.rowCount() > 0) {
                root.popup.open()
            } else {
                root.popup.close()
            }
        }
    }

    onActivated: function(index) {
        let selected = searchModel.get_location(index)
        if (selected && selected.display_name) {
            root.editText = selected.display_name
            console.log("Selected:", selected.display_name)
        }
    }

    Component.onCompleted: {
        console.log("ComboBox ready")
    }
}