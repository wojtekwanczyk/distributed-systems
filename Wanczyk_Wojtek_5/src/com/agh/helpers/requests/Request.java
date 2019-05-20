package com.agh.helpers.requests;

import java.io.Serializable;

public class Request implements Serializable {
    public final String title;

    public Request(String title){
        this.title = title;
    }
}
