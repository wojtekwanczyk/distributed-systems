package com.company;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.net.*;
import java.time.LocalDateTime;

public class Main {

    public static void main(String[] args) {
        MulticastSocket socket = null;
        int port = Integer.parseInt(args[0]);
        try {
            socket = new MulticastSocket(port);
        } catch (IOException e) {
            e.printStackTrace();
        }
        InetAddress group = null;
        try {
            group = InetAddress.getByName("224.100.0.1");
        } catch (UnknownHostException e) {
            e.printStackTrace();
        }
        try {
            socket.joinGroup(group);
        } catch (IOException e) {
            e.printStackTrace();
        }

        byte[] buff = new byte[1024];
        String full_log = "";
        BufferedWriter writer = null;
        String filename = "log_" + Integer.toString(port )+ ".txt";
        for(int i=0;  ;i++) {
            DatagramPacket packet = new DatagramPacket(buff, buff.length);
            try {
                socket.receive(packet);
            } catch (IOException e) {
                e.printStackTrace();
            }
            String received = new String(
                    packet.getData(), 0, packet.getLength());
            if ("end".equals(received)) {
                break;
            }
            LocalDateTime date = LocalDateTime.now();
            String log = date.toString() + ":\t" + received;
            System.out.println(log);
            full_log = full_log + "\n " + log;

            if(i % 10 == 0){
                try {
                    writer = new BufferedWriter(new FileWriter(filename, true));
                    writer.write(full_log);
                    writer.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                full_log = "";
            }
        }
        try {
            socket.leaveGroup(group);
        } catch (IOException e) {
            e.printStackTrace();
        }
        socket.close();





    }
}
