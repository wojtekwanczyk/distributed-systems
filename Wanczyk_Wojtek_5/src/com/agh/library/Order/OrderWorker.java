package com.agh.library.Order;

import akka.actor.AbstractActor;
import akka.event.Logging;
import akka.event.LoggingAdapter;
import com.agh.helpers.other.Price;
import com.agh.helpers.other.Response;
import com.agh.helpers.titles.TitleDatabase;

import java.io.BufferedReader;
import java.io.FileReader;

public class OrderWorker extends AbstractActor {

    private final LoggingAdapter log = Logging.getLogger(getContext().getSystem(), this);

    @Override
    public Receive createReceive()  {
        return receiveBuilder()
                .match(TitleDatabase.class, request -> {
                    BufferedReader reader = null;
                    try {
                        reader = new BufferedReader(new FileReader(request.database));
                    } catch (Exception e) {
                        System.out.println("Database " + request.database + " not accessible");
                    }
                    String line = null;
                    while (reader != null && (line = reader.readLine()) != null) {
                        if(line.startsWith(request.title)){
                            System.out.println("Found: " + line);
                            break;
                        }
                    }

                    if(line != null){
                        String[] lineSplit = line.split(";");
                        Price price = new Price();
                        price.price = Double.parseDouble(lineSplit[1]);
                        getSender().tell(price, getSelf());
                    } else {
                        getSender().tell(Response.NOT_FOUND, getSelf());
                    }

                    getContext().stop(getSelf());
                })
                .matchAny(o -> log.info("received unknown message"))
                .build();

    }
}
