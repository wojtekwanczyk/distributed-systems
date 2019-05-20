package com.agh.helpers;

import java.io.Serializable;

public class TitleDatabase extends Title implements Serializable {
    public String database;

    public TitleDatabase(String title, String database) {
        super(title);
        this.database = database;
    }
}