package chunkserver;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.logging.Logger;

import chunkserver.DefinesProto.ChunkInfo;
import chunkserver.DefinesProto.FileInfo;

/* This class has methods to create/modify/delete db tables*/
public class DbUtil {
	private static final Logger logger = Logger.getLogger(ChunkGrpcServer.class.getName());
	private Connection connect = null;

	public Connection getConnection(String username, String password) {
		if (connect != null)
			return connect;
		try {
			Class.forName("com.mysql.jdbc.Driver");
			connect = DriverManager
					.getConnection("jdbc:mysql://localhost/feedback?" + "user=" + username + "&password=" + password);
		} catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return connect;
	}

	public void createChunkTable() {
		String query;
		Connection connect = getConnection("shravan", "abc");
		query = "CREATE TABLE CHUNKS (" + "ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
				+ "HASH VARCHAR(40) NOT NULL," + "FILENAME VARCHAR(255) NOT NULL," + "OFFSET INT NOT NULL,"
				+ "LEN INT NOT NULL);";
		try {
			Statement statement = connect.createStatement();
			ResultSet rs = statement.executeQuery(query);
			logger.info(rs.toString());
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			close();
			e.printStackTrace();
		}

	}

	public void createFileTable() {
		String query;
		Connection connect = getConnection("shravan", "abc");
		query = "CREATE TABLE FILEINFO (" + "ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
				+ "FILENAME VARCHAR(255) NOT NULL," + "SIZE INT NOT NULL," + "LAST_MODIFIED DATE NOT NULL,"
				+ "DIRECTORY TINYINT NOT NULL," + "PARENT VARCHAR(255) NOT NULL);";
		try {
			Statement statement = connect.createStatement();
			ResultSet rs = statement.executeQuery(query);
			logger.info(rs.toString());
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			close();
			e.printStackTrace();
		}
	}

	public void deleteChunkTable() {
		Connection connect = getConnection("shravan", "abc");
		String query = "DROP TABLE IF EXISTS CHUNKS";
		Statement stmt;
		try {
			stmt = connect.createStatement();
			ResultSet rs = stmt.executeQuery(query);
			logger.info(rs.toString());
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			close();
			e.printStackTrace();
		}

	}

	public void deleteFileTable() {
		Connection connect = getConnection("shravan", "abc");
		String query = "DROP TABLE IF EXISTS FILEINFO";
		Statement stmt;
		try {
			stmt = connect.createStatement();
			ResultSet rs = stmt.executeQuery(query);
			logger.info(rs.toString());
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			close();
			e.printStackTrace();
		}

	}

	public void addChunks(ChunkInfo chunk) {
		Connection connect = getConnection("shravan", "abc");
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
		Connection connect = getConnection("shravan", "abc");
		String query = "INSERT INTO FILEINFO VALUES (default, ?, ?, ?, ?, ?) ";
		try {
			PreparedStatement pstmt = connect.prepareStatement(query);
			pstmt.setString(1, fi.getFilename());
			pstmt.setInt(2, fi.getSize());
			pstmt.setDate(3, (java.sql.Date) new SimpleDateFormat("MM/dd/yyyy HH:mm:ss").parse(fi.getLastmodified()));
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
		Connection connect = getConnection("shravan", "abc");
		String query = "SELECT * FROM CHUNKS WHERE FILENAME=" + filename + ";";
		Statement stmt;
		try {
			stmt = connect.createStatement();
			ResultSet rs = stmt.executeQuery(query);

			while (rs.next()) {
				ChunkInfo chunk = ChunkInfo.newBuilder().setHash(rs.getString(1)).setFilename(rs.getString(2))
						.setOffset(rs.getInt(3)).setLen(rs.getInt(4)).build();
				chunklist.add(chunk);
			}

		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return chunklist;
	}

	public ArrayList<String> getSubDirNames(String dirname) {
		ArrayList<String> dirlist = new ArrayList<String>();
		Connection connect = getConnection("shravan", "abc");
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
	
	

	private void close() {

		if (connect != null)
			try {
				connect.close();
			} catch (SQLException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
	}

	public static void main(String[] args) {

		// TODO Auto-generated method stub
		// Some basic tests
		DbUtil db = new DbUtil();
		db.createFileTable();
		db.createChunkTable();
		//db.addFileInfo(fi);
		

	}

}
