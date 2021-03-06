package com.agh.client;

import akka.actor.ActorRef;
import akka.actor.ActorSystem;
import akka.actor.Props;
import com.agh.helpers.requests.FindRequest;
import com.agh.helpers.requests.OrderRequest;
import com.agh.helpers.requests.StreamRequest;
import com.typesafe.config.Config;
import com.typesafe.config.ConfigFactory;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;

public class Client {

    public static void main(String[] args) throws Exception{
        // config
        File configFile = new File("config_client.conf");
        Config config = ConfigFactory.parseFile(configFile);

        // create actor system & actors
        final ActorSystem system = ActorSystem.create("client_system", config);
        final ActorRef client = system.actorOf(Props.create(ClientActor.class), "client");

        // interaction
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        while (true) {
            String line = br.readLine();
            if (line.equals("q")) {
                break;
            }
            if (line.startsWith("f ")) {
                String[] line_split = line.split(" ", 2);
                String title = line_split[1];
                FindRequest request = new FindRequest(title);
                client.tell(request, null);
                continue;
            }
            if (line.startsWith("o ")) {
                String[] line_split = line.split(" ", 2);
                String title = line_split[1];
                OrderRequest request = new OrderRequest(title);
                client.tell(request, null);
                continue;
            }
            if (line.startsWith("s ")) {
                String[] line_split = line.split(" ", 2);
                String title = line_split[1];
                StreamRequest request = new StreamRequest(title);
                client.tell(request, null);
                continue;
            }
            System.out.println("Unknown command");
        }

        system.terminate();

    }
}
