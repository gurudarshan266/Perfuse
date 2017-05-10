package chunkserver;

import io.grpc.Server;
import io.grpc.ServerBuilder;
import io.grpc.stub.StreamObserver;
import java.io.IOException;
import java.util.ArrayList;
import java.util.logging.Logger;

import chunkserver.DefinesProto.ChunkInfo;
import chunkserver.DefinesProto.Delay;
import chunkserver.DefinesProto.Error;
import chunkserver.DefinesProto.FileInfo;
import chunkserver.DefinesProto.MethodType;
import chunkserver.DefinesProto.NodeInfo;
import chunkserver.RequestProto.Request;
import chunkserver.ResponseProto.Response;
import chunkserver.ResponseProto.Response.Builder;

public class ChunkGrpcServer {
	private static final Logger logger = Logger.getLogger(ChunkGrpcServer.class.getName());

	private Server server;
	private final int port = 50051;

	/** Start serving requests. */
	public void start() throws IOException {
		server = ServerBuilder.forPort(port).addService(new ChunkServerImpl()).build().start();
		logger.info("Server started, listening on " + port);
		Runtime.getRuntime().addShutdownHook(new Thread() {
			@Override
			public void run() {
				// Use stderr here since the logger may has been reset by its
				// JVM shutdown hook.
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
	 * Await termination on the main thread since the grpc library uses daemon
	 * threads.
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

	private static class ChunkServerImpl extends ChunkServerGrpc.ChunkServerImplBase {
		
		@Override
		public StreamObserver<ChunkInfo> routeUpdate(final StreamObserver<Error> responseObserver) {
			return new StreamObserver<ChunkInfo>() {

				int ec = 0;
//				System.out.println("Received route update message");
				@Override
				public void onNext(ChunkInfo chunk) {
					DbUtil db = new DbUtil();
					db.addChunks(chunk);
					/*
					 * TODO: Currently the error code is always set to 0: Fix
					 * this
					 */
				}
				@Override
				public void onError(Throwable t) {
					System.err.println(t.getMessage());
				}
				@Override
				public void onCompleted() {
					responseObserver.onNext(Error.newBuilder().setEc(-5).build());
					responseObserver.onCompleted();
				}

			};
		}
		
		public void getResponse(Request request, StreamObserver<Response> responseObserver) {

			MethodType mt = request.getMethod();
			int reqid = request.getReqid();
			System.out.println("Received message: " + mt.name() + " Req ID: " + reqid);
			Builder builder = Response.newBuilder().setRespid(reqid).setMethod(mt);
			DbUtil db = new DbUtil();

			String sip = request.getClientIp();

			Response response = null;

			switch (mt) {
			case GETFILEINFO:
				/*
				 * Given a filename, retrieve metadata from the database
				 */
				FileInfo fi = db.getFileInfo(request.getFilename());
				if (fi == null) {
					response = builder.setEc(-2).build();
				} else {
					response = builder.setEc(0).addFilesinfo(fi).build();
				}
				break;
			case GETCHUNKDATA:
				/*
				 * Given the filename and hash, send a request to storage server
				 * having the data Send error code, if any
				 */
				break;
			case GETHASHES:
				/*
				 * Given a filename, check if its a file Retrieve all hashes of
				 * the file Fill in chunkinfo struct Fill in response object.
				 * Check if the corresponding file information is present in DB
				 */
				//boolean present = 
				ArrayList<ChunkInfo> hashes = db.getChunks(request.getFilename());
				if (hashes.size() == 0) {
					builder.setEc(-1).build();
				} else {
					for (int i = 0; i < hashes.size(); i++) {
						builder.addChunksinfo(hashes.get(i));
					}
					response = builder.setEc(0).build();
				}

				break;
			case WRITECHUNK:
				/*
				 * Given a filename, parent and size, retrieve the closest
				 * storage server
				 */
				ArrayList<NodeInfo> seeders = db.getStorageNodes(sip);
				if (seeders.isEmpty()) {
					response = builder.setEc(-2).build();
				} else {
					response = builder.setEc(0).addAllSeeders(seeders).build();
				}

				break;
			case VIVALDIUPDATE:
				break;
			case GETDIRLIST:
				/*
				 * Given a path name check if its a directory If it is directory
				 * retrieve all its immediate children Fill in fileinfo struct
				 * Fill in response object Set error code, if any
				 */
				ArrayList<String> dirlist = db.getSubDirNames(request.getFilename());
				for (int i = 0; i < dirlist.size(); i++) {
					builder.addFilesinfo(db.getFileInfo(dirlist.get(i)));
				}
				response = builder.setEc(0).build();
				break;
			case UPDATEFILEINFO:
				/*
				 * Add or Update file info in the FILEINFO Table
				 */
				int rc = db.updateFileInfo(request);
				response=builder.setEc(rc).build();
			case NOP:
				break;
				
			case REMOVEFILE:
				/*
				 * Called for rmdir or rm operations
				 */
				boolean is_dir = request.getFileinfo().getIsDir();
				if (is_dir) {
					rc = db.removeDir(request);
				} else {
					rc = db.removeFile(request);
				}
				response=builder.setEc(rc).build();
				break;
			case ADDDIR:
				/*
				 * Mkdir
				 */
				rc = db.addDir(request);
				break;
			case NEWNODE:
				/*
				 * New client or server is added
				 * Fetch a max of three nodes from NODEINFO list
				 * Get Client objects for each node and pass the new node info to them
				 * Update Vivaldi information
				 */
				Delay delay = null;
				ArrayList<NodeInfo> nodelist = db.getRandomNodes();
				NodeInfo newnode = NodeInfo.newBuilder().setIp(sip).build();
				if (db.isNodePresent(newnode)) {
					response = builder.setEc(0).build(); /*Ideally should throw error*/
					break;
				}
				boolean is_client = request.getIsClient();
				if (nodelist.isEmpty()) {
					if (is_client) {
						response = builder.setEc(-1).build();
					} else {
						db.addNodeInfo(newnode);
						response = builder.setEc(0).build();
					}
					break;
				}
				for (NodeInfo node : nodelist) {
					String ip = node.getIp();
					Vivaldi.getInstance().addNode(ip);
				
					ChunkGrpcClient rpcclient = new ChunkGrpcClient(ip, 50004);
					delay = rpcclient.pingClient(newnode);
					db.updateDelayTable(sip, ip, delay);
					
					Vivaldi.getInstance().setDistance(sip,ip,delay.getDl());
					if (!is_client) {
						db.addNodeInfo(newnode);
					}
				}
				response = builder.setEc(0).build();
				break;
			default:
				System.out.println("Invalid message type");
				break;
			}
			responseObserver.onNext(response);
			responseObserver.onCompleted();
		}

	}
}
