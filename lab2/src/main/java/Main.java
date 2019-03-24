import distributedmap.*;

public class Main {
    public static void main(String[] args) {
        System.out.println(args[0]);
        DistributedMap myMap = new DistributedMap();

        myMap.start(args[0], "HashMapCluster", "");

    }
}
