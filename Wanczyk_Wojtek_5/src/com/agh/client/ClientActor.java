package com.agh.client;

import akka.actor.AbstractActor;
import akka.event.Logging;
import akka.event.LoggingAdapter;
import com.agh.helpers.other.Price;
import com.agh.helpers.other.Response;
import com.agh.helpers.requests.FindRequest;
import com.agh.helpers.requests.OrderRequest;
import com.agh.helpers.requests.StreamRequest;
import com.agh.helpers.titles.Title;
import com.agh.library.Find.FindManager;

public class ClientActor extends AbstractActor {
    private final LoggingAdapter log = Logging.getLogger(getContext().getSystem(), this);
    private FindManager library;


    @Override
    public AbstractActor.Receive createReceive() {
        return receiveBuilder()
                .match(FindRequest.class, request -> {
                    Title title = new Title(request.title);
                    getContext()
                            .actorSelection("akka.tcp://library_system@127.0.0.1:3553/user/findManager")
                            .tell(title, getSelf());
                })
                .match(OrderRequest.class, request -> {
                    Title title = new Title(request.title);
                    getContext()
                            .actorSelection("akka.tcp://library_system@127.0.0.1:3553/user/findManager")
                            .tell(title, getSelf());
                })
                .match(StreamRequest.class, request -> {
                    Title title = new Title(request.title);
                    getContext()
                            .actorSelection("akka.tcp://library_system@127.0.0.1:3553/user/findManager")
                            .tell(title, getSelf());
                })
                .match(Price.class, price -> {
                    System.out.println("Price: " + price.price);
                })
                .match(Response.class, response -> {
                    System.out.println(response);
                })
                .matchAny(o -> log.info("received unknown message"))
                .build();
    }


    @Override
    public void preStart() throws Exception {
        //context().actorOf(Props.create(LibraryActor.class), "libraryWorker");
    }
}
