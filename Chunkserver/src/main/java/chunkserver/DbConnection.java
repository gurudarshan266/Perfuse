package chunkserver;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class DbConnection {
	private Connection connect = null;
	private static DbConnection db = null;
	private DbConnection() {
		try {
			Class.forName("com.mysql.jdbc.Driver");
			connect = DriverManager
					.getConnection("jdbc:mysql://localhost/feedback?" + "user=shravan" + "&password=abc");
		} catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
	
	public static Connection getInstance() {
		if (db == null) {
			db = new DbConnection();
		}
		
		return db.connect;
	}

}
