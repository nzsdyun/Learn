/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.example.encrypt;

import java.io.UnsupportedEncodingException;
import java.security.InvalidKeyException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;

/**
 *
 * @author sky
 */
public final class EncryptUtils {

    /**
     * Used to build output as Hex
     */
    private static final char[] DIGITS_LOWER = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'};

    private EncryptUtils() {
    }
    
//    public static void main(String[] args) {
//        //test
//        String encryptContent = "{\"request_id\":\"0\",\"person_id\":\"22222222222\",\"person_name\":\"222\",\"device\":{\"model\":\"MBP 2017\",\"version\":\"10.3.3\",\"plat\":\"3\"}}";
//        byte[] encrypt = encryptBySHA256(encryptContent);
//        System.err.println(printByte(encrypt));
//    }

    /**
     * use SHA256 encrypt data
     *
     * @param data need encrypt string
     * @return encrypt string
     */
    public static byte[] encryptBySHA256(final String data) {
        byte[] byteBuffer = null;
        try {
            MessageDigest message_digest = MessageDigest.getInstance("SHA-256");
            message_digest.update(data.getBytes("utf-8"));
            byteBuffer = message_digest.digest();
        } catch (NoSuchAlgorithmException | UnsupportedEncodingException ex) {
            Logger.getLogger(EncryptUtils.class.getName()).log(Level.SEVERE, null, ex);
        }
        return byteBuffer;
    }

    /**
     * use HMACSHA256 encrypt data
     *
     * @param data need encrypt string
     * @param key encrypt key
     * @return encrypt string
     * @throws java.io.UnsupportedEncodingException
     */
    public static String encryptByHMACSHA256(final String data, final String key)
            throws UnsupportedEncodingException {
        String result = null;
        try {
            Mac hmac_sha256 = Mac.getInstance("HmacSHA256");
            SecretKeySpec secret_key = new SecretKeySpec(key.getBytes(),
                    "HmacSHA256");
            hmac_sha256.init(secret_key);
            byte[] hash = hmac_sha256.doFinal(data.getBytes());
            result = encodeHexString(hash);
        } catch (NoSuchAlgorithmException | InvalidKeyException ex) {
            Logger.getLogger(EncryptUtils.class.getName()).log(Level.SEVERE, null, ex);
        }
        return result;
    }

    private static String encodeHexString(byte[] bytes) {
        char[] hexChars = new char[bytes.length * 2];
        for (int j = 0; j < bytes.length; j++) {
            int v = bytes[j] & 0xFF;
            hexChars[j * 2] = DIGITS_LOWER[v >>> 4];
            hexChars[j * 2 + 1] = DIGITS_LOWER[v & 0x0F];
        }
        return new String(hexChars);
    }
    
    private static String printByte(byte[] data) {
        StringBuilder sb = new StringBuilder();
        for(int i = 0; i < data.length; i++) {
            sb.append(data[i]);
        }
        return sb.toString();
    }

}
