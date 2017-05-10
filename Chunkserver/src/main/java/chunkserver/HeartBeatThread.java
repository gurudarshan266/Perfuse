package chunkserver;

import chunkserver.DefinesProto.MethodType;
import chunkserver.RequestProto.Request;

public class HeartBeatThread implements Runnable {

	private String host;
	public HeartBeatThread(String ip) {
		this.setHost(ip);
	}
	@Override
	public void run() {
		// TODO Auto-generated method stub
		Request req = Request.newBuilder().setMethod(MethodType.NOP).setReqid(0).build();
		ChunkGrpcClient rpcclient = new ChunkGrpcClient(this.getHost(), 50004);
		//while (true) {
			try {
				rpcclient.heartBeat(req);
			} catch (Exception e) {
				e.printStackTrace();
			}
		//}
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
