package com.agh.library.Stream;

import akka.NotUsed;
import akka.actor.AbstractActor;
import akka.actor.ActorRef;
import akka.event.Logging;
import akka.event.LoggingAdapter;
import akka.stream.ActorMaterializer;
import akka.stream.OverflowStrategy;
import akka.stream.ThrottleMode;
import akka.stream.javadsl.Sink;
import akka.stream.javadsl.Source;
import com.agh.helpers.other.Response;
import com.agh.helpers.titles.TitleActor;
import scala.concurrent.duration.FiniteDuration;

import java.io.File;
import java.nio.file.Files;
import java.util.concurrent.TimeUnit;
import java.util.stream.Stream;

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
                    if(file != null) try {
                        System.out.println("Streaming " + file.toString());
                        ActorMaterializer mat = ActorMaterializer.create(getContext());
                        ActorRef run = Source.actorRef(1000, OverflowStrategy.dropNew())
                                .throttle(1, FiniteDuration.create(1, TimeUnit.SECONDS), 1, ThrottleMode.shaping())
                                .to(Sink.actorRef(client, NotUsed.getInstance()))
                                .run(mat);

                        Stream<String> lines = Files.lines(file.toPath());
                        lines.forEachOrdered(
                                line -> run.tell(line, getSelf()));
                    } catch (Exception e) {
                        System.out.println(e.toString());
                        client.tell(Response.STREAM_ERROR, getSelf());
                    }
                    else {
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
