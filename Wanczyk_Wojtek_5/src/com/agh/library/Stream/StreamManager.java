package com.agh.library.Stream;

import akka.actor.AbstractActor;
import akka.actor.ActorRef;
import akka.actor.Props;
import akka.event.Logging;
import akka.event.LoggingAdapter;
import com.agh.helpers.titles.Title;
import com.agh.helpers.titles.TitleActor;

public class StreamManager extends AbstractActor {
    private final LoggingAdapter log = Logging.getLogger(getContext().getSystem(), this);
    private Integer nr = 0;

    @Override
    public Receive createReceive() {
        return receiveBuilder()
                .match(Title.class, request -> {
                    TitleActor new_request = new TitleActor(request.title, getSender());
                    String childName = getName();
                    ActorRef child = context().actorOf(Props.create(StreamSupervisor.class), childName);
                    child.tell(new_request, getSelf());
                })
                .matchAny(o -> log.info("received unknown message"))
                .build();
    }

    private String getName(){
        nr++;
        return "streamSupervisor" + nr.toString();
    }

    //@Override
    //public void preStart() throws Exception {
        //context().actorOf(Props.create(LibraryActor.class), "libraryWorker");
    //}
}
