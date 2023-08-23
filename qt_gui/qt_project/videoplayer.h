#ifndef VIDEOPLAYER_H
#define VIDEOPLAYER_H

#include <QMainWindow>
#include <QtNetwork/QTcpSocket>
#include <QtNetwork/QHostAddress>
#include <QMessageBox>
#include <QDebug>
#include <QDataStream>
#include <QString>
#include <QByteArray>

#include <QVideoWidget>
#include <QMediaPlayer>
#include <QVideoSurfaceFormat>

#include <opencv2/opencv.hpp>
#include <QLabel>
#include <QTimer>

class VideoPlayer : public QDialog
{
    Q_OBJECT

public:
    VideoPlayer(QWidget *parent = nullptr);
    ~VideoPlayer();

private slots:
    void playNextFrame(const QImage& image);
    void Read_Data_From_Socket(); // Refactor > add definition in mainwindow.cpp
    QImage matToQImage(const cv::Mat& mat);
    void Read_Data_From_Socket1();

private:
    QLabel *frameLabel;
//    QPushButton *closeButton;
//    cv::VideoCapture videoCapture;
    QTimer *frameTimer;

    QTcpSocket *TCPSocket;
    QVideoWidget *videoWidget;
    QMediaPlayer *mediaPlayer;
    QVideoSurfaceFormat *videoSurfaceFormat;

};

#endif // VIDEOPLAYER_H
