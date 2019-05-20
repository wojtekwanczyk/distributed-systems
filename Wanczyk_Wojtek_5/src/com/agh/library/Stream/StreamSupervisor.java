package com.agh.library.Stream;

import akka.actor.AbstractActor;
import akka.actor.ActorRef;
import akka.event.Logging;
import akka.event.LoggingAdapter;
import com.agh.helpers.other.Response;
import com.agh.helpers.titles.TitleActor;

import java.io.File;

public class StreamSupervisor extends AbstractActor {
    private final LoggingAdapter log = Logging.getLogger(getContext().getSystem(), this);
    private String books = "data/books";
    private ActorRef client;
    private File[] fileList;
    private File file = null;

    @Override
    public Receive createReceive() {
        return receiveBuilder()
                .match(TitleActor.class, request -> {
                    client = request.actor;
                    fileList = getFileList(books);

                    // search for file
                    for(File f : fileList){
                        if(f.toString().contains(request.title)){
                            System.out.println("Found file to stream: " + f.toString());
                            file = f;
                            break;
                        }
                    }

                    //stream file
                    if(file != null){
                        client.tell(Response.SUCCESS, getSelf());
                    } else {
                        System.out.println("File " + request.title + " not found.");
                        client.tell(Response.NOT_FOUND, getSelf());
                    }
                })
                .matchAny(o -> log.info("received unknown message"))
                .build();
    }

    private File[] getFileList(String directory_name){
        File directory = new File(directory_name);
        return directory.listFiles();
    }

}
