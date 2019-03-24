package distributedmap;


import org.jgroups.JChannel;
import org.jgroups.Message;
import org.jgroups.ReceiverAdapter;
import org.jgroups.View;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class DistributedMap extends ReceiverAdapter implements SimpleStringClass {
    private JChannel channel;

    @Override
    public boolean containsKey(String key) {
        return false;
    }

    @Override
    public Integer get(String key) {
        return null;
    }

    @Override
    public void put(String key, Integer value) {

    }

    @Override
    public Integer remove(String key) {
        return null;
    }

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
            //channel.getState(null, 10000);
        } catch (Exception e) {
            e.printStackTrace();
        }
        eventLoop();
        channel.close();
    }

    private void eventLoop() {
        BufferedReader input = new BufferedReader(new InputStreamReader(System.in));
        String text = "";
        while(!text.equals("end")) {
            try {
                text = input.readLine();
                Message msg = new Message(null, text);
                channel.send(msg);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

    }

    public void viewAccepted(View new_view) {
        System.out.println("** view: " + new_view);
    }

    public void receive(Message msg) {
        System.out.printf("from %s: %s\n", msg.getSrc(), msg.getObject());
    }
}
