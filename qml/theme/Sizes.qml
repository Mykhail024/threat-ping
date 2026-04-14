pragma Singleton
import QtQuick

QtObject {

    // Spacing Scale (4px base)
    readonly property int s1:  4
    readonly property int s2:  8
    readonly property int s3:  12
    readonly property int s4:  16
    readonly property int s5:  20
    readonly property int s6:  24
    readonly property int s8:  32
    readonly property int s10: 40
    readonly property int s12: 48

    // Border Radius
    readonly property int radius_pill:   999   // full pill — badges, chips
    readonly property int radius_sm:     6     // buttons, inputs
    readonly property int radius_md:     10    // cards, panels
    readonly property int radius_lg:     12    // modal / window outer
}
