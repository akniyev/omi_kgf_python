import QtQuick 2.0
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.3

Rectangle {
    width: 600; height: 600

    ColumnLayout {
        id: columnLayout
        x: 8
        y: 8
        width: 234
        height: 283

        Label {
            id: label
            text: qsTr("Name")
            Layout.fillWidth: true
        }

        TextField {
            id: textField
            x: 8
            y: 232
            Layout.fillWidth: true
            placeholderText: qsTr("Text Field")
        }

        Label {
            id: label1
            text: qsTr("Inputs")
        }


        TextField {
            id: textField1
            x: 8
            y: 232
            Layout.fillWidth: true
            placeholderText: qsTr("Text Field")
        }

        Label {
            id: label2
            text: qsTr("Function body")
        }

        TextArea {
            id: textArea
            x: 8
            y: 264
            Layout.fillHeight: true
            Layout.fillWidth: true
        }
    }
}
