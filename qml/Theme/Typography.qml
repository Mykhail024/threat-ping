pragma Singleton
import QtQuick

QtObject {

    // Hero Label — 20px / Semibold / -0.3px tracking
    readonly property int    hero_size:    20
    readonly property int    hero_weight:  Font.DemiBold   // 600 = semibold
    readonly property real   hero_spacing: -0.3

    // Section Title — 13px / Semibold / +0.4px tracking / Uppercase
    readonly property int    section_size:      13
    readonly property int    section_weight:    Font.DemiBold   // 600
    readonly property real   section_spacing:   0.4
    readonly property bool   section_uppercase: true

    // Body — 13px / Regular
    readonly property int    body_size:    13
    readonly property int    body_weight:  Font.Normal     // 400
    readonly property real   body_spacing: 0

    // Body Small — 12px / Regular
    readonly property int    body_small_size:    12
    readonly property int    body_small_weight:  Font.Normal    // 400
    readonly property real   body_small_spacing: 0

    // Micro — 11px / Medium
    readonly property int    micro_size:    11
    readonly property int    micro_weight:  Font.Medium    // 500
    readonly property real   micro_spacing: 0
}
