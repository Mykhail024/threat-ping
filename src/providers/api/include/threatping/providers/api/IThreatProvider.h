#pragma once

#include <QObject>

#include "ProviderMetadata.h"

namespace threatping::providers::api {

class IThreatProvider : public QObject
{
    public:
        virtual ~IThreatProvider() = default;

        [[nodiscard]] virtual ProviderMetadata metadata() const = 0;
};

} // namespace threatping::providers::api

#define IThreatProvider_iid "ThreatPing.IThreatProvider/1.0"
Q_DECLARE_INTERFACE(threatping::providers::api::IThreatProvider, IThreatProvider_iid)
