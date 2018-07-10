/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package javaexample.multithread;

import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author 17990
 */
public class MultiThreadExample1 {

    private static Object mLock = new Object();

    public static void main(String[] args) {
        // 两种创建线程的方式
        testImpl1();
        testImpl2();
        // 线程概念：线程表示一条单独的执行流，有自己的程序计数器和栈
        // 线程状态： NEW, RUNNABLE, WAITING, TIME_WAITING_TERMINATED
        testJoin();
        // sleep, yield
        // sleep: 让出CPU，休眠一段时间
        // yield: 让出CPU，但是否让出取决于当前调度器
    }

    public static void testJoin() {
        try {
            ThreadImpl1 threadImpl1 = new ThreadImpl1();
            threadImpl1.start();
            threadImpl1.join();
            System.out.println("test join");
        } catch (InterruptedException ex) {
            Logger.getLogger(MultiThreadExample1.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    public static void testImpl1() {
        ThreadImpl1 threadImpl1 = new ThreadImpl1();
        threadImpl1.start();
    }

    public static void testImpl2() {
        Thread threadImpl2 = new Thread(new ThreadImpl2());
        threadImpl2.start();
    }

    static class ThreadImpl1 extends Thread {

        @Override
        public void run() {
            try {
                System.out.println("thread impl 1 thread id :" + Thread.currentThread().getId() + ", name:" + Thread.currentThread().getName());
                Thread.sleep(3000);
            } catch (InterruptedException ex) {
                Logger.getLogger(MultiThreadExample1.class.getName()).log(Level.SEVERE, null, ex);
            }
        }

    }

    static class ThreadImpl2 implements Runnable {

        @Override
        public void run() {
            System.out.println("thread impl 2 thread id :" + Thread.currentThread().getId() + ", name:" + Thread.currentThread().getName());
        }

    }
}
