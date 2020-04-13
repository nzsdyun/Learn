/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.example.test;

import com.jiantuiyuedu.mail.Mail;
import java.io.File;

/**
 *
 * @author 17990
 */
public class MailTest {
    public static void main(String[] args) {
        send();
    }
    
    private static void send() {
                Mail mail = new Mail.Builder()
                // 替换成相关域名服务商的host,这里是163
                .setHost("smtp.163.com")
                // 替换相关端口,一般是465或者587
                .setPort("465")
                // 替换相关端口,一般是465或者587
                .setPort("465")
                // 替换相关账号
                .setUser("18950855435@163.com")
                // 替换相关密码
                .setPassword("994199723abcd")
                // 替换相关发件人
                .setFrom("SkyChen")
                // 替换相关收件人
                .setTo(new String[] {
                        "1799058367@qq.com",
                })
                .setSubject("Test")
                .setBody("this is test mail")
                .build();
        File file = new  File(System.getProperty("user.dir") + File.separator + "attachment" + File.separator + "test.txt");
        try {
            mail.addAttachment(file.getPath(), file.getName());
            if (mail.send()) {
                System.out.println("send success");
            } else {
                System.out.println("send failed");
            }
        } catch (Exception e) {
                System.out.println("send failed:" + e.getMessage());
        }
    }
}
