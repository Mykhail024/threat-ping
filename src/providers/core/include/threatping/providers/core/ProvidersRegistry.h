#pragma once

#include <QHash>
#include <QObject>
#include <QPluginLoader>
#include <QSharedPointer>

#include "threatping/providers/api/IThreatProvider.h"

namespace threatping::providers::core {
class ProvidersRegistry : public QObject
{
        Q_OBJECT
    public:
        explicit ProvidersRegistry(QObject *parent = nullptr);

        void registerProvider(api::IThreatProvider *provider, QSharedPointer<QPluginLoader> loader);

        [[nodiscard]] api::IThreatProvider *provider(const QString &providerId) const;

        [[nodiscard]] int count() const;

    private:
        QHash<QString, QPair<api::IThreatProvider *, QSharedPointer<QPluginLoader>>> m_providers;
};
} // namespace threatping::providers::core
