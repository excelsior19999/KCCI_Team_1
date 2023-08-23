QT       += core gui multimedia multimediawidgets webenginewidgets network websockets
greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++17

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    GoogleMap.cpp \
    MapWindow.cpp \
    main.cpp \
    mainwindow.cpp \
    websocket.cpp

HEADERS += \
    GoogleMap.h \
    MapWindow.h \
    mainwindow.h \
    websocket.h

FORMS += \
    mainwindow.ui

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

OPENCV_PATH = /usr/local//include/opencv4/
INCLUDEPATH += $$OPENCV_PATH

OPENCV_PATH_lib = /usr/local/lib/
LIBS += -L$$OPENCV_PATH_lib/lib -lopencv_core -lopencv_imgproc -lopencv_highgui -lopencv_videoio
BuildRequires:  pkgconfig(Qt5WebSockets)
