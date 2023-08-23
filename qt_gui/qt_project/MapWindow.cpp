#include "MapWindow.h"
#include <QVBoxLayout>


// 지도 팝업 화면


MapWindow::MapWindow(QWidget *parent)
    : QMainWindow(parent)
{
    setWindowTitle("Map Window");

    QVBoxLayout *layout = new QVBoxLayout(this);

    // Create a GoogleMap widget
    GoogleMap *mapView = new GoogleMap(this);
    mapView->setHtml(mapView->loadGoogleMapFromFile("/home/intel/teamProject/team1/map.html"));
    mapView->setMinimumSize(1200, 700);
    mapView->setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding);

    layout->addWidget(mapView);
    setFixedSize(1200, 700);

}
