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
			try {
				Thread.sleep(100);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			ChunkGrpcClient rpcclient = new ChunkGrpcClient(this.getHost(), 50004);
			System.out.println("HEART BEAT MONITORING STARTED FOR " + getHost());
			boolean flag = true;
			while (flag) {
				try {
					Thread.sleep(1000);
					rpcclient.heartBeat(req);
				} catch (Exception e) {
					System.err.println(e.getMessage() + ":Node "+ getHost() + " has died");
					flag = false;
				}
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
