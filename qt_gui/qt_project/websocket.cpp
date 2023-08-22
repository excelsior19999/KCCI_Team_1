#include "websocket.h"
#include <iostream>

websocket::websocket(QWidget *parent) : QLabel(parent)
{
    setAlignment(Qt::AlignCenter);
    setSizePolicy(QSizePolicy::Ignored, QSizePolicy::Ignored);
    qDebug() << "exception_websocket";
}

void websocket::setWebSocket(QWebSocket *webSocket)
{
    socket = webSocket;
    connect(socket, &QWebSocket::binaryMessageReceived, this, &websocket::onBinaryMessageReceived);
    qDebug() << "exception_setWebSocket ";
}

void websocket::onBinaryMessageReceived(const QByteArray &message)
{
    QImage receivedImage;
    //qDebug() << "exception_onBinaryMessageReceived ";

//    qDebug() << message << "\n";
//    if ( message.isEmpty() ) {
//        qDebug() << "exception_onBinaryMessageReceived_message ";
//    }

    try {
        receivedImage.loadFromData(message);
        setPixmap(QPixmap::fromImage(receivedImage));
    }  catch (const std::bad_alloc &) {
        qDebug() << "exception " ;
    }


}
