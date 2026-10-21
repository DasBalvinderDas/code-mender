import java.security.MessageDigest;
import java.sql.*;
import javax.crypto.Cipher;
import java.io.*;

public class Vuln {
    String password = "hunter2hunter2";
    void login(Connection c, String user) throws Exception {
        Statement s = c.createStatement();
        s.executeQuery("SELECT * FROM users WHERE name = '" + user + "'");
    }
    byte[] hash(byte[] d) throws Exception { return MessageDigest.getInstance("MD5").digest(d); }
    Cipher cipher() throws Exception { return Cipher.getInstance("AES/ECB/PKCS5Padding"); }
    Object read(InputStream in) throws Exception { return new ObjectInputStream(in).readObject(); }
}
