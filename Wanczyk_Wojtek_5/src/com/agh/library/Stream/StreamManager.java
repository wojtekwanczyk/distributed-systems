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
    private ActorRef child;
    private TitleActor new_request;
    private Integer nr = 0;

    @Override
    public Receive createReceive() {
        return receiveBuilder()
                .match(Title.class, request -> {
                    new_request = new TitleActor(request.title, getSender());
                    String name = getName();
                    child = context().actorOf(Props.create(StreamSupervisor.class), name);
                    child.tell(new_request, getSelf());
                })
                .matchAny(o -> log.info("received unknown message"))
                .build();
    }

    private String getName(){
        nr++;
        return "streamSupervisor" + nr.toString();
    }
}
