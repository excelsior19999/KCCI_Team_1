#include "GoogleMap.h"
#include <iostream>
#include <QFile>
#include <QTextStream>


GoogleMap::GoogleMap(QWidget *parent) : QWebEngineView(parent)
{

}

QString GoogleMap::loadGoogleMapFromFile(const QString &filePath)
{
    QString html = readHtmlFile(filePath);
    //setHtml("<html><body><h1>Hello, World!</h1></body></html>");
    return html;
}
QString GoogleMap::readHtmlFile(const QString &filePath)
{
    QString html;
    QFile file(filePath);
    if (file.open(QIODevice::ReadOnly | QIODevice::Text))//)
    {
        QTextStream in(&file);
        html = in.readAll();
        file.close();
    }
    return html;
}

void GoogleMap::setUrl(const QUrl &url)
{
    QWebEngineView::setUrl(url);
    // 필요한 추가 작업을 수행합니다.
}
