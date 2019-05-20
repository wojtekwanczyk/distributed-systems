package com.agh.library;

import akka.actor.ActorRef;
import akka.actor.ActorSystem;
import akka.actor.Props;
import com.typesafe.config.Config;
import com.typesafe.config.ConfigFactory;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;

public class Library {

    public static void main(String[] args) throws Exception {
        File configFile = new File("config_library.conf");
        Config config = ConfigFactory.parseFile(configFile);

        // create actor system & actors
        final ActorSystem system = ActorSystem.create("library_system", config);
        final ActorRef findManager = system.actorOf(Props.create(FindManager.class), "findManager");
        final ActorRef orderManager = system.actorOf(Props.create(OrderManager.class), "orderManager");
        final ActorRef streamManager = system.actorOf(Props.create(StreamManager.class), "streamManager");

        // interaction
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        while (true) {
            String line = br.readLine();
            if (line.equals("q")) {
                break;
            }
            findManager.tell(line, null);
        }

        system.terminate();
    }
}
