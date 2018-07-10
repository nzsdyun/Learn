/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package javaexample.multithread;

import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author 17990
 */
public class MultiThreadExample4 {

    public static void main(String[] args) {
        // 线程中断机制，中断只是一种线程的协作机制，只是向线程发送一个中断信号，具体什么时候中断由线程决定。
        // interrupted(), isInterrupted(), interrupt()
        // interrupted(), isInterrupted()是判断线程是否被中断， interrupted是静态方法，调用的是当前线程，调用该方法后会清除中断标识。
        // interrupt中断线程，中断的结果取决于线程当前的状态
        // 1. 如果线程不是alive（NEW， TERMINATED），interrupt对线程不会有任何影响。
        // 2. 如果线程处于WAITING,TIME_WAITING(sleep, join, wait), interrupt会使线程清除中断标识，并抛出InterruptedException异常
        // 3. 如果线程处于BLOCKED并且正在IO操作， interrupt会设置线程中断标识，并关闭IO操作，抛出ClosedByInterruptException
        // 4. 如果线程处于BLOCKED并且正在selection操作，interrupt会设置线程中断标识并且selection操作立即返回。
        testInterrupt();
    }

    private static void testInterrupt() {
        InterruptThread interruptThread = new InterruptThread();
        interruptThread.interrupt();
        System.out.println("is interrupt:" + interruptThread.isInterrupted());
        interruptThread.start();
        interruptThread.interrupt();
        System.out.println("is interrupt:" + interruptThread.isInterrupted());
        
        InterruptThread interruptThread1 = new InterruptThread();
        interruptThread1.start();
        try {
            Thread.sleep(10000);
        } catch (InterruptedException ex) {
            Logger.getLogger(MultiThreadExample4.class.getName()).log(Level.SEVERE, null, ex);
        }
        interruptThread1.interrupt();
        System.out.println("is interrupt:" + interruptThread1.isInterrupted());
    }

    static class InterruptThread extends Thread {

        @Override
        public void run() {

            try {
               Thread.sleep(5000);
                while (!Thread.currentThread().isInterrupted()) {
                   try {
                       System.out.println(System.in.read());
                   } catch (IOException ex) {
                       Logger.getLogger(MultiThreadExample4.class.getName()).log(Level.SEVERE, null, ex);
                   }
                }
                System.out.println("exit io operation");

            } catch (InterruptedException e) {
                Logger.getLogger(MultiThreadExample3.class.getName()).log(Level.SEVERE, null, e);
            }
        }

    }

}
