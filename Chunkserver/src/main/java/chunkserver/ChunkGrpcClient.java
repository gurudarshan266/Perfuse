package chunkserver;

import com.google.common.annotations.VisibleForTesting;
import com.google.protobuf.Message;

import chunkserver.DefinesProto.Delay;
import chunkserver.DefinesProto.NodeInfo;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
//import io.grpc.Status;
//import io.grpc.StatusRuntimeException;
//import io.grpc.stub.StreamObserver;
//import java.io.IOException;
//import java.util.Iterator;
//import java.util.List;
//import java.util.Random;
//import java.util.concurrent.CountDownLatch;
//import java.util.concurrent.TimeUnit;
//import java.util.logging.Level;
import java.util.logging.Logger;

import storageserver.StorageServerGrpc.*;

public class ChunkGrpcClient {
	
	private static final Logger logger = Logger.getLogger(ChunkGrpcClient.class.getName());

	  private final ManagedChannel channel;
	  private final StorageServerBlockingStub blockingStub;
	  private String host;
	  //private final StorageServerStub asyncStub;

	  public ChunkGrpcClient(String host, int port) {
		  this(ManagedChannelBuilder.forAddress(host, port).usePlaintext(true));
		  this.setHost(host);
	  }
	  
	  public ChunkGrpcClient(ManagedChannelBuilder<?> channelBuilder ){
		  channel = channelBuilder.build();
		  blockingStub = storageserver.StorageServerGrpc.newBlockingStub(channel);
		  //asyncStub = storageserver.StorageServerGrpc.newStub(channel);
	  }
	  
	  public Delay pingClient(NodeInfo nodeinfo) {
		  logger.info("Ping Src: " + getHost() + " Dst: " + nodeinfo.getIp());
		  Delay delay = blockingStub.pingClient(nodeinfo);
		  return delay;
	  }
	
	  public static void main(String[] args) {
		// TODO Auto-generated method stub

	}

	public String getHost() {
		return host;
	}

	public void setHost(String host) {
		this.host = host;
	}

}
