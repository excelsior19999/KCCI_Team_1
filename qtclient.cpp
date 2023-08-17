// g++ qtclient.cpp -o qtclient
// socket client
#include <iostream>
#include <cstring>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <string>

// qt pub
#include <iostream>
#include <mqtt/async_client.h>

const std::string ServerIP = "192.168.100.75";
const int mqttPort = 1888;
const int serverPort = 9899;
// const std::string SERVER_ADDRESS("192.168.100.75:1888");
const std::string CLIENT_ID("ddukNip_pub");

class MyCallback : public virtual mqtt::callback {
public:
    void connection_lost(const std::string& cause) override {
        std::cout << "Connection lost: " << cause << std::endl;
    }
};

int mqtt_pub() {
    mqtt::async_client client(ServerIP + ":" + mqttPort, CLIENT_ID);

    mqtt::connect_options connOpts;
    connOpts.set_keep_alive_interval(20);
    connOpts.set_clean_session(true);

    MyCallback callback;
    client.set_callback(callback);

    try {
        mqtt::token_ptr conntok = client.connect(connOpts);
        conntok->wait();
        
        std::string topic = "vigilante/action";
        std::string payload = "MQTT MSG action..";
        int qos = 1;
        bool retained = false;

        mqtt::message_ptr pubmsg = mqtt::make_message(topic, payload);
        pubmsg->set_qos(qos);
        pubmsg->set_retained(retained);

        client.publish(pubmsg)->wait_for(TIMEOUT);
    }
    catch (const mqtt::exception& exc) {
        std::cerr << "Error: " << exc.what() << std::endl;
        return 1;
    }

    return 0;
}

int socket_client() {
    int clientSocket;
    sockaddr_in serverAddr;

    // Create socket
    clientSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (clientSocket == -1) {
        perror("Socket creation error");
        return 1;
    }

    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = inet_addr(ServerIP);
    serverAddr.sin_port = htons(serverPort);

    // Connect
    if (connect(clientSocket, (struct sockaddr *)&serverAddr, sizeof(serverAddr)) == -1) {
        perror("Connection error");
        close(clientSocket);
        return 1;
    }

    const char *message = "Hello, Server!";
    send(clientSocket, message, strlen(message), 0);

    char buffer[1024];
    ssize_t bytesRead = recv(clientSocket, buffer, sizeof(buffer), 0);
    if (bytesRead > 0) {
        buffer[bytesRead] = '\0';
        std::cout << "Received from server: " << buffer << std::endl;
    } else {
        perror("Receiving error");
    }

    close(clientSocket);

    return 0;
}


int main(int argc, char* argv[]) {
    // mqtt_pub();
    // socket_client();

    // 스레드 객체를 생성하고 함수와 인자 전달
    std::thread t1(mqtt_pub);
    std::thread t2(socket_client);

    // 스레드 실행 대기
    t1.join();
    t2.join();

    std::cout << "Main thread finished" << std::endl;

    return 0;
}





