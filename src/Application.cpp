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
QStringList Application::defaultProvidersDir()
{
    QStringList dirs;

    const char *env = std::getenv("THREAT_PING_PROVIDERS_DIR");
    if (env && *env) {
        const QString envDir = QString::fromUtf8(env);
        if (QDir(envDir).exists()) {
            dirs.append(envDir);
        } else {
            Log_Warning(
                QString("THREAT_PING_PROVIDERS_DIR is set, but directory does not exist: %1")
                    .arg(envDir));
        }
    }

    const QString appDir = QCoreApplication::applicationDirPath();
    const QString relative = appDir + "/plugins/providers";
    if (QDir(relative).exists()) {
        dirs.append(relative);
    } else {
        Log_Warning(QString("Relative providers directory does not exist: %1").arg(relative));
    }

    const QString systemDir = QString::fromUtf8(THREAT_PROVIDER_PLUGIN_INSTALL_DIR);
    if (QDir(systemDir).exists()) {
        dirs.append(systemDir);
    } else {
        Log_Warning(QString("System providers directory does not exist: %1").arg(systemDir));
    }

    return dirs;
}

Application::Application(QObject *parent)
    : QObject(parent)
    , m_pRegistry(new pCore::ProvidersRegistry(this))
{
    Log_Info(std::string("Starting ThreatPing version ") + THREAT_PING_VERSION);

    for (const auto &dir : defaultProvidersDir()) {
        registerThreatProviders(dir);
    }

    Log_Info(QString("Loaded %1 threat providers").arg(m_pRegistry->count()));
}

void Application::registerThreatProviders(const QString &folder_path)
{
    Log_Info(QString("Loading threat providers from: %1").arg(folder_path));

    QDir dir(folder_path);

    dir.setFilter(QDir::Files);

    const QStringList filters = {"*.so", "*.dll", "*.dylib"};

    dir.setNameFilters(filters);

    for (const auto &fileName : dir.entryList()) {
        const QString filePath = dir.filePath(fileName);

        auto loader = QSharedPointer<QPluginLoader>::create(filePath);

        QObject *pluginObj = loader->instance();
        if (!pluginObj) {
            Log_Warning(
                QString("Failed to load plugin %1: %2").arg(filePath, loader->errorString()));
            continue;
        }

        auto *provider = qobject_cast<pApi::IThreatProvider *>(pluginObj);

        if (!provider) {
            Log_Warning(QString("Plugin does not implement IThreatProvider: %1").arg(filePath));
            loader->unload();
            continue;
        }

        m_pRegistry->registerProvider(provider, loader);
    }
}
} // namespace threatping
