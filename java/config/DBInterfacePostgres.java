//package org.config;
//
//import java.util.ArrayList;
//import java.util.LinkedHashMap;
//
//import java.sql.Connection;
//import java.sql.DriverManager;
//import java.sql.SQLException;
//import java.sql.ResultSet;
//import java.sql.Statement;
//
//import org.json.JSONArray;
//import org.json.JSONObject;
//
//public class DBInterfacePostgres {
//    int    portNumber;
//    String sqlType, userName, password, hostName, serverName, connectString;
//
//    Connection connectorObject;
//
//    ArrayList<LinkedHashMap<String, String>> outputArray = new ArrayList<>();
//
//    void connectionSettings(String sqlType, String userName, String password, String hostName, String serverName, int portNumber) throws SQLException, ClassNotFoundException {
//        this.sqlType       = sqlType;
//        this.userName      = userName;
//        this.password      = password;
//        this.hostName      = hostName;
//        this.serverName    = serverName;
//        this.portNumber    = portNumber;
//        this.connectString = String.format("jdbc:%s://%s:%d/%s", sqlType, hostName, portNumber, serverName);
//
//        Class.forName("org.postgresql.Driver");
//        this.connectorObject = DriverManager.getConnection(connectString, userName, password);
//    }
//
//    boolean checkIfTableExists(String tableName) throws SQLException {
//        String    queryString    = String.format("SELECT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '%s')", tableName);
//        Statement queryStatement = connectorObject.createStatement();
//        ResultSet queryResult    = queryStatement.executeQuery(queryString);
//
//        return queryResult.next();
//    }
//
//
//
//    void uploadToDatabase(JSONArray uploadData, String tableName) {
//
//
//        for (int i = 0; i < uploadData.length(); i++) {
//
//        }
//    }
//
//    public static void main(String[] args) throws SQLException, ClassNotFoundException {
//        DBInterfacePostgres interfaceObject = new DBInterfacePostgres();
//        interfaceObject.connectionSettings("postgresql", "postgres", "Pani0505!", "localhost", "NaverKeywords", 5432);
//        interfaceObject.checkIfTableExists("CHSCRAPE_STATUS");
////        Connection connectorObject = null;
////        Statement  queryStatement  = null;
////        ResultSet  queryResult     = null;
////
////        try {
////            Class.forName("org.postgresql.Driver");
////            connectorObject = DriverManager.getConnection("jdbc:postgresql://localhost:5432/NaverKeywords", "postgres", "Pani0505!");
////        } catch (ClassNotFoundException | SQLException e) {
////            throw new RuntimeException(e);
////        }
////
////        queryStatement = connectorObject.createStatement();
////        queryResult    = queryStatement.executeQuery("select * from \"CALENDAR_DATA\"");
////
////        while (queryResult.next()) {
////            System.out.println(String.format("%s %s", queryResult.getString("DATE"), queryResult.getString("WEEK_NUMBER")));
////        }
//    }
//}
