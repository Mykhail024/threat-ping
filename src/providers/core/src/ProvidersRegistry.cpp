#include <QObject>
#include <smp/log.hpp>

#include "threatping/providers/core/ProvidersRegistry.h"

namespace threatping::providers::core {
ProvidersRegistry::ProvidersRegistry(QObject *parent) : QObject(parent) {}

void ProvidersRegistry::registerProvider(api::IThreatProvider *provider,
                                         QSharedPointer<QPluginLoader> loader)
{
    if (!provider || loader.isNull()) {
        Log_Warning("Plugin instace is null!");
        return;
    }

    const auto metadata = provider->metadata();
    if (metadata.providerId.isEmpty()) {
        Log_Warning("Provider metadata has empty providerId, skipping registration");
        return;
    }

    m_providers.insert(metadata.providerId, {provider, loader});

    auto *obj = qobject_cast<QObject *>(provider);
    if (obj && obj->parent() == nullptr) {
        obj->setParent(this);
    }

    Log_Info(QString("Plugin %1 loaded successful"));
}

int ProvidersRegistry::count() const { return m_providers.size(); }
} // namespace threatping::providers::core
