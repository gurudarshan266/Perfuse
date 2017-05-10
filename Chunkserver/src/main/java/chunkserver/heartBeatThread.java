package chunkserver;

import chunkserver.DefinesProto.MethodType;
import chunkserver.RequestProto.Request;

public class heartBeatThread implements Runnable {

	private String host;
	public heartBeatThread(String ip) {
		this.setHost(ip);
	}
	@Override
	public void run() {
		// TODO Auto-generated method stub
		Request req = Request.newBuilder().setMethod(MethodType.NOP).setReqid(0).build();
		ChunkGrpcClient rpcclient = new ChunkGrpcClient(this.getHost(), 50004);
		while (true) {
			rpcclient.heartBeat(req);
		}
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
