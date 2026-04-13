pragma Singleton
import QtQuick

QtObject {
    // Background Layers
    readonly property color background: "#0f0f10"
    readonly property color surface: "#1a1a1d"
    readonly property color surface_elevated: "#222226"
    readonly property color surface_hover: "#2a2a2f"
    readonly property color border_subtle: "#2e2e34"
    readonly property color border_strong: "#3e3e46"

    // Text Colors
    readonly property color text_primary: "#f0f0f2"
    readonly property color text_secondary: "#9999a8"
    readonly property color text_disabled: "#55555f"

    // UI Accents
    readonly property color accent_primary: "#6366f1"
    readonly property color accent_hover: "#4f46e5"
    readonly property color accent_destructive: "#ef4444"

    // Threat Accent Colors
    readonly property color threat_air_alert:  "#ef4444"
    readonly property color threat_earthquake: "#f97316"
    readonly property color threat_weather:    "#eab308"
    readonly property color threat_flood:      "#3b82f6"
    readonly property color threat_wildfire:   "#f43f5e"
    readonly property color threat_chemical:   "#a855f7"
    readonly property color threat_all_clear:  "#22c55e"
    readonly property color threat_unknown:    "#6b7280"
}
