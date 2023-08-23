#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QDebug>
#include "MapWindow.h"
#include "websocket.h"
#include <QtWidgets>
#include <QtWebSockets/QWebSocket>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    void onOpenSteamingClicked();

private slots:
    void onOpenMapClicked();
    void onConnected();
    void lineEditFont();

private:
    Ui::MainWindow *ui;
    MapWindow *mapWindow;
    QWebSocket *socket;
    QLabel *videoLabel;

};
#endif // MAINWINDOW_H
