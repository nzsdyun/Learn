/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package javaexample.multithread;

import com.sun.jmx.remote.internal.ArrayQueue;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author 17990
 */
public class MultiThreadExample3 {

    // volatile 内存的可见性
    private static volatile boolean wait = true;
    private static Object lock = new Object();

    public static void main(String[] args) {
        // 线程间的协作
        // wait/notify
        // wait/notify方法调用必须在拥有同步对象锁里面调用
        // 对象中除了维持一个锁对象和线程等待队列之外，还维护着一个条件队列
        // wait执行过程： 释放对象锁，加入对象的条件队列，阻塞线程（WAITING, TIME_WAITING），直到下一次获取对象锁
        // notify执行过程：释放对象锁，从对象的条件队列中唤醒一个线程（公平的，任意的），唤醒的线程重新获取对象锁执行。
        // 等待队列线程可能被假唤醒（spurious wakeups），所有我们一般需要循环检查执行条件。
        testWaitNotify();
        // wait等待的是对象锁，notify唤醒着是条件队列的线程。
//        testProducerConsumer();
        testCountDownLatch();
        // 异步调用
        testAsyncCall();
    }

    private static void testAsyncCall() {
        MyExecutor myExecutor = MyExecutors.newSingleThread();
        MyFuture<String> myFuture = myExecutor.execute(new MyCallable<String>() {
            @Override
            public String call() throws Exception {
                // do some things
                Thread.sleep(3000);
                return "async call";
            }
        });

        // do some things
        try {
            Thread.sleep(2000);
        } catch (InterruptedException ex) {
            Logger.getLogger(MultiThreadExample3.class.getName()).log(Level.SEVERE, null, ex);
        }
        try {
            String result = myFuture.get();
            System.out.println("async result:" + result);
        } catch (Exception e) {
            Logger.getLogger(MultiThreadExample3.class.getName()).log(Level.SEVERE, null, e);
        }
    }

    // 异步执行
    static interface MyCallable<V> {

        V call() throws Exception;
    }

    // 获取异步调用结果
    static interface MyFuture<V> {

        V get() throws Exception;
    }

    // 异步线程接口
    static interface MyExecutor {

        <V> MyFuture<V> execute(MyCallable<V> callable);
    }

    // 异步线程接口实现
    static class MyExecutors implements MyExecutor {

        private static MyExecutors singExecutors = new MyExecutors();
        private MyExcutorsThread myExcutorsThread;
        private Object lock = new Object();

        private MyExecutors() {
            myExcutorsThread = new MyExcutorsThread();
        }

        static MyExecutor newSingleThread() {
            return singExecutors;
        }

        @Override
        public <V> MyFuture<V> execute(MyCallable<V> callable) {
            myExcutorsThread.execute(callable, lock);
            return new MyFutureImpl(lock);
        }

        class MyFutureImpl<V> implements MyFuture<V> {

            private Object lock;

            public MyFutureImpl(Object lock) {
                this.lock = lock;
            }

            @Override
            public V get() throws Exception {
                synchronized (lock) {
                    while (!myExcutorsThread.isFinish()) {
                        lock.wait();
                    }
                }
                return (V) myExcutorsThread.getResult();
            }

        }

        class MyExcutorsThread<V> extends Thread {

            private MyCallable<V> callable;
            private Object lock;
            private V result;
            private volatile boolean finish = false;

            public MyExcutorsThread() {
            }

            public void execute(MyCallable<V> callable, Object lock) {
                this.callable = callable;
                this.lock = lock;
                start();
            }

            @Override
            public void run() {
                try {
                    synchronized (lock) {
                        result = callable.call();
                        lock.notify();
                    }
                    finish = true;
                } catch (Exception e) {
                    Logger.getLogger(MultiThreadExample3.class.getName()).log(Level.SEVERE, null, e);
                    finish = true;
                }
            }

            public V getResult() {
                return result;
            }

            public boolean isFinish() {
                return finish;
            }
        }
    }

    private static void testCountDownLatch() {
        DriverThread driverThread = new DriverThread();
        driverThread.start();
    }

    static class CountDownLatchO {

        private volatile int count;

        public CountDownLatchO(int count) {
            this.count = count;
        }

        public synchronized void await() {
            try {
                while (count > 0) {
                    wait();
                }
            } catch (InterruptedException ex) {
                Logger.getLogger(MultiThreadExample3.class.getName()).log(Level.SEVERE, null, ex);
            }
        }

        public synchronized void countDown() {
            count--;
            if (count <= 0) {
                notifyAll();
            }
        }

    }

    static class DriverThread extends Thread {

        // use CountDownLatch intance of
        private CountDownLatchO startCountDownLatch = new CountDownLatchO(1);
        private CountDownLatchO doneCountDownLatch = new CountDownLatchO(10);

        public DriverThread() {
            super("driver lao wang");
        }

        @Override
        public void run() {
            for (int i = 0; i < 10; i++) {
                new Thread(new WorkRunnable(startCountDownLatch, doneCountDownLatch)).start();
            }
            doWork();
            // 同时开始和结束，工人等待司机到来，司机等待所有工人
            startCountDownLatch.countDown();
            doneCountDownLatch.await();
            System.out.println("driver car......");

        }

        public void doWork() {
            try {
                Thread.sleep(2000);
                System.out.println("works i ready to driver car, are you ready ? ");
            } catch (InterruptedException ex) {
                Logger.getLogger(MultiThreadExample3.class.getName()).log(Level.SEVERE, null, ex);
            }
        }

    }

    static class WorkRunnable implements Runnable {

        // use CountDownLatch intance of
        private CountDownLatchO startCountDownLatch;
        private CountDownLatchO doneCountDownLatch;

        public WorkRunnable(CountDownLatchO startCountDownLatch, CountDownLatchO doneCountDownLatch) {
            this.startCountDownLatch = startCountDownLatch;
            this.doneCountDownLatch = doneCountDownLatch;
        }

        @Override
        public void run() {
            startCountDownLatch.await();
            System.out.println("driver " + "i " + Thread.currentThread().getName() + " will do something, please wait me....");
            doWork();
            doneCountDownLatch.countDown();
        }

        public void doWork() {
            try {
                Thread.sleep((int) (Math.random() * 2000));
                System.out.println("driver " + "i " + Thread.currentThread().getName() + " already to finish, please driver car");
            } catch (InterruptedException ex) {
                Logger.getLogger(MultiThreadExample3.class.getName()).log(Level.SEVERE, null, ex);
            }
        }

    }

    private static void testProducerConsumer() {
        ArrayQueue<String> foodQueues = new ArrayQueue<String>(10);
        ProducerThread[] producerThreads = new ProducerThread[2];
        for (int i = 0; i < 2; i++) {
            producerThreads[i] = new ProducerThread(foodQueues);
            producerThreads[i].start();
        }
        ConsumerThread[] consumerThreads = new ConsumerThread[3];
        for (int i = 0; i < 3; i++) {
            consumerThreads[i] = new ConsumerThread(foodQueues);
            consumerThreads[i].start();
        }
    }

    static class ProducerThread extends Thread {

        private ArrayQueue<String> foodQueues;

        public ProducerThread(ArrayQueue<String> foodQueues) {
            this.foodQueues = foodQueues;
        }

        @Override
        public void run() {
            try {
                while (true) {
                    synchronized (foodQueues) {
                        while (foodQueues.size() == 10) {
                            System.out.println("the foods is too many, stop produce!!!");
                            foodQueues.wait();
                        }
                        System.out.println("start produce steam roll");
                        foodQueues.add("steamed roll");
                        foodQueues.notifyAll();
                    }
                }

            } catch (Exception e) {
                Logger.getLogger(MultiThreadExample3.class.getName()).log(Level.SEVERE, null, e);
            }
        }

    }

    static class ConsumerThread extends Thread {

        private ArrayQueue<String> foodQueues;

        public ConsumerThread(ArrayQueue<String> foodQueues) {
            this.foodQueues = foodQueues;
        }

        @Override
        public void run() {
            try {
                while (true) {
                    synchronized (foodQueues) {
                        while (foodQueues.isEmpty()) {
                            System.out.println("not foods, pleas stop consume!!!");
                            foodQueues.wait();
                        }
                        String food = foodQueues.remove(0);
                        System.out.println(food + " is perfect");
                        foodQueues.notifyAll();
                    }
                }
            } catch (Exception e) {
                Logger.getLogger(MultiThreadExample3.class.getName()).log(Level.SEVERE, null, e);
            }
        }
    }

    private static void testWaitNotify() {
        WaitThread waitThread = new WaitThread();
        waitThread.start();
        try {
            Thread.sleep(3000);
        } catch (InterruptedException ex) {
            Logger.getLogger(MultiThreadExample3.class.getName()).log(Level.SEVERE, null, ex);
        }
        notifyWait();
    }

    private static void notifyWait() {
        synchronized (lock) {
            lock.notify();
            wait = false;
        }
    }

    static class WaitThread extends Thread {

        @Override
        public void run() {
            try {
                synchronized (lock) {
                    while (wait) {
                        lock.wait();
                        System.out.println("wait ...");
                    }
                    System.out.println("wait exit");
                }
            } catch (InterruptedException ex) {
                Logger.getLogger(MultiThreadExample3.class.getName()).log(Level.SEVERE, null, ex);
            }
        }
    }
}
