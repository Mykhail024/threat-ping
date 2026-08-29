#include <QCoreApplication>
#include <QObject>
#include <smp/log.hpp>
namespace threatping {
Application::Application(QObject *parent)
    : QObject(parent)
{
    Log_Info(std::string("Starting ThreatPing version ") + THREAT_PING_VERSION);
}
} // namespace threatping
