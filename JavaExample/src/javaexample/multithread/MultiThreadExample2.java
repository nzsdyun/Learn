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
public class MultiThreadExample2 {

    private static int count = 0;
    private static int count1 = 0;
    private static int count2 = 0;
    private static boolean exit = false;
    private static Object lock = new Object();

    public static void main(String[] args) {
        // 竟态条件（race codition）: 多个线程对同一个对象进行访问和修改时，最终的执行结果和执行时序有关
        testSharedMemory();
        // 内存可见性：一个线程对一个共享变量进行修改，另一个线程不一定马上能看到或者永远看不到
        // 因为数据的读取不一定从内存中进行读取，在计算机中，数据除了内存之外，还可能保存在CPU寄存器或者各级缓存中
        // 对数据的操作也不一定写入内容，可能先保存在寄存器或者缓存中，在合适时间写入内存中。
        testMemoryVisible();
        // synchronized
        // synchronized 可以同步静态方法，实例方法，代码块
        // synchronized 同步的是对象，而不是代码，多个线程可以同时访问同一份代码，只要它的同步对象不同。
        // synchronized 同步的只要是同一个对象，即使代码不同，也会被同步顺序访问
        // 任意对象都有一个锁和一个等待队列线程
        // synchronized 执行大概过程：
        // 1. 尝试获取对象锁，成功进入第二步，否则加入等待队列
        // 2. 执行相关的代码块
        // 3. 释放锁并从等待队列线程中唤醒一个线程并执行。
        // synchronized 可以保证数据获取对象锁的时候从内存中读取，释放锁的时候数据写入内存， 从而保证数据内存的可见性。
        
        
    }
    
    private void addCount() {
        count++;
    }
    
    // 同步静态方法
    private synchronized static void addCountSyn0() {
        count++;
    }
    
    //同步实例方法
    private synchronized void addCountSyn1() {
        count1++;
    }
    // 同步代码块
    private void addCountSyn2() {
        synchronized(lock) {
            count2++;
        }
    }
    
    private synchronized static void changeExit() {
        exit = true;
    }
    
    private synchronized static boolean getExit() {
        return exit;
    }
    
    

    private static void testMemoryVisible() {
        MemoryVisibleThread memoryVisibleThread = new MemoryVisibleThread();
        memoryVisibleThread.start();
        try {
            Thread.sleep(2000);
        } catch (InterruptedException ex) {
            Logger.getLogger(MultiThreadExample2.class.getName()).log(Level.SEVERE, null, ex);
        }
//        exit = true;
        changeExit();
    }
    
    static class MemoryVisibleThread extends Thread {

        @Override
        public void run() {
            while (/*!exit*/ getExit()) {
            }
            System.out.println("memory visible thread exit");
        }
        
    }

    private static void testSharedMemory() {
        MultiThreadExample2 threadExample2 = new MultiThreadExample2();
        SharedThread[] sharedThreads = new SharedThread[100];
        for (int i = 0; i < 100; i++) {
            sharedThreads[i] = new SharedThread(threadExample2);
            sharedThreads[i].start();
        }
        try {
            for (int i = 0; i < 100; i++) {
                sharedThreads[i].join();
            }
        } catch (InterruptedException ex) {
            Logger.getLogger(MultiThreadExample2.class.getName()).log(Level.SEVERE, null, ex);
        }
        System.out.println("count:" + count);
        System.out.println("count1:" + count1);
        System.out.println("count2:" + count2);
    }

    static class SharedThread extends Thread {
        private MultiThreadExample2 threadExample2;
        public SharedThread(MultiThreadExample2 threadExample2) {
            this.threadExample2 = threadExample2;
        }

        @Override
        public void run() {
            try {
                for (int i = 0; i < 100; i++) {
                    addCountSyn0();
                }
                for (int i = 0; i < 100; i++) {
                    threadExample2.addCountSyn1();
                }
                for (int i = 0; i < 100; i++) {
                    threadExample2.addCountSyn2();
                }
                Thread.sleep((int) (Math.random() * 2000));
            } catch (InterruptedException ex) {
                Logger.getLogger(MultiThreadExample2.class.getName()).log(Level.SEVERE, null, ex);
            }
        }

    }

}
