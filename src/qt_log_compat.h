#pragma once

#include <QString>
#include <ostream>

inline std::ostream &operator<<(std::ostream &out, const QString &str)
{
    return out << str.toUtf8().constData();
}
