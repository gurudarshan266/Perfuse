package chunkserver;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.sql.Timestamp;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.logging.Logger;

import chunkserver.DefinesProto.ChunkInfo;
import chunkserver.DefinesProto.Delay;
import chunkserver.DefinesProto.FileInfo;
import chunkserver.DefinesProto.FileInfo.Builder;
import chunkserver.DefinesProto.NodeInfo;
import chunkserver.RequestProto.Request;

/* This class has methods to create/modify/delete db tables*/
public class DbUtil {
	private static final Logger logger = Logger.getLogger(ChunkGrpcServer.class.getName());
	private static final DateFormat sdf = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
	private Connection connect = DbConnection.getInstance();

	// public Connection getConnection(String username, String password) {
	// if (connect != null)
	// return connect;
	// try {
	// Class.forName("com.mysql.jdbc.Driver");
	// connect = DriverManager
	// .getConnection("jdbc:mysql://localhost/feedback?" + "user=" + username +
	// "&password=" + password);
	// } catch (ClassNotFoundException e) {
	// // TODO Auto-generated catch block
	// e.printStackTrace();
	// } catch (SQLException e) {
	// // TODO Auto-generated catch block
	// e.printStackTrace();
	// }
	// return connect;
	// }

	public void createChunkTable() {
		String query;
		query = "CREATE TABLE CHUNKS (" + "ID INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,"
				+ "HASH VARCHAR(40) NOT NULL," + "FILENAME VARCHAR(255) NOT NULL," + "OFFSET INT NOT NULL,"
				+ "LEN INT NOT NULL," + "SEEDERS VARCHAR(1024) NOT NULL);";
		try {
			Statement statement = connect.createStatement();
			statement.executeUpdate(query);
			logger.info(query);
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			// close();
			e.printStackTrace();
		}

	}

	public void createFileTable() {
		String query;
		query = "CREATE TABLE FILEINFO (" + "ID INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,"
				+ "FILENAME VARCHAR(255) NOT NULL," + "SIZE INT NOT NULL," + "LAST_MODIFIED TIMESTAMP NOT NULL,"
				+ "DIRECTORY TINYINT NOT NULL," + "PARENT VARCHAR(255) NOT NULL);";
		try {
			Statement statement = connect.createStatement();
			statement.executeUpdate(query);
			logger.info(query);
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			// close();
			e.printStackTrace();
		}
	}

	public void createNodeTable() {
		String query;
		query = "CREATE TABLE NODEINFO (" + "ID INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,"
				+ "NAME VARCHAR(255) NOT NULL," + "IP VARCHAR(255) NOT NULL," + "PORT INT NOT NULL,"
				+ "CAPACITY INT NOT NULL," + "VIVALDIMETRIC DOUBLE NOT NULL," + "UPTIME TIMESTAMP NOT NULL);";
		try {
			Statement statement = connect.createStatement();
			statement.executeUpdate(query);
			logger.info(query);
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			// close();
			e.printStackTrace();
		}
	}

	public void addNodeInfo(NodeInfo seed) {
		
		if (this.isNodePresent(seed)) return;
		String query = "INSERT INTO NODEINFO VALUES (default, ?, ?, ?, ?, ?, ?) ";
		try {
			PreparedStatement pstmt = connect.prepareStatement(query);
			pstmt.setString(1, "server-1");
			pstmt.setString(2, seed.getIp());
			pstmt.setInt(3, seed.getPort());
			pstmt.setInt(4, 100);
			pstmt.setDouble(5, seed.getVivaldimetric());
			pstmt.setTimestamp(6, new Timestamp(new Date().getTime()));
			pstmt.executeUpdate();
			logger.info(pstmt.toString());
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}
	/*
	 * Currently 'request' is not being parsed It must be parsed for server
	 * preferences
	 */
	public NodeInfo getNodeInfo(Request request) {
		String query;
		NodeInfo node = null;
		query = "SELECT * FROM NODEINFO WHERE CAPACITY < 50 ORDER BY VIVALDIMETRIC LIMIT 1";
		try {
			Statement statement = connect.createStatement();
			ResultSet rs = statement.executeQuery(query);
			logger.info(query);
			if (!rs.next()) {
				query = "SELECT * FROM NODEINFO ORDER BY CAPACITY LIMIT 1";
				rs = statement.executeQuery(query);
				if (!rs.next()) {
					return null;
				} else {
					node = NodeInfo.newBuilder().setIp(rs.getString(3)).setPort(rs.getInt(4))
							.setVivaldimetric(rs.getInt(5)).build();
					return node;
				}
			} else {
				node = NodeInfo.newBuilder().setIp(rs.getString(3)).setPort(rs.getInt(4)).setVivaldimetric(rs.getInt(5))
						.build();
				return node;
			}
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			// close();
			e.printStackTrace();
		}
		return node;
	}

	public void deleteChunkTable() {
		String query = "DROP TABLE IF EXISTS CHUNKS";
		Statement stmt;
		try {
			stmt = connect.createStatement();
			stmt.executeUpdate(query);
			logger.info(query);
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			// close();
			e.printStackTrace();
		}

	}

	public void deleteNodeTable() {
		String query = "DROP TABLE IF EXISTS NODEINFO";
		Statement stmt;
		try {
			stmt = connect.createStatement();
			stmt.executeUpdate(query);
			logger.info(query);
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			// close();
			e.printStackTrace();
		}

	}

	public void deleteFileTable() {
		String query = "DROP TABLE IF EXISTS FILEINFO";
		Statement stmt;
		try {
			stmt = connect.createStatement();
			stmt.executeUpdate(query);
			logger.info(query);
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			// close();
			e.printStackTrace();
		}

	}

	public String getBaseName(String fullpath) {
		String[] tokens = fullpath.split(".+?/(?=[^/]+$)");
		return tokens[1];
	}

	public String getParentName(String fullpath) {
		String[] tokens = fullpath.split(".+?/(?=[^/]+$)");
		return tokens[0];
	}

	public String getNodeIDs(List<NodeInfo> nodeinfolist) {
		String idstring = "";
		String query = null;
		ResultSet rs = null;
		for (NodeInfo node : nodeinfolist) {
			query = "SELECT ID FROM NODEINFO WHERE IP='" + node.getIp() + "' AND PORT=" + node.getPort();
			logger.info(query);
			try {
				Statement stmt = connect.createStatement();
				rs = stmt.executeQuery(query);
				if (!rs.next())
					return null;
				else
					idstring += rs.getInt(1) + " ";
			} catch (SQLException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
		return idstring.trim();
	}

	public void addChunks(ChunkInfo chunk) {
		String hash = chunk.getHash();
		String query = "SELECT * FROM CHUNKS WHERE HASH='" + hash + "'";
		ArrayList<NodeInfo> seeders;
		Statement stmt;
		ResultSet rs = null;
		PreparedStatement pstmt;
		try {
			stmt = connect.createStatement();
			rs = stmt.executeQuery(query);
			if (!rs.next()) {
				query = "INSERT INTO CHUNKS VALUES (default, ?, ?, ?, ?, ?) ";
				String filename = chunk.getFilename();
				pstmt = connect.prepareStatement(query);
				pstmt.setString(1, chunk.getHash());
				pstmt.setString(2, filename);
				pstmt.setInt(3, chunk.getOffset());
				pstmt.setInt(4, chunk.getLen());
				pstmt.setString(5, getNodeIDs(chunk.getSeedersList()));
				pstmt.executeUpdate();
				
			} else {
				seeders = getSeeders(rs.getString(5));
				seeders.add(chunk.getSeeders(0)); /*ASSUMPTION*/
				query = "UPDATE CHUNKS SET SEEDERS = ?" + "WHERE HASH='" + hash + "';";
				pstmt = connect.prepareStatement(query);
				pstmt.setString(1, getNodeIDs(seeders));
				pstmt.executeUpdate();
			}
			logger.info(pstmt.toString());
		} catch (SQLException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}

	}

	// public void updateFileInfo(String filename) {
	//
	// }

	public void addFileInfo(FileInfo fi) {
		String query = "INSERT INTO FILEINFO VALUES (default, ?, ?, ?, ?, ?) ";
		try {
			PreparedStatement pstmt = connect.prepareStatement(query);
			pstmt.setString(1, fi.getFilename());
			pstmt.setInt(2, fi.getSize());
			pstmt.setTimestamp(3, new Timestamp(sdf.parse(fi.getLastmodified()).getTime()));
			// pstmt.setInt(4, chunk.getLength());
			pstmt.setBoolean(4, fi.getIsDir());
			pstmt.setString(5, fi.getParent());
			pstmt.executeUpdate();
			logger.info(query);
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (ParseException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	public NodeInfo getNodeFromId(int id) {
		String query = "SELECT * FROM NODEINFO WHERE ID=" + id;
		Statement stmt;
		try {
			stmt = connect.createStatement();
			ResultSet rs = stmt.executeQuery(query);
			chunkserver.DefinesProto.NodeInfo.Builder builder = NodeInfo.newBuilder();
			logger.info(query);
			if (!rs.next()) {
				return null;
			} else {
				NodeInfo nodeinfo = builder.setIp(rs.getString(3)).setPort(rs.getInt(4)).setVivaldimetric(6).build();
				return nodeinfo;
			}
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return null;
	}
	
	public ArrayList<NodeInfo> getSeeders(String nodeids) {
		ArrayList<NodeInfo> seeders = new ArrayList<NodeInfo>();
		String[] nodes = nodeids.split("\\s+");
		for (String id : nodes) {
			int idint = Integer.parseInt(id);
			NodeInfo nodeinfo = getNodeFromId(idint);
			if (nodeinfo != null) {
				seeders.add(nodeinfo);
			}
		}
		return seeders;
	}

	public ArrayList<ChunkInfo> getChunks(String filename) {
		ArrayList<ChunkInfo> chunklist = new ArrayList<ChunkInfo>();
		String query = "SELECT * FROM CHUNKS WHERE FILENAME='" + filename + "';";
		Statement stmt;
		ChunkInfo chunk = null;
		logger.info(query);
		try {
			stmt = connect.createStatement();
			ResultSet rs = stmt.executeQuery(query);
			if (!rs.next()) {
				return chunklist;
			} else {
				do {
					chunkserver.DefinesProto.ChunkInfo.Builder builder = ChunkInfo.newBuilder();
					String[] nodeids = rs.getString(6).trim().split("\\s+");
					for (String id : nodeids) {
						int idint = Integer.parseInt(id);
						NodeInfo nodeinfo = getNodeFromId(idint);
						if (nodeinfo != null) {
							builder.addSeeders(nodeinfo);
						}
					}
					chunk = builder.setHash(rs.getString(2)).setFilename(rs.getString(3)).setOffset(rs.getInt(4))
							.setLen(rs.getInt(5)).build();
					chunklist.add(chunk);
				} while (rs.next());
			}
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return chunklist;
	}

	public ArrayList<String> getSubDirNames(String dirname) {
		ArrayList<String> dirlist = new ArrayList<String>();
		String query = "SELECT FILENAME FROM FILEINFO WHERE PARENT='" + dirname + "';";
		Statement stmt;
		logger.info(query);
		try {
			stmt = connect.createStatement();
			ResultSet rs = stmt.executeQuery(query);

			while (rs.next()) {
				dirlist.add(rs.getString(1));
			}

		} catch (SQLException e) {
			// TODO
			e.printStackTrace();
		}
		return dirlist;
	}

	public FileInfo getFileInfo(String filename) {
		String query = "SELECT * FROM FILEINFO WHERE FILENAME='" + filename + "';";
		Statement stmt;
		Builder builder = FileInfo.newBuilder();
		logger.info(query);
		try {
			stmt = connect.createStatement();
			ResultSet rs = stmt.executeQuery(query);
			if (!rs.next()) {
				return null;
			} else {
				FileInfo fi = builder.setFilename(rs.getString(2)).setSize(rs.getInt(3))
						.setLastmodified(sdf.format(rs.getDate(4))).setIsDir(rs.getBoolean(5))
						.setParent(rs.getString(6)).build();
				return fi;

			}
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return null;
	}

	private void close() {

		if (connect != null)
			try {
				connect.close();
			} catch (SQLException e) {
				e.printStackTrace();
			}
	}

	

	public int updateFileInfo(Request request) {
		String filename = request.getFilename();
		FileInfo fi = getFileInfo(filename);
		String query = null;
		if (fi == null) {
			addFileInfo(request.getFileinfo());
		} else {
			fi = request.getFileinfo();
			query = "UPDATE FILEINFO SET SIZE = ?, LAST_MODIFIED = ?, DIRECTORY = ?, PARENT, = ? " + "WHERE FILENAME='"
					+ filename + "';";
			try {
				PreparedStatement pstmt = connect.prepareStatement(query);
				pstmt.setInt(1, fi.getSize());
				pstmt.setTimestamp(2, new Timestamp(sdf.parse(fi.getLastmodified()).getTime()));
				pstmt.setBoolean(3, fi.getIsDir());
				pstmt.setString(4, fi.getParent());
				pstmt.executeUpdate();
				logger.info(query);
			} catch (SQLException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (ParseException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}

		}
		return 0;
	}

	public int addDir(Request request) {
		String filename = request.getFileinfo().getFilename();
		String parent = request.getFileinfo().getParent();
		String query = "SELECT * FROM FILEINFO WHERE FILENAME='" + parent + "' AND DIRECTORY=TRUE;";
		logger.info(query);
		Statement stmt;
		try {
			stmt = connect.createStatement();
			ResultSet rs = stmt.executeQuery(query);
			if (rs.next()) {
				/* Parent exists */
				addFileInfo(request.getFileinfo());
			} else {
				return -1;
			}
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		return 0;

	}

	public int removeDir(Request request) {
		// TODO Auto-generated method stub

		String filename = request.getFileinfo().getFilename();
		String query = "SELECT FILENAME FROM FILEINFO WHERE PARENT='" + filename + "';";
		logger.info(query);
		try {
			Statement stmt = connect.createStatement();
			ResultSet rs = stmt.executeQuery(query);
			if (rs.next()) {
				return -39; /* ENOTEMPTY error code */
			} else {
				// removeChunks(filename);
				query = "DELETE FROM FILEINFO WHERE FILENAME='" + filename + "';";
				logger.info(query);
				stmt.executeUpdate(query);
			}
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return 0;
	}

	public int removeFile(Request request) {
		// TODO Auto-generated method stub
		String filename = request.getFileinfo().getFilename();
		removeChunks(filename);
		String query = "DELETE FROM FILEINFO WHERE FILENAME='" + filename + "';";
		logger.info(query);
		Statement stmt;
		try {
			stmt = connect.createStatement();
			stmt.executeUpdate(query);

		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return 0;
	}

	private void removeChunks(String filename) {
		// TODO Auto-generated method stub
		String query = "DELETE FROM CHUNKS WHERE FILENAME='" + filename + "';";
		logger.info(query);
		Statement stmt;
		try {
			stmt = connect.createStatement();
			stmt.executeUpdate(query);
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public ArrayList<NodeInfo> getRandomNodes() {
		// TODO Auto-generated method stub
		// String query = "SELECT * FROM NODEINFO ORDER BY RAND() LIMIT 3";
		String query = "SELECT * FROM NODEINFO";
		ArrayList<NodeInfo> nodes = new ArrayList<NodeInfo>();
		logger.info(query);
		try {
			Statement stmt = connect.createStatement();
			ResultSet rs = stmt.executeQuery(query);
			if (!rs.next()) {
				return nodes;
			} else {
				do {
					nodes.add(NodeInfo.newBuilder().setIp(rs.getString(3)).build());
				} while (rs.next());
			}
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		return nodes;
	}

	public void createDelayTable() {
		String query;
		query = "CREATE TABLE DELAYTABLE (" + "ID INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,"
				+ "SIP VARCHAR(255) NOT NULL," + "DIP VARCHAR(255) NOT NULL," + "DELAY DOUBLE NOT NULL)";
		try {
			Statement statement = connect.createStatement();
			statement.executeUpdate(query);
			logger.info(query);
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			// close();
			e.printStackTrace();
		}
	}

	public void deleteDelayTable() {
		String query = "DROP TABLE IF EXISTS DELAYTABLE";
		Statement stmt;
		try {
			stmt = connect.createStatement();
			stmt.executeUpdate(query);
			logger.info(query);
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			// close();
			e.printStackTrace();
		}

	}

	public void updateDelayTable(String sip, String dip, Delay delay) {
		// TODO Auto-generated method stub
		String query = "INSERT INTO DELAYTABLE VALUES (default, ?, ?, ?) ";
		try {
			PreparedStatement pstmt = connect.prepareStatement(query);
			// pstmt.setString(1, "server-1");
			pstmt.setString(1, sip);
			pstmt.setString(2, dip);
			pstmt.setDouble(3, delay.getDl());
			pstmt.executeUpdate();
			logger.info(pstmt.toString());
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public ArrayList<NodeInfo> getStorageNodes(String clientip) {
		// TODO Auto-generated method stub
		ArrayList<NodeInfo> nodes = new ArrayList<NodeInfo>();
		String query;
		NodeInfo node = null;
		query = "SELECT * FROM DELAYTABLE WHERE SIP='" + clientip + "'" + " ORDER BY DELAY LIMIT 3";
		logger.info(query);
		try {
			Statement statement = connect.createStatement();
			ResultSet rs = statement.executeQuery(query);
			logger.info(query);
			if (!rs.next()) {
				return nodes;
			} else {
				do {
					node = NodeInfo.newBuilder().setIp(rs.getString(3)).setPort(50004).setVivaldimetric(rs.getDouble(4))
							.build();
					nodes.add(node);
				} while (rs.next());
			}
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			// close();
			e.printStackTrace();
		}
		return nodes;
	}
	
	public boolean isNodePresent(NodeInfo newnode) {
		String query = "SELECT * FROM NODEINFO WHERE IP='" + newnode.getIp() + "';";
		ResultSet rs;
		try {
			Statement stmt = connect.createStatement();
			rs = stmt.executeQuery(query);
			if (rs.next()) {
				return true;
			} else {
				return false;
			}
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		return false;
		
	}
	
	public static void main(String[] args) {

		// TODO Auto-generated method stub
		// Some basic tests
		DbUtil db = new DbUtil();
		db.deleteChunkTable();
		db.deleteFileTable();
		db.deleteNodeTable();
		db.deleteDelayTable();
		db.createFileTable();
		db.createChunkTable();
		db.createNodeTable();
		db.createDelayTable();
		// db.addFileInfo(fi);

//		FileInfo fi = FileInfo.newBuilder().setFilename("/Guru").setIsDir(true)
//				.setLastmodified(sdf.format(new Timestamp(new Date().getTime()))).setSize(4096).setParent("/").build();
//		FileInfo fi2 = FileInfo.newBuilder().setFilename("/Shravan").setIsDir(true)
//				.setLastmodified(sdf.format(new Timestamp(new Date().getTime()))).setSize(4096).setParent("/").build();
//		FileInfo fi3 = FileInfo.newBuilder().setFilename("/Guru/ESA").setIsDir(false)
//				.setLastmodified(sdf.format(new Timestamp(new Date().getTime()))).setSize(1073741824).setParent("/Guru")
//				.build();
		FileInfo fi4 = FileInfo.newBuilder().setFilename("/").setIsDir(true)
				.setLastmodified(sdf.format(new Timestamp(new Date().getTime()))).setSize(4096).setParent("NO_ROOT")
				.build();
//
//		NodeInfo seed = NodeInfo.newBuilder().setIp("192.168.1.15").setPort(50004).setVivaldimetric(5).build();
//		db.addNodeInfo(seed);

//		db.addFileInfo(fi);
//		db.addFileInfo(fi2);
//		db.addFileInfo(fi3);
		db.addFileInfo(fi4);

	}

	
}
