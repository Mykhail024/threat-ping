#pragma once

#include <QObject>

namespace threatping {
class Application : public QObject
{
        Q_OBJECT
    public:
        explicit Application(QObject *parent = nullptr);
};
} // namespace threatping
