package com.agh.library.Order;

import akka.actor.AbstractActor;
import akka.actor.ActorRef;
import akka.actor.Props;
import akka.event.Logging;
import akka.event.LoggingAdapter;
import com.agh.helpers.other.Price;
import com.agh.helpers.other.Response;
import com.agh.helpers.titles.Title;
import com.agh.helpers.titles.TitleActor;
import com.agh.helpers.titles.TitleDatabase;
import com.agh.library.Find.FindWorker;

public class OrderSupervisor extends AbstractActor {
    private final LoggingAdapter log = Logging.getLogger(getContext().getSystem(), this);
    private Integer nr = 0;
    private ActorRef actor;
    private Title title;
    private boolean found = false;
    private ActorRef saver = context().actorOf(Props.create(SaveOrderWorker.class), "saveOrderWorker");

    @Override
    public Receive createReceive() {
        return receiveBuilder()
                .match(TitleActor.class, request -> {
                    actor = request.actor;
                    title = new Title(request.title);
                    TitleDatabase title = new TitleDatabase(request.title, "data/db1.txt");
                    String childName = getName();
                    ActorRef child = context().actorOf(Props.create(FindWorker.class), childName);
                    child.tell(title, getSelf());

                    title = new TitleDatabase(request.title, "data/db2.txt");
                    childName = getName();
                    child = context().actorOf(Props.create(FindWorker.class), childName);
                    child.tell(title, getSelf());
                })
                .match(Price.class, price_ret -> {
                    //save order
                    // same title in two databases
                    if(!found) {
                        found = true;
                        saver.tell(title, getSelf());
                    }
                })
                .match(Response.class, response -> {
                    if(response.equals(Response.NOT_FOUND)){
                        nr--;
                        if(nr.equals(0)){
                            actor.tell(response, getSelf());
                            getContext().stop(getSelf());
                        }
                    }
                    if(response.equals(Response.SAVE_ERROR)){
                        actor.tell(response, getSelf());
                        getContext().stop(getSelf());
                    }
                    if(response.equals(Response.SAVE_SUCCESS)){
                        actor.tell(response, getSelf());
                        getContext().stop(getSelf());
                    }
                })
                .matchAny(o -> log.info("received unknown message"))
                .build();
    }

    private String getName(){
        nr++;
        return "Worker" + nr.toString();
    }

}
