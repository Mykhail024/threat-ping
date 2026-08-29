#pragma once

#include <QString>
#include <QVector>

#include "ProviderCapabilities.h"

namespace threatping::providers::api {
struct ProviderMetadata
{
        QString providerId;
        QString name;
        QString description;
        QVector<ThreadProviderCapabilities> capabilities;
};
} // namespace threatping::providers::api
