//package org.config;
//
//import com.google.cloud.bigquery.connection.v1.Connection;
//import com.google.cloud.bigquery.connection.v1.ConnectionName;
//import com.google.cloud.bigquery.connection.v1.GetConnectionRequest;
//import com.google.cloud.bigquery.connection.v1.ConnectionServiceClient;
//
//import java.io.IOException;
//
//public class BigQueryInterface {
//    ConnectionServiceClient client;
//    ConnectionName          name;
//    GetConnectionRequest    request;
//    Connection              response;
//
//    void GetConnection(String projectId, String location, String connectionId) throws IOException {
//        this.client   = ConnectionServiceClient.create();
//        this.name     = ConnectionName.of(projectId, location, connectionId);
//        this.request  = GetConnectionRequest.newBuilder().setName(name.toString()).build();
//        this.response = client.getConnection(request);
//    }
//}
