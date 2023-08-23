#include "mainwindow.h"
#include "ui_mainwindow.h"


MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    //, ui(new Ui::MainWindow)
{
    // Set up UI
    ui = new Ui::MainWindow;
    ui->setupUi(this);

    // Create a WebSocket connection to the server
    socket = new QWebSocket;
    connect(socket, &QWebSocket::connected, this, &MainWindow::onConnected);
    socket->open(QUrl("ws://10.10.14.21:5000"));

    // Pass the socket to the label widget
    ui->label->setWebSocket(socket);

    connect(ui->pushButton, &QPushButton::clicked, this, &MainWindow::onOpenMapClicked);

    lineEditFont();
}

MainWindow::~MainWindow()
{
    delete ui;
}



void MainWindow::onOpenMapClicked()
{
    mapWindow = new MapWindow(this); // 새로운 MapWindow 인스턴스 생성
    mapWindow->show(); // 새 창을 보여줌

}

void MainWindow::onConnected()
{
    qDebug() << "Connected to the server.";
    // You can perform any actions here upon successful connection
}

void MainWindow::lineEditFont()
{
    QFont font;
    font.setPointSize(16);
    font.setFamily("Palatino");
    ui->lineEdit->setFont(font);
}

