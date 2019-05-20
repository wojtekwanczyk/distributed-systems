package com.agh.helpers;

import akka.actor.ActorRef;
import java.io.Serializable;

public class TitleActor extends Title implements Serializable {
    public ActorRef actor;

    public TitleActor(String title, ActorRef actor) {
        super(title);
        this.actor = actor;
    }
}
