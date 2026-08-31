#pragma once

#include <QObject>

namespace threatping::providers::core {
class ProvidersRegistry;
}

namespace threatping {
class Application : public QObject
{
        Q_OBJECT
    public:
        explicit Application(QObject *parent = nullptr);

        [[nodiscard]] static QStringList defaultProvidersDir();

    private:
        void registerThreatProviders(const QString &path);

        threatping::providers::core::ProvidersRegistry *m_pRegistry;
};
} // namespace threatping
