#ifndef LABELWIDGETWITHSOCKET_H
#define LABELWIDGETWITHSOCKET_H

#include <QLabel>
#include <QWebSocket>

class websocket : public QLabel
{
    Q_OBJECT

public:
    explicit websocket(QWidget *parent = nullptr);

    void setWebSocket(QWebSocket *webSocket);

private slots:
    void onBinaryMessageReceived(const QByteArray &message);

private:
    QWebSocket *socket;
};

#endif // LABELWIDGETWITHSOCKET_H
