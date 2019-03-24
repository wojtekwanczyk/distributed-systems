package distributedmap;


import org.jgroups.*;
import org.jgroups.util.Util;

import java.io.*;
import java.util.HashMap;

public class DistributedMap extends ReceiverAdapter implements SimpleStringClass {
    private JChannel channel;
    final private HashMap<String, Integer> map = new HashMap<>();

    public void start(String name, String cluster, String properties) {
        try {
            if(properties.isEmpty()){
                channel = new JChannel();
            } else {
                channel = new JChannel(properties);
            }
            channel.setName(name);
            channel.setReceiver(this);
            channel.connect(cluster);
            channel.getState(null, 10000);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void stop() {
        channel.close();
    }

    public void viewAccepted(View view) {
        System.out.println("*** group info ***\n\t" + view);
    }

    public void receive(Message msg) {
        String content = msg.getObject().toString();
        Address source = msg.getSrc();
        System.out.printf("*** received message ***\n\t %s: %s\n", source, content);

        String[] contentArray = content.split(" ");
        String action = contentArray[0];
        String key = contentArray[1];

        if(!source.equals(channel.getAddress())){
            switch (action) {
                case "put":
                    Integer value = Integer.valueOf(contentArray[2]);
                    map.put(key, value);
                    break;
                case "remove":
                    map.remove(key);
                    break;
            }
        }
    }

    public void getState(OutputStream output) throws Exception {
        synchronized(map) {
            Util.objectToStream(map, new DataOutputStream(output));
        }
    }

    @SuppressWarnings("unchecked")
    public void setState(InputStream input) throws Exception {
        HashMap<String, Integer> receivedMap;
        receivedMap = (HashMap<String, Integer>) Util.objectFromStream(new DataInputStream(input));

        synchronized (map) {
            map.clear();
            map.putAll(receivedMap);
        }

        System.out.println("*** received map state ***");
        show();
    }


    @Override
    public boolean containsKey(String key) {
        return map.containsKey(key);
    }

    @Override
    public Integer get(String key) {
        return map.get(key);
    }

    @Override
    public void put(String key, Integer value) {
        try {
            channel.send(new Message(null, "put" + " " + key + " " + value));
        } catch (Exception e) {
            e.printStackTrace();
            return;
        }
        map.put(key, value);
    }

    @Override
    public Integer remove(String key) {
        try {
            channel.send(new Message(null, "remove" + " " + key));
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
        return map.remove(key);
    }

    public void show() {
        if(map.isEmpty()){
            System.out.println("Map is empty");
        }
        map.entrySet().forEach(System.out::println);
    }
}
