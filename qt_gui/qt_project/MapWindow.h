#ifndef MAPWINDOW_H
#define MAPWINDOW_H

#include <QMainWindow>
#include "GoogleMap.h"

class MapWindow : public QMainWindow
{
    Q_OBJECT

public:
    MapWindow(QWidget *parent = nullptr);
};

#endif // MAPWINDOW_H
