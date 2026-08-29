#include <QtGui/QGuiApplication>

#include "Application.h"

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    threatping::Application app_(&app);

    return app.exec();
}
