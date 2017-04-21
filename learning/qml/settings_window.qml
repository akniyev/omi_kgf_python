import QtQuick 2.0
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.3
import QtQuick.Dialogs 1.1
import MyPaintedItem 1.1

Rectangle {
    id: mainRect
    objectName: "main_rect"
    width: 300; height: 600

    MessageDialog {
            id: msg
            title: "Title"
            text: "Button pressed"
            onAccepted: visible = false
        }

    ColumnLayout {
        id: columnLayout
        anchors.rightMargin: 5
        anchors.leftMargin: 5
        anchors.bottomMargin: 5
        anchors.topMargin: 5
        anchors.fill: parent

        MyPaintedItem {
            id: paintedItem
            objectName: "paintedItem"
        }

        Label {
            id: lb_name
            text: qsTr("Name")
            Layout.fillWidth: true
        }

        TextField {
            id: tf_name
            objectName: "name_field"
            x: 8
            y: 232
            Layout.fillWidth: true
            placeholderText: qsTr("Node name")
        }

        Label {
            id: lb_inputs
            text: qsTr("Inputs")
        }


        TextField {
            id: tf_inputs
            x: 8
            y: 232
            Layout.fillWidth: true
            placeholderText: qsTr("Node inputs")
        }

        Label {
            id: lb_outputs
            x: 13
            y: 105
            text: qsTr("Outputs")
        }

        TextField {
            id: tf_outputs
            x: 24
            y: 87
            Layout.fillWidth: true
            placeholderText: qsTr("Node outputs")
        }

        Label {
            id: lb_function
            text: qsTr("Function body")
        }



        TextArea {
            id: ta_function
            x: 8
            y: 264
            Layout.fillHeight: true
            Layout.fillWidth: true
        }

        RowLayout {
            id: rowLayout
            width: 100
            height: 100
            Layout.preferredHeight: 10

            Button {
                id: b_save
                objectName: "button_save"

                text: qsTr("Save")
                Layout.fillHeight: true
                Layout.fillWidth: true
                signal pressed(string name)
                onClicked: {
                    this.pressed(this.objectName)
                }
            }

            Button {
                id: b_reset
                objectName: "button_reset"
                text: qsTr("Reset")
                Layout.fillHeight: true
                Layout.fillWidth: true
            }
        }


    }
}
