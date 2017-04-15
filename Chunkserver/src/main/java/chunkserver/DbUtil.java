package chunkserver;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.logging.Logger;

import chunkserver.DefinesProto.ChunkInfo;
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
		query = "CREATE TABLE CHUNKS (" + "ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
				+ "HASH VARCHAR(40) NOT NULL," + "FILENAME VARCHAR(255) NOT NULL," + "OFFSET INT NOT NULL,"
				+ "LEN INT NOT NULL);";
		try {
			Statement statement = connect.createStatement();
			ResultSet rs = statement.executeQuery(query);
			logger.info(rs.toString());
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			// close();
			e.printStackTrace();
		}

	}

	public void createFileTable() {
		String query;
		query = "CREATE TABLE FILEINFO (" + "ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
				+ "FILENAME VARCHAR(255) NOT NULL," + "SIZE INT NOT NULL," + "LAST_MODIFIED DATE NOT NULL,"
				+ "DIRECTORY TINYINT NOT NULL," + "PARENT VARCHAR(255) NOT NULL);";
		try {
			Statement statement = connect.createStatement();
			ResultSet rs = statement.executeQuery(query);
			logger.info(rs.toString());
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			// close();
			e.printStackTrace();
		}
	}

	public void createNodeTable() {
		String query;
		query = "CREATE TABLE NODEINFO (" + "ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
				+ "NAME VARCHAR(255) NOT NULL," + "IP VARCHAR(255) NOT NULL," + "PORT INT NOT NULL,"
				+ "CAPACITY INT NOT NULL," + "VIVALDIMETRIC INT NOT NULL," + "UPTIME DATE NOT NULL);";
		try {
			Statement statement = connect.createStatement();
			ResultSet rs = statement.executeQuery(query);
			logger.info(rs.toString());
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			// close();
			e.printStackTrace();
		}
	}
	public void addNodeInfo(NodeInfo seed) {
		String query = "INSERT INTO NODEINFO VALUES (default, ?, ?, ?, ?, ?, ?) ";
		try {
			PreparedStatement pstmt = connect.prepareStatement(query);
			pstmt.setString(1, "server-1");
			pstmt.setString(2, seed.getIp());
			pstmt.setInt(3, seed.getPort());
			pstmt.setInt(4, 100);
			pstmt.setInt(5, seed.getVivaldimetric());
			pstmt.setDate(6, (java.sql.Date)new Date());
			pstmt.executeUpdate();
			logger.info(pstmt.getResultSet().toString());
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	/*
	 * Currently 'request' is not being parsed
	 * It must be parsed for server preferences
	 */
	public NodeInfo getNodeInfo(Request request) {
		String query;
		NodeInfo node = null;
		query = "SELECT * FROM NODEINFO WHERE CAPACITY < 50 ORDER BY VIVALDIMETRIC LIMIT 1";
		try {
			Statement statement = connect.createStatement();
			ResultSet rs = statement.executeQuery(query);
			logger.info(rs.toString());
			if (!rs.next()) {
				query = "SELECT * FROM NODEINFO ORDER BY CAPACITY LIMIT 1";
				statement.executeQuery(query);
				if (!rs.next()) {
					return null;
				} else {
					node = NodeInfo.newBuilder().setIp(rs.getString(3)).setPort(rs.getInt(4)).setVivaldimetric(rs.getInt(5)).build();
					return node;
				}
			} else {
				node = NodeInfo.newBuilder().setIp(rs.getString(3)).setPort(rs.getInt(4)).setVivaldimetric(rs.getInt(5)).build();
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
			ResultSet rs = stmt.executeQuery(query);
			logger.info(rs.toString());
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
			ResultSet rs = stmt.executeQuery(query);
			logger.info(rs.toString());
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			// close();
			e.printStackTrace();
		}

	}

	public void addChunks(ChunkInfo chunk) {
		String query = "INSERT INTO CHUNKS VALUES (default, ?, ?, ?, ?) ";
		try {
			PreparedStatement pstmt = connect.prepareStatement(query);
			pstmt.setString(1, chunk.getHash());
			pstmt.setString(2, chunk.getFilename());
			pstmt.setInt(3, chunk.getOffset());
			pstmt.setInt(4, chunk.getLen());
			pstmt.executeUpdate();
			logger.info(pstmt.getResultSet().toString());
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	public void addFileInfo(FileInfo fi) {
		String query = "INSERT INTO FILEINFO VALUES (default, ?, ?, ?, ?, ?) ";
		try {
			PreparedStatement pstmt = connect.prepareStatement(query);
			pstmt.setString(1, fi.getFilename());
			pstmt.setInt(2, fi.getSize());
			pstmt.setDate(3, (java.sql.Date) sdf.parse(fi.getLastmodified()));
			// pstmt.setInt(4, chunk.getLength());
			pstmt.setBoolean(4, fi.getIsDir());
			pstmt.setString(5, fi.getParent());
			pstmt.executeUpdate();
			logger.info(pstmt.getResultSet().toString());
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (ParseException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

	public ArrayList<ChunkInfo> getChunks(String filename) {
		ArrayList<ChunkInfo> chunklist = new ArrayList<ChunkInfo>();
		String query = "SELECT * FROM CHUNKS WHERE FILENAME=" + filename + ";";
		Statement stmt;
		try {
			stmt = connect.createStatement();
			ResultSet rs = stmt.executeQuery(query);

			if (!rs.next()) {
				return null;
			} else {
				do {
					ChunkInfo chunk = ChunkInfo.newBuilder().setHash(rs.getString(2)).setFilename(rs.getString(3))
							.setOffset(rs.getInt(4)).setLen(rs.getInt(5)).build();
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
		String query = "SELECT FILENAME FROM FILEINFO WHERE PARENT=" + dirname + ";";
		Statement stmt;
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
		String query = "SELECT * FROM FILEINFO WHERE FILENAME=" + filename;
		Statement stmt;
		Builder builder = FileInfo.newBuilder();
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

	// private void close() {
	//
	// if (connect != null)
	// try {
	// connect.close();
	// } catch (SQLException e) {
	// // TODO Auto-generated catch block
	// e.printStackTrace();
	// }
	// }

	public static void main(String[] args) {

		// TODO Auto-generated method stub
		// Some basic tests
		DbUtil db = new DbUtil();
		db.createFileTable();
		db.createChunkTable();
		db.createNodeTable();
		// db.addFileInfo(fi);

		FileInfo fi = FileInfo.newBuilder().setFilename("/Guru").setIsDir(true).setLastmodified(sdf.format(new Date()))
				.setSize(4096).setParent("/").build();
		FileInfo fi2 = FileInfo.newBuilder().setFilename("/Shravan").setIsDir(true)
				.setLastmodified(sdf.format(new Date())).setSize(4096).setParent("/").build();
		FileInfo fi3 = FileInfo.newBuilder().setFilename("ESA").setIsDir(false).setLastmodified(sdf.format(new Date()))
				.setSize(1073741824).setParent("/Guru").build();
		
		NodeInfo seed = NodeInfo.newBuilder().setIp("192.168.1.13").setPort(50005).setVivaldimetric(5).build();
		db.addNodeInfo(seed);

		db.addFileInfo(fi);
		db.addFileInfo(fi2);
		db.addFileInfo(fi3);
	}

}
