#ifndef GOOGLEMAP_H
#define GOOGLEMAP_H

#include <QWidget>
#include <QObject>
#include <QtWebEngineWidgets/QWebEngineView>
#include <QVBoxLayout>
#include <QUrl>

class GoogleMap : public QWebEngineView
{
    Q_OBJECT

public:
    explicit GoogleMap(QWidget *parent = nullptr);

    // Google Maps 설정 함수
    QString loadGoogleMapFromFile(const QString &filePath);
    void setUrl(const QUrl &url);
private:
    //googlemap *webView; // Web View 위젯 포인터

    QString readHtmlFile(const QString &filePath);
};

#endif // GOOGLEMAP_H
