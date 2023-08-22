#include "mainwindow.h"

#include <QApplication>
#include <opencv4/opencv2/opencv.hpp>


int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();
    return a.exec();
}
