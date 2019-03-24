package distributedmap;


import org.jgroups.*;
import org.jgroups.protocols.*;
import org.jgroups.protocols.pbcast.GMS;
import org.jgroups.protocols.pbcast.NAKACK2;
import org.jgroups.protocols.pbcast.STABLE;
import org.jgroups.protocols.pbcast.STATE_TRANSFER;
import org.jgroups.stack.ProtocolStack;
import org.jgroups.util.Util;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.UnknownHostException;
import java.util.HashMap;
import java.util.List;

public class DistributedMap extends ReceiverAdapter implements SimpleStringClass {
    private JChannel channel;
    final private HashMap<String, Integer> map = new HashMap<>();

    public void start(String name, String cluster) throws UnknownHostException {
        channel = new JChannel(false);
        channel.setName(name);
        channel.setReceiver(this);

        ProtocolStack stack = new ProtocolStack();

        channel.setProtocolStack(stack);
        stack.addProtocol(new UDP())
//        stack.addProtocol(new UDP().setValue("mcast_group_addr",InetAddress.getByName("230.100.200.100")))
                .addProtocol(new PING())
                .addProtocol(new MERGE3())
                .addProtocol(new FD_SOCK())
                .addProtocol(new FD_ALL().setValue("timeout", 12000).setValue("interval", 3000))
                .addProtocol(new VERIFY_SUSPECT())
                .addProtocol(new BARRIER())
                .addProtocol(new NAKACK2())
                .addProtocol(new UNICAST3())
                .addProtocol(new STABLE())
                .addProtocol(new GMS())
                .addProtocol(new UFC())
                .addProtocol(new MFC())
                .addProtocol(new FRAG2())
                .addProtocol(new STATE_TRANSFER());

        try {
            stack.init();
            channel.connect(cluster);
            channel.getState(null, 10000);
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    public void stop() {
        channel.close();
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

    public void viewAccepted(View view) {
        System.out.println("*** group info ***\n\t" + view);

        if(view instanceof MergeView) {
            MergeViewHandler handler = new MergeViewHandler(channel, (MergeView)view);
            handler.start();
        }
    }

    private static class MergeViewHandler extends Thread {
        JChannel channel;
        MergeView view;

        private MergeViewHandler(JChannel channel, MergeView view) {
            this.channel = channel;
            this.view = view;
        }

        public void run() {
            List<View> subgroups = view.getSubgroups();
            View tmp_view = subgroups.get(0); // picks the first
            Address local_addr = channel.getAddress();

            if (tmp_view.getMembers().contains(local_addr)) {
                System.out.println("Member of the new primary partition ("
                        + tmp_view + "), will do nothing");
            } else {
                System.out.println("Not member of the new primary partition ("
                        + tmp_view + "), will re-acquire the state");
                try {
                    channel.getState(null, 10000);
                } catch (Exception ex) {
                    ex.printStackTrace();
                }
            }
        }
    }
}
