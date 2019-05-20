package com.agh.library.Order;

import akka.actor.AbstractActor;
import akka.event.Logging;
import akka.event.LoggingAdapter;
import com.agh.helpers.other.Response;
import com.agh.helpers.titles.Title;

import java.io.BufferedWriter;
import java.io.FileWriter;

public class SaveOrderWorker extends AbstractActor {

    private final LoggingAdapter log = Logging.getLogger(getContext().getSystem(), this);
    private final String orders = "data/orders.txt";

    @Override
    public Receive createReceive()  {
        return receiveBuilder()
                .match(Title.class, request -> {
                    BufferedWriter writer = null;
                    try {
                        writer = new BufferedWriter(new FileWriter(orders, true));
                        System.out.println("Saving order, title: " + request.title);
                        String msg = request.title + "\n";
                        writer.write(msg);
                        writer.close();
                        System.out.println("Saving order successful");
                    } catch (Exception e) {
                        System.out.println("Unable to write to file  " + orders);
                        getSender().tell(Response.SAVE_ERROR, getSelf());
                    }
                    getSender().tell(Response.SAVE_SUCCESS, getSelf());
                })
                .matchAny(o -> log.info("received unknown message"))
                .build();

    }
}
