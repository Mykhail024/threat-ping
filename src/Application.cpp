#include <QCoreApplication>
#include <QDir>
#include <QJsonDocument>
#include <QJsonObject>
#include <QObject>
#include <QPluginLoader>
#include <smp/log.hpp>

#include "Application.h"
#include "config.h"
#include "threatping/providers/api/IThreatProvider.h"
#include "threatping/providers/core/ProvidersRegistry.h"

namespace pCore = threatping::providers::core;
namespace pApi = threatping::providers::api;

namespace threatping {
Application::Application(QObject *parent)
    : QObject(parent)
    , m_pRegistry(new pCore::ProvidersRegistry(this))
{
    Log_Info(std::string("Starting ThreatPing version ") + THREAT_PING_VERSION);

    const auto THREAT_PROVIDERS_FOLDER = QCoreApplication::applicationDirPath() + "/providers";

    Log_Info(QString("Loading threat providers from: %1").arg(THREAT_PROVIDERS_FOLDER));

    registerThreatProviders(THREAT_PROVIDERS_FOLDER);

    Log_Info(QString("Loaded %1 threat providers").arg(m_pRegistry->count()));
}

void Application::registerThreatProviders(const QString &folder_path)
{
    QDir dir(folder_path);

    dir.setFilter(QDir::Files);

    const QStringList filters = {"*.so", "*.dll", "*.dylib"};

    dir.setNameFilters(filters);

    for (const auto &fileName : dir.entryList()) {
        const QString filePath = dir.filePath(fileName);

        auto loader = QSharedPointer<QPluginLoader>::create(filePath);

        if (!loader->load()) {
            Log_Warning(QString("Failed to load plugin: %1").arg(loader->errorString()));
            continue;
        }

        QObject *pluginObj = loader->instance();
        if (!pluginObj) {
            Log_Warning(
                QString("Failed to load plugin %1 %2").arg(filePath).arg(loader->errorString()));
            continue;
        }

        auto *provider = qobject_cast<pApi::IThreatProvider *>(pluginObj);

        if (!provider) {
            Log_Warning(QString("Plugin doest not implement IThreatProvider: %1").arg(filePath));
            loader->unload();
            continue;
        }

        m_pRegistry->registerProvider(provider, loader);
    }
}
} // namespace threatping
