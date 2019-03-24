import distributedmap.DistributedMap;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) {
        System.out.println(args[0]);
        DistributedMap myMap = new DistributedMap();

        myMap.start(args[0], "HashMapCluster", "");
        operate(myMap);
        myMap.stop();
    }

    private static void operate(DistributedMap map) {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        while (true) {
            String content = null;
            try {
                content = in.readLine();
            } catch (IOException e) {
                e.printStackTrace();
            }

            if (content.equals("end")) {
                    break;
            }

            String[] contentArray = content.split(" ");
            String action = contentArray[0];
            String key;

            switch (action) {
                case "c":
                    if(checkInput(contentArray, 2)) {
                        key = contentArray[1];
                        System.out.println(map.containsKey(key));
                    }
                    break;
                case "g":
                    if(checkInput(contentArray, 2)) {
                        key = contentArray[1];
                        System.out.println(map.get(key));
                    }
                    break;
                case "r":
                    if(checkInput(contentArray, 2)) {
                        key = contentArray[1];
                        System.out.println(map.remove(key));
                    }
                    break;
                case "p":
                    if(checkInput(contentArray, 3)){
                        key = contentArray[1];
                        Integer value = 0;
                        try {
                            value = Integer.parseInt(contentArray[2]);
                        } catch(NumberFormatException e) {
                            System.out.println("Second argument must be number");
                            break;
                        }
                        map.put(key, value);
                    }
                    break;
                case "s":
                    if(checkInput(contentArray, 1)) {
                        map.show();
                    }
                    break;
            }
        }
    }

    public static boolean checkInput(String[] array, int len) {
        if(array.length != len) {
            System.out.println("Wrong input");
            return false;
        }
        return true;
    }
}
