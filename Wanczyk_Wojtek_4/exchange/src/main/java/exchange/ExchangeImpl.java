package exchange;

import sr.ExchangeClass.ExchangeRequest;
import sr.ExchangeClass.Currency;
import sr.ExchangeClass.ExchangeStream;
import sr.ExchangeGrpc.ExchangeImplBase;

import java.util.HashMap;
import java.util.List;
import java.util.Random;
import io.grpc.stub.StreamObserver;

import static java.lang.Math.abs;


public class ExchangeImpl extends ExchangeImplBase {

    private HashMap<Currency, Double> rates;
    private Random rand;

    private double cut(double a){
        int temp = (int)(a*100.0);
        double rate = ((double)temp)/100.0;
        return abs(rate);
    }


    ExchangeImpl(){
        rates = new HashMap<>();
        rand = new Random();
        for(Currency currency : Currency.values()){
            double rate = rand.nextDouble() * 4.5 + 0.5; // double from 0.5 to 5.01
            rate = cut(rate);
            rates.put(currency, rate);
        }
    }

    @Override
    public void subscribeForExchange(ExchangeRequest request,
                                     StreamObserver<ExchangeStream> responseObserver) {
        Currency mainCurrency = request.getMainCurrency();
        List<Currency> extraCurrencyList = request.getExtraCurrencyList();
        extraCurrencyList.remove(mainCurrency);
        int waitTime = 4000;


        while(true) {

            // send updates
            for(Currency currency : extraCurrencyList) {
                double rate = rates.get(currency);
                ExchangeStream eStream = ExchangeStream
                        .newBuilder()
                        .setCurrency(currency)
                        .setExchangeRate(rate)
                        .build();
                responseObserver.onNext(eStream);
            }

            // change values and wait
            try {
                Thread.sleep(waitTime);
                for(Currency currency : rates.keySet()){
                    double rate = rates.get(currency);
                    rate += rand.nextDouble() / 5 - 0.05; // delta (-0.05, 0.15)
                    rate = cut(rate);
                    rates.put(currency, rate);
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

    }
}
