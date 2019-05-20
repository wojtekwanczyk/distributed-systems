package com.agh.library.Find;

import akka.actor.AbstractActor;
import akka.actor.ActorRef;
import akka.actor.Props;
import akka.event.Logging;
import akka.event.LoggingAdapter;
import com.agh.helpers.other.Price;
import com.agh.helpers.other.Response;
import com.agh.helpers.titles.TitleActor;
import com.agh.helpers.titles.TitleDatabase;

public class FindSupervisor extends AbstractActor {
    private final LoggingAdapter log = Logging.getLogger(getContext().getSystem(), this);
    private Integer nr = 0;
    private ActorRef actor;

    @Override
    public AbstractActor.Receive createReceive() {
        return receiveBuilder()
                .match(TitleActor.class, request -> {
                    actor = request.actor;
                    TitleDatabase title = new TitleDatabase(request.title, "data/db1.txt");
                    String childName = getName();
                    ActorRef child = context().actorOf(Props.create(FindWorker.class), childName);
                    child.tell(title, getSelf());

                    title = new TitleDatabase(request.title, "data/db2.txt");
                    childName = getName();
                    child = context().actorOf(Props.create(FindWorker.class), childName);
                    child.tell(title, getSelf());
                })
                .match(Price.class, price -> {
                    actor.tell(price, getSelf());
                    getContext().stop(getSelf());
                })
                .match(Response.class, response -> {
                    if(response.equals(Response.NOT_FOUND)){
                        nr--;
                        if(nr.equals(0)){
                            actor.tell(response, getSelf());
                            getContext().stop(getSelf());
                        }
                    }
                })
                .matchAny(o -> log.info("received unknown message"))
                .build();
    }

    private String getName(){
        nr++;
        return "findWorker" + nr.toString();
    }

    //@Override
    //public void preStart() throws Exception {
    //context().actorOf(Props.create(LibraryActor.class), "libraryWorker");
    //}
}
