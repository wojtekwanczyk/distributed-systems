package exchange;

import sr.ExchangeClass;
import sr.ExchangeClass.ExchangeRequest;
import sr.ExchangeClass.Currency;
import sr.ExchangeClass.ExchangeStream;
import sr.ExchangeGrpc.ExchangeImplBase;

import java.util.HashMap;
import java.util.List;
import java.util.Random;
import io.grpc.stub.StreamObserver;


public class ExchangeImpl extends ExchangeImplBase {

    private HashMap<Currency, Double> rates;
    private Random rand;


    ExchangeImpl(){
        rates = new HashMap<>();
        rand = new Random();
        for(Currency currency : Currency.values()){
            double rate = rand.nextDouble() * 5 + 0.01; // double from 0.01 to 5.01
            rates.put(currency, rate);
        }
    }

    @Override
    public void subscribeForExchange(ExchangeRequest request,
                                     StreamObserver<ExchangeStream> responseObserver) {
        Currency mainCurrency = request.getMainCurrency();
        List<Currency> extraCurrencyList = request.getExtraCurrencyList();
        extraCurrencyList.remove(mainCurrency);
        int waitTime = 1000;


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
                for(Currency currency : rates.keySet()){
                    double rate = rates.get(currency);
                    rate += rand.nextDouble() / 5 - 0.2; // delta (-0.2, 0.2)
                    rates.put(currency, rate);
                }
                Thread.sleep(waitTime);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

    }
}
