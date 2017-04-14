package chunkserver;

import io.grpc.Server;
import io.grpc.ServerBuilder;
import io.grpc.stub.StreamObserver;
import java.io.IOException;
import java.util.logging.Logger;

import chunkserver.DefinesProto.MethodType;
import chunkserver.RequestProto.Request;
import chunkserver.ResponseProto.Response;

public class ChunkGrpcServer {
	private static final Logger logger = Logger.getLogger(ChunkGrpcServer.class.getName());

	private Server server;
	private final int port = 50051;
	
	/** Start serving requests. */
	  public void start() throws IOException {
		server = ServerBuilder.forPort(port)
			        .addService(new ChunkServerImpl())
			        .build()
			        .start();
	    logger.info("Server started, listening on " + port);
	    Runtime.getRuntime().addShutdownHook(new Thread() {
	      @Override
	      public void run() {
	        // Use stderr here since the logger may has been reset by its JVM shutdown hook.
	        System.err.println("*** shutting down gRPC server since JVM is shutting down");
	        ChunkGrpcServer.this.stop();
	        System.err.println("*** server shut down");
	      }
	    });
	}
	
	  /** Stop serving requests and shutdown resources. */
	  public void stop() {
	    if (server != null) {
	      server.shutdown();
	    }
	}
	  
	  /**
	   * Await termination on the main thread since the grpc library uses daemon threads.
	   */
	  private void blockUntilShutdown() throws InterruptedException {
	    if (server != null) {
	      server.awaitTermination();
	    }
	  }
	  
	  /**
	   * Main launches the server from the command line.
	   */
	  public static void main(String[] args) throws IOException, InterruptedException {
	    final ChunkGrpcServer server = new ChunkGrpcServer();
	    server.start();
	    server.blockUntilShutdown();
	  }
	  
	  static class ChunkServerImpl extends ChunkServerGrpc.ChunkServerImplBase {
		  
		  public void getResponse(Request request, StreamObserver<Response> responseObserver) {
			  MethodType mt = request.getMethod();
			  System.out.println("Received message " + mt.name());
			  int reqid = request.getReqid();
			  String filename = request.getFilename();
			  String chash = request.getHash();
			  String data = request.getData();
			  
			  Response response = Response.newBuilder().setRespid(reqid).setMethod(mt).build();

			  
			  switch (mt) {
			  case GETFILEINFO:
				  /* Given a filename, retrieve metadata from the database
				   */
				  break;
			  case GETCHUNKDATA:
				  /* Given the filename and hash, send a request to storage server having the data
				   * Send error code, if any
				   */
				  break;
			  case GETHASHES:
				  /*
				   * Given a filename, check if its a file
				   * Retrieve all hashes of the file
				   * Fill in chunkinfo struct
				   * Fill in response object
				   */
				  break;
			  case WRITECHUNK:
				  break;
			  case VIVALDIUPDATE:
				  break;
			  case GETDIRLIST:
				  /*
				   * Given a path name check if its a directory
				   * If it is directory retrieve all its immediate children
				   * Fill in fileinfo struct
				   * Fill in response object
				   * Set error code, if any
				   */
				  break;
			  case NOP:
				  break;
			  }
				  
			  responseObserver.onNext(response);
			  responseObserver.onCompleted();
		  }
		  
	  }
}