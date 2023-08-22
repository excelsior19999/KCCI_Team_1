#include "videoplayer.h"
#include <QDebug>

VideoPlayer::VideoPlayer(QWidget *parent)
    : QDialog(parent)
{
    /* Socket Client */
    QString serverAddress = "10.10.14.203";
    quint16 serverPort = 9888;

    TCPSocket = new QTcpSocket();
    TCPSocket->connectToHost(QHostAddress(serverAddress), serverPort);

    // connect 성공 시 메시지가 들어올 때마다 Read_Data_From_Socket() 실행
    connect(TCPSocket, SIGNAL(readyRead()), this, SLOT(Read_Data_From_Socket()));

    TCPSocket->open(QIODevice::ReadWrite);
    {
    if(TCPSocket->isOpen()) {
        QMessageBox::information(this, "Qt Client", "Connected To The Server.");
    } else {
        QMessageBox::information(this, "Qt Client", "Not Connected Server.");
    }
    }

    frameLabel = new QLabel(this);
    frameTimer = new QTimer(this);
    {
//    connect(frameTimer, &QTimer::timeout, this, &VideoPlayer::playNextFrame);

//    QVBoxLayout *layout = new QVBoxLayout;
//    layout->addWidget(frameLabel);
//    setLayout(layout);

//    videoCapture.open(filePath.toStdString());

//    if (!videoCapture.isOpened()) {
//        qDebug() << "Failed to open video file";
//        close();
//    }

//    frameTimer->start(33); // Display at approximately 30 frames per second
//
    }
}

VideoPlayer::~VideoPlayer()
{
    //videoCapture.release();
}

void VideoPlayer::Read_Data_From_Socket1()

{
    if(false){
        //    qDebug() << "Read_Data_From_Socket Start";
        if (TCPSocket) {
            if (TCPSocket->isOpen()) {

                {

                //            QByteArray Data_From_Server = TCPSocket->readAll();
                //            QDataStream DataIn(&Data_From_Server, QIODevice::ReadOnly);
                // 5.15
                //            DataIn.setVersion(QDataStream::Version::Qt_5_15);

                //            QString MessageString = QString::fromStdString(Data_From_Server.toStdString());
                //            QString data = "";
                }

                QByteArray readData;
                const int payload_size = 8;
                //            while (true) {

                if (readData.size() < payload_size) { // 8
                    //                    char packet[4*1024];
                    //readData = TCPSocket->read(4*1024);
                    readData.append(TCPSocket->read(4*1024));
                    //                    int bytesRead = DataIn.; // recv(clientSocket, packet, 4*1024, 0);
                    if (readData.size() <= 0) {
                        return;
                        //                        break;
                    }
                    //                    data += std::string(packet, readData);
                }

                if (readData.isEmpty()) {
                    return;
                    //                    break;
                }
                // Extract msg_size
                QByteArray packed_msg_size = readData.mid(0, payload_size);
                readData = readData.mid(payload_size); // 8~끝

                // 역직렬화를 위해 QByteArray에서 데이터 읽기
                QDataStream inStream(packed_msg_size);
                inStream.setVersion(QDataStream::Version::Qt_5_15); // 동일한 버전 사용

                // 길이 역직렬화
                quint64 msg_size;
                inStream >> msg_size; // 역직렬화된 데이터를 msg_size에 넣기

                int a =0;
                while (static_cast<quint64>(readData.size()) < msg_size) {
                    //                    char packet[4*1024];
                    //                    int bytesRead = recv(clientSocket, packet, 4*1024, 0);
                    //readData = TCPSocket->read(4*1024); //QByteArray
                    readData.append(TCPSocket->read(4*1024));
                    //a++;

                    if (readData.size() <= 0) {
                        break;
                    }
                   if(a<10000000)
                        break;
                    //                    data += std::string(packet, bytesRead);
                }
                qDebug()<< "while end";

                QByteArray frame_data = readData;
                readData = readData.mid(msg_size); // data 초기화

                // data 역직렬화
                // 역직렬화를 위해 QByteArray에서 데이터 읽기
                QDataStream inStream2(frame_data);
                inStream2.setVersion(QDataStream::Version::Qt_5_15); // 동일한 버전 사용
                //                cv::Mat frameCv;
                quint64 frameInt;
                inStream2 >> frameInt;

                {
                //                cv::imshow("RECEIVING VIDEO", frame);
                //                if ((cv::waitKey(10) & 0xFF) == 'q') {
                //                    return;
                //                }






                //                QMainWindow window;
                //                QLabel label(&window);


                //                cv::VideoCapture cap("/home/intel/repo/kcci.intel.ai.project/Class02/smart_factory_src/resources/factory/conveyor.mp4");
                //                if (!cap.isOpened()) {
                //                    qDebug() << "Video not opened.";
                //                    return;
                //                }

                //                cv::Mat frame;
                //                cv::namedWindow("Video Player", cv::WINDOW_NORMAL);
                //                cap >> frame;


                //                qDebug() << "frame type =====>>" << typeid(frame).name();

                //                qDebug() << frameOrg <<  typeid(frameOrg).name();
                }

                // 정수형 변수를 cv::Mat으로 변환
    //            cv::Mat frame = cv::Mat::ones(1, 1, CV_32S) * frameInt;
    //            qDebug() << "frame ===>>" << typeid(frame).name();

                cv::Mat frameMat = cv::Mat::ones(100, 100, CV_8UC3) *static_cast<int>(frameInt); //
                QImage qFrame = matToQImage(frameMat);

                playNextFrame(qFrame);

                /* frame 넣어서 imshow */


                //                QImage qtImage(frame.data, frame.cols, frame.rows, frame.step, QImage::Format_RGB888);
                //                label.setPixmap(QPixmap::fromImage(qtImage));
                //                label.adjustSize();

                //                label.show();
                //                window.show();


                //            }
                // End while

            }
    }    }
}

void VideoPlayer::Read_Data_From_Socket()
{
    if (TCPSocket) {
        if (TCPSocket->isOpen()) {

            QByteArray readData;
//            const int payload_size = 8;

            uint msg_size = 921765;
            //qDebug() << "msg_size(921773, 921765) : " << msg_size << "\n";
            // 921773 // 921765


            int cData = 0;
            while (readData.size() < msg_size) { // static_cast<quint64>
                if (readData.size() < 0) {
                    break;
                }

                cData += 4*1024;
                readData.resize(cData);
                readData.append(TCPSocket->read(4*1024)); // 65536 까지만 담음

                //readData += TCPSocket->read(4*1024);
                qDebug() << "readData.size() 921765 : " << readData.size() << "readData.capacity() : " << readData.capacity() << "\n";
            }
            qDebug() << "while_end";
            readData.resize(msg_size);

            qDebug() << "readData.size() 921765 : " << readData.size() << "\n";

            QByteArray frame_data;
            frame_data.resize(msg_size);
            frame_data = readData;
            qDebug() << "frame_data.size() 921773 : " << frame_data.size() << "\n";

            readData.clear();

            // data 역직렬화
            // 역직렬화를 위해 QByteArray에서 데이터 읽기
            QDataStream inStream2(frame_data);
            inStream2.setVersion(QDataStream::Version::Qt_5_15); // 동일한 버전 사용
            quint64 frameInt;
            inStream2 >> frameInt;


            QImage qImg;

            // 정수형 변수를 cv::Mat으로 변환
            cv::Mat frameMat = cv::Mat::ones(1, 1, CV_32S) * frameInt;
            qDebug() << "frame ===>>" << typeid(frameMat).name();

            QImage qFrame = matToQImage(frameMat);
            qDebug() << "qFrame ===>>" << typeid(qFrame).name() << " size : " << qFrame.size() << "\n";

            playNextFrame(qFrame);

        }
    }
}


void VideoPlayer::playNextFrame(const QImage& image)
{
    if (image.isNull()) {
        frameTimer->stop(); // 이미지가 유효하지 않을 때 타이머를 중지합니다.
        return;
    }

    frameLabel->setPixmap(QPixmap::fromImage(image)); // QImage를 QLabel에 설정하여 이미지를 표시합니다.
    frameLabel->setScaledContents(true); // 이미지를 QLabel의 크기에 맞게 스케일링합니다.
}

//void VideoPlayer::playNextFrame(cv::Mat frame)
//{


//    if (frame.empty()) {
//        frameTimer->stop();
//        return;
//    }

//    cv::cvtColor(frame, frame, cv::COLOR_BGR2RGB);
//    QImage qImage(frame.data, frame.cols, frame.rows, frame.step, QImage::Format_RGB888);

//    frameLabel->setPixmap(QPixmap::fromImage(qImage));
//    frameLabel->setScaledContents(true);
//}

QImage VideoPlayer::matToQImage(const cv::Mat& mat) {
    if (mat.empty()) {
        return QImage();
    }

    if (mat.type() == CV_8UC1) { // 8-bit grayscale image
        return QImage(mat.data, mat.cols, mat.rows, static_cast<int>(mat.step), QImage::Format_Grayscale8);
    } else if (mat.type() == CV_8UC3) { // 8-bit color image
        cv::cvtColor(mat, mat, cv::COLOR_BGR2RGB);
        return QImage(mat.data, mat.cols, mat.rows, static_cast<int>(mat.step), QImage::Format_RGB888);
    } else {
        return QImage(); // Unsupported image format
    }
}
