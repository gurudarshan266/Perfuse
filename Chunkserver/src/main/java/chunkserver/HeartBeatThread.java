package chunkserver;

import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.logging.Logger;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;

import chunkserver.DefinesProto.MethodType;
import chunkserver.RequestProto.Request;

public class HeartBeatThread implements Runnable {
	private static final Logger logger = Logger.getLogger(HeartBeatThread.class.getName());
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
			logger.info("HEART BEAT MONITORING STARTED FOR " + getHost());
			boolean flag = true;
			while (flag) {
				try {
					Thread.sleep(1000);
					rpcclient.heartBeat(req);
				} catch (Exception e) {
					logger.warning(e.getMessage() + ": Node "+ getHost() + " has died");
					flag = false;
					deleteDelayEntries();
					deleteNodeEntries();
				}
			}
		}
	
	private void deleteNodeEntries() {
		DbUtil db = new DbUtil();
		db.deleteNodeEntries(this.getHost());
	}
	private void deleteDelayEntries() {
		DbUtil db = new DbUtil();
	    
	    db.deleteDelayEntries(this.getHost());
		
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
