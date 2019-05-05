package sr;

import static io.grpc.MethodDescriptor.generateFullMethodName;
import static io.grpc.stub.ClientCalls.asyncBidiStreamingCall;
import static io.grpc.stub.ClientCalls.asyncClientStreamingCall;
import static io.grpc.stub.ClientCalls.asyncServerStreamingCall;
import static io.grpc.stub.ClientCalls.asyncUnaryCall;
import static io.grpc.stub.ClientCalls.blockingServerStreamingCall;
import static io.grpc.stub.ClientCalls.blockingUnaryCall;
import static io.grpc.stub.ClientCalls.futureUnaryCall;
import static io.grpc.stub.ServerCalls.asyncBidiStreamingCall;
import static io.grpc.stub.ServerCalls.asyncClientStreamingCall;
import static io.grpc.stub.ServerCalls.asyncServerStreamingCall;
import static io.grpc.stub.ServerCalls.asyncUnaryCall;
import static io.grpc.stub.ServerCalls.asyncUnimplementedStreamingCall;
import static io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall;

/**
 */
@javax.annotation.Generated(
    value = "by gRPC proto compiler (version 1.20.0)",
    comments = "Source: exchange.proto")
public final class ExchangeGrpc {

  private ExchangeGrpc() {}

  public static final String SERVICE_NAME = "Exchange";

  // Static method descriptors that strictly reflect the proto.
  private static volatile io.grpc.MethodDescriptor<sr.ExchangeClass.ExchangeRequest,
      sr.ExchangeClass.ExchangeStream> getSubscribeForExchangeMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "subscribeForExchange",
      requestType = sr.ExchangeClass.ExchangeRequest.class,
      responseType = sr.ExchangeClass.ExchangeStream.class,
      methodType = io.grpc.MethodDescriptor.MethodType.SERVER_STREAMING)
  public static io.grpc.MethodDescriptor<sr.ExchangeClass.ExchangeRequest,
      sr.ExchangeClass.ExchangeStream> getSubscribeForExchangeMethod() {
    io.grpc.MethodDescriptor<sr.ExchangeClass.ExchangeRequest, sr.ExchangeClass.ExchangeStream> getSubscribeForExchangeMethod;
    if ((getSubscribeForExchangeMethod = ExchangeGrpc.getSubscribeForExchangeMethod) == null) {
      synchronized (ExchangeGrpc.class) {
        if ((getSubscribeForExchangeMethod = ExchangeGrpc.getSubscribeForExchangeMethod) == null) {
          ExchangeGrpc.getSubscribeForExchangeMethod = getSubscribeForExchangeMethod = 
              io.grpc.MethodDescriptor.<sr.ExchangeClass.ExchangeRequest, sr.ExchangeClass.ExchangeStream>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.SERVER_STREAMING)
              .setFullMethodName(generateFullMethodName(
                  "Exchange", "subscribeForExchange"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  sr.ExchangeClass.ExchangeRequest.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  sr.ExchangeClass.ExchangeStream.getDefaultInstance()))
                  .setSchemaDescriptor(new ExchangeMethodDescriptorSupplier("subscribeForExchange"))
                  .build();
          }
        }
     }
     return getSubscribeForExchangeMethod;
  }

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static ExchangeStub newStub(io.grpc.Channel channel) {
    return new ExchangeStub(channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static ExchangeBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    return new ExchangeBlockingStub(channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static ExchangeFutureStub newFutureStub(
      io.grpc.Channel channel) {
    return new ExchangeFutureStub(channel);
  }

  /**
   */
  public static abstract class ExchangeImplBase implements io.grpc.BindableService {

    /**
     */
    public void subscribeForExchange(sr.ExchangeClass.ExchangeRequest request,
        io.grpc.stub.StreamObserver<sr.ExchangeClass.ExchangeStream> responseObserver) {
      asyncUnimplementedUnaryCall(getSubscribeForExchangeMethod(), responseObserver);
    }

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor())
          .addMethod(
            getSubscribeForExchangeMethod(),
            asyncServerStreamingCall(
              new MethodHandlers<
                sr.ExchangeClass.ExchangeRequest,
                sr.ExchangeClass.ExchangeStream>(
                  this, METHODID_SUBSCRIBE_FOR_EXCHANGE)))
          .build();
    }
  }

  /**
   */
  public static final class ExchangeStub extends io.grpc.stub.AbstractStub<ExchangeStub> {
    private ExchangeStub(io.grpc.Channel channel) {
      super(channel);
    }

    private ExchangeStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected ExchangeStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new ExchangeStub(channel, callOptions);
    }

    /**
     */
    public void subscribeForExchange(sr.ExchangeClass.ExchangeRequest request,
        io.grpc.stub.StreamObserver<sr.ExchangeClass.ExchangeStream> responseObserver) {
      asyncServerStreamingCall(
          getChannel().newCall(getSubscribeForExchangeMethod(), getCallOptions()), request, responseObserver);
    }
  }

  /**
   */
  public static final class ExchangeBlockingStub extends io.grpc.stub.AbstractStub<ExchangeBlockingStub> {
    private ExchangeBlockingStub(io.grpc.Channel channel) {
      super(channel);
    }

    private ExchangeBlockingStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected ExchangeBlockingStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new ExchangeBlockingStub(channel, callOptions);
    }

    /**
     */
    public java.util.Iterator<sr.ExchangeClass.ExchangeStream> subscribeForExchange(
        sr.ExchangeClass.ExchangeRequest request) {
      return blockingServerStreamingCall(
          getChannel(), getSubscribeForExchangeMethod(), getCallOptions(), request);
    }
  }

  /**
   */
  public static final class ExchangeFutureStub extends io.grpc.stub.AbstractStub<ExchangeFutureStub> {
    private ExchangeFutureStub(io.grpc.Channel channel) {
      super(channel);
    }

    private ExchangeFutureStub(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected ExchangeFutureStub build(io.grpc.Channel channel,
        io.grpc.CallOptions callOptions) {
      return new ExchangeFutureStub(channel, callOptions);
    }
  }

  private static final int METHODID_SUBSCRIBE_FOR_EXCHANGE = 0;

  private static final class MethodHandlers<Req, Resp> implements
      io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {
    private final ExchangeImplBase serviceImpl;
    private final int methodId;

    MethodHandlers(ExchangeImplBase serviceImpl, int methodId) {
      this.serviceImpl = serviceImpl;
      this.methodId = methodId;
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        case METHODID_SUBSCRIBE_FOR_EXCHANGE:
          serviceImpl.subscribeForExchange((sr.ExchangeClass.ExchangeRequest) request,
              (io.grpc.stub.StreamObserver<sr.ExchangeClass.ExchangeStream>) responseObserver);
          break;
        default:
          throw new AssertionError();
      }
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public io.grpc.stub.StreamObserver<Req> invoke(
        io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        default:
          throw new AssertionError();
      }
    }
  }

  private static abstract class ExchangeBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    ExchangeBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return sr.ExchangeClass.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("Exchange");
    }
  }

  private static final class ExchangeFileDescriptorSupplier
      extends ExchangeBaseDescriptorSupplier {
    ExchangeFileDescriptorSupplier() {}
  }

  private static final class ExchangeMethodDescriptorSupplier
      extends ExchangeBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final String methodName;

    ExchangeMethodDescriptorSupplier(String methodName) {
      this.methodName = methodName;
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.MethodDescriptor getMethodDescriptor() {
      return getServiceDescriptor().findMethodByName(methodName);
    }
  }

  private static volatile io.grpc.ServiceDescriptor serviceDescriptor;

  public static io.grpc.ServiceDescriptor getServiceDescriptor() {
    io.grpc.ServiceDescriptor result = serviceDescriptor;
    if (result == null) {
      synchronized (ExchangeGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new ExchangeFileDescriptorSupplier())
              .addMethod(getSubscribeForExchangeMethod())
              .build();
        }
      }
    }
    return result;
  }
}
